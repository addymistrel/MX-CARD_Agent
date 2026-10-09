from __future__ import annotations
import asyncio
import json
from typing import AsyncGenerator, Callable, TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, END, START

from agent.events import AgentEvent, AgentEventType
from agent.session import Session
from client.response import StreamEventType, TokenUsage, ToolCall, ToolResultMessage
from config.config import Config
from prompts.system import create_loop_breaker_prompt
from tools.base import ToolConfirmation


class AgentState(TypedDict):
    messages_snapshot: list[dict]
    tool_calls: list[ToolCall]
    response_text: str
    usage: TokenUsage | None
    error: str | None
    turn_count: int
    events: Annotated[list[AgentEvent], operator.add]


class Agent:
    def __init__(
        self,
        config: Config,
        confirmation_callback: Callable[[ToolConfirmation], bool] | None = None,
    ):
        self.config = config
        self.session = Session(self.config)
        self.session.approval_manager.confirmation_callback = confirmation_callback
        self._stop_requested = False
        self._pause_event = asyncio.Event()
        self._pause_event.set()
        self._graph = self._build_graph()

    def stop(self) -> None:
        self._stop_requested = True
        self._pause_event.set()

    def pause(self) -> None:
        self._pause_event.clear()

    def resume(self, additional_info: str | None = None) -> None:
        if additional_info:
            try:
                ctx = self.session.get_context_manager()
                ctx.add_user_message(additional_info)
            except Exception:
                pass
        self._pause_event.set()

    def reset_control(self) -> None:
        self._stop_requested = False
        self._pause_event.set()

    def _build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("call_model", self._node_call_model)
        graph.add_node("execute_tools", self._node_execute_tools)
        graph.add_edge(START, "call_model")
        graph.add_conditional_edges(
            "call_model",
            self._route_after_model,
            {"execute_tools": "execute_tools", END: END},
        )
        graph.add_edge("execute_tools", "call_model")
        return graph.compile()

    def _route_after_model(self, state: AgentState) -> str:
        if self._stop_requested or state.get("error"):
            return END
        if state.get("tool_calls"):
            return "execute_tools"
        return END

    async def _node_call_model(self, state: AgentState) -> dict:
        if self._stop_requested:
            return {
                "error": "Execution stopped by user",
                "events": [AgentEvent.agent_error("Execution stopped by user")],
                "tool_calls": [],
                "response_text": "",
                "usage": None,
                "turn_count": state["turn_count"],
            }

        ctx = self.session.get_context_manager()

        if ctx.needs_compression():
            summary, usage = await self.session.chat_compactor.compress(ctx)
            if summary:
                ctx.replace_with_summary(summary)
                if usage:
                    ctx.set_latest_usage(usage)
                    ctx.add_usage(usage)

        tool_schemas = self.session.tool_registry.get_schemas()
        tool_calls: list[ToolCall] = []
        response_text = ""
        usage: TokenUsage | None = None
        error: str | None = None
        events: list[AgentEvent] = []

        self.session.increment_turn()

        if state["turn_count"] >= self.config.max_turns:
            return {
                "error": f"Maximum turns ({self.config.max_turns}) reached",
                "events": [AgentEvent.agent_error(f"Maximum turns ({self.config.max_turns}) reached")],
                "tool_calls": [],
                "response_text": "",
                "usage": None,
                "turn_count": state["turn_count"],
            }

        async for event in self.session.client.chat_completion(
            ctx.get_messages(),
            tools=tool_schemas if tool_schemas else None,
        ):
            if self._stop_requested:
                break
            if not self._pause_event.is_set():
                await self._pause_event.wait()
            if self._stop_requested:
                break

            if event.type == StreamEventType.TEXT_DELTA:
                if event.text_delta:
                    content = event.text_delta.content
                    response_text += content
                    events.append(AgentEvent.text_delta(content))
            elif event.type == StreamEventType.TOOL_CALL_COMPLETE:
                if event.tool_call:
                    tool_calls.append(event.tool_call)
            elif event.type == StreamEventType.ERROR:
                error = event.error or "Unknown error occurred."
                events.append(AgentEvent.agent_error(error))
            elif event.type == StreamEventType.MESSAGE_COMPLETE:
                usage = event.usage

        if self._stop_requested:
            return {
                "error": "Execution stopped by user",
                "events": [AgentEvent.agent_error("Execution stopped by user")],
                "tool_calls": [],
                "response_text": response_text,
                "usage": usage,
                "turn_count": state["turn_count"],
            }

        ctx.add_assistant_message(
            response_text or "",
            (
                [
                    {
                        "id": tc.call_id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments),
                        },
                    }
                    for tc in tool_calls
                ]
                if tool_calls
                else None
            ),
        )

        if response_text:
            events.append(AgentEvent.text_complete(response_text))
            self.session.loop_detector.record_action("response", text=response_text)

        if not tool_calls:
            if usage:
                ctx.set_latest_usage(usage)
                ctx.add_usage(usage)
            ctx.prune_tool_outputs()

        if usage:
            ctx.set_latest_usage(usage)
            ctx.add_usage(usage)

        return {
            "tool_calls": tool_calls,
            "response_text": response_text,
            "usage": usage,
            "error": error,
            "events": events,
            "turn_count": state["turn_count"] + 1,
            "messages_snapshot": ctx.get_messages(),
        }

    async def _node_execute_tools(self, state: AgentState) -> dict:
        ctx = self.session.get_context_manager()
        tool_calls = state["tool_calls"]
        events: list[AgentEvent] = []
        tool_call_results: list[ToolResultMessage] = []

        for tool_call in tool_calls:
            if self._stop_requested:
                break
            if not self._pause_event.is_set():
                await self._pause_event.wait()
            if self._stop_requested:
                break

            tool_name = tool_call.name or "unknown"

            events.append(AgentEvent.tool_call_start(
                tool_call.call_id,
                tool_name,
                tool_call.arguments,
            ))

            self.session.loop_detector.record_action(
                "tool_call",
                tool_name=tool_name,
                args=tool_call.arguments,
            )

            result = await self.session.tool_registry.invoke(
                tool_name,
                tool_call.arguments,
                self.config.cwd,
                self.session.hook_system,
                self.session.approval_manager,
                self.session.undo_tracker,
            )

            events.append(AgentEvent.tool_call_complete(
                tool_call.call_id,
                tool_name,
                result,
            ))

            tool_call_results.append(
                ToolResultMessage(
                    tool_call_id=tool_call.call_id,
                    content=result.to_model_output(),
                    is_error=not result.success,
                )
            )

        for tool_result in tool_call_results:
            ctx.add_tool_result(
                tool_result.tool_call_id,
                tool_result.content,
            )

        loop_detection_error = self.session.loop_detector.check_for_loop()
        if loop_detection_error:
            loop_prompt = create_loop_breaker_prompt(loop_detection_error)
            ctx.add_user_message(loop_prompt)

        ctx.prune_tool_outputs()

        return {
            "tool_calls": [],
            "events": events,
            "messages_snapshot": ctx.get_messages(),
        }

    async def run(self, message: str) -> AsyncGenerator[AgentEvent, None]:
        self.reset_control()
        ctx = self.session.get_context_manager()
        await self.session.hook_system.trigger_before_agent(message)
        yield AgentEvent.agent_start(message)
        ctx.add_user_message(message)

        final_response: str | None = None
        initial_state: AgentState = {
            "messages_snapshot": ctx.get_messages(),
            "tool_calls": [],
            "response_text": "",
            "usage": None,
            "error": None,
            "turn_count": 0,
            "events": [],
        }

        async for chunk in self._graph.astream(initial_state, stream_mode="updates"):
            if self._stop_requested:
                break
            for node_name, node_output in chunk.items():
                for event in node_output.get("events", []):
                    yield event
                    if event.type == AgentEventType.TEXT_COMPLETE:
                        final_response = event.data.get("content")
            if self._stop_requested:
                break

        if self._stop_requested:
            yield AgentEvent.agent_error("Execution stopped by user.")
            return

        await self.session.hook_system.trigger_after_agent(message, final_response)
        yield AgentEvent.agent_end(final_response)

    async def __aenter__(self) -> Agent:
        await self.session.initialize()
        return self

    async def __aexit__(
        self,
        exc_type,
        exc_val,
        exc_tb,
    ) -> None:
        if self.session:
            if self.session.client:
                await self.session.client.close()
            if self.session.mcp_manager:
                await self.session.mcp_manager.shutdown()
