from typing import Any
from client.llm_client import LLMClient
from client.response import StreamEventType, TokenUsage
from constants.agent import (
    COMPACTION_TOOL_OUTPUT_TRUNCATE,
    COMPACTION_ASSISTANT_TRUNCATE,
    COMPACTION_USER_TRUNCATE,
    COMPACTION_TOOL_ARGS_TRUNCATE,
)
from context.manager import ContextManager
from prompts.system import get_compression_prompt


class ChatCompactor:
    def __init__(self, client: LLMClient):
        self.client = client

    def _format_history_for_compaction(self, messages: list[dict[str, Any]]) -> str:
        output = ["Here is the conversation that needs to be continue: \n"]

        for msg in messages:
            role = msg.get("role", "")
            content = msg.get("content", "")

            if role == "system":
                continue

            if role == "tool":
                tool_id = msg.get("tool_call_id", "unknown")

                truncated = content[:COMPACTION_TOOL_OUTPUT_TRUNCATE] if len(content) > COMPACTION_TOOL_OUTPUT_TRUNCATE else content
                if len(content) > COMPACTION_TOOL_OUTPUT_TRUNCATE:
                    truncated += "\n... [tool output truncated]"

                output.append(f"[Tool Result ({tool_id})]:\n{truncated}")
            elif role == "assistant":
                tool_details = []
                if content:
                    truncated = content[:COMPACTION_ASSISTANT_TRUNCATE] if len(content) > COMPACTION_ASSISTANT_TRUNCATE else content
                    if len(content) > COMPACTION_ASSISTANT_TRUNCATE:
                        truncated += "\n... [response truncated]"
                    output.append(f"Assistant:\n{truncated}")

                if msg.get("tool_calls"):
                    for tc in msg["tool_calls"]:
                        func = tc.get("function", {})
                        name = func.get("name", "unknown")
                        args = func.get("arguments", "{}")

                        if len(args) > COMPACTION_TOOL_ARGS_TRUNCATE:
                            args = args[:COMPACTION_TOOL_ARGS_TRUNCATE]
                        tool_details.append(f"  - {name}({args})")

                    output.append("Assistant called tools:\n" + "\n".join(tool_details))
            else:
                truncated = content[:COMPACTION_USER_TRUNCATE] if len(content) > COMPACTION_USER_TRUNCATE else content
                if len(content) > COMPACTION_USER_TRUNCATE:
                    truncated += "\n... [message truncated]"
                output.append(f"User:\n{truncated}")

        return "\n\n---\n\n".join(output)

    async def compress(
        self, context_manager: ContextManager
    ) -> tuple[str | None, TokenUsage | None]:
        messages = context_manager.get_messages()

        if len(messages) < 3:
            return None, None

        compression_messages = [
            {
                "role": "system",
                "content": get_compression_prompt(),
            },
            {
                "role": "user",
                "content": self._format_history_for_compaction(messages),
            },
        ]

        try:
            summary = ""
            usage = None
            async for event in self.client.chat_completion(
                compression_messages,
                stream=False,
            ):
                if event.type == StreamEventType.MESSAGE_COMPLETE:
                    usage = event.usage
                    if event.text_delta:
                        summary += event.text_delta.content
                elif event.type == StreamEventType.ERROR:
                    return None, None

            if not summary or not usage:
                return None, None

            return summary, usage
        except Exception:
            return None, None
