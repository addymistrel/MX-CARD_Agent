from __future__ import annotations
from typing import AsyncGenerator
from agent.events import AgentEvent, AgentEventType
from client.llm_client import LLMClient
from client.response import StreamEventType
from common.constants.error_constants import ErrorConstants
from context.manager import ContextManager


class Agent:
    def __init__(self):
        self.client = LLMClient()
        self.context_manager = ContextManager()

    async def run(self, message: str):
        yield AgentEvent.agent_start(message)
        self.context_manager.add_user_message(message)

        final_response: str | None = None

        async for event in self._agentic_loop():
            yield event

            if event.type == AgentEventType.TEXT_COMPLETE:
                final_response = event.data.get("content")

        yield AgentEvent.agent_end(final_response)

    async def _agentic_loop(self) -> AsyncGenerator[AgentEvent, None]:
        response_text = ""

        if self.client:
            async for event in self.client.chat_completion(
                self.context_manager.get_messages(), True
            ):
                if (
                    event.type == StreamEventType.TEXT_DELTA
                    and event.text_delta is not None
                ):
                    content = event.text_delta.content
                    response_text += content
                    yield AgentEvent.text_delta(content)
                elif event.type == StreamEventType.ERROR:
                    yield AgentEvent.agent_error(
                        event.error or ErrorConstants.UNKNOWN_ERROR_MESSAGE
                    )

        self.context_manager.add_assistant_message(response_text or "")
        if response_text:
            AgentEvent.text_complete(response_text)

    async def __aenter__(self) -> Agent:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.client:
            await self.client.close()
            self.client = None
