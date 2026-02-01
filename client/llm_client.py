from typing import Any, AsyncGenerator
from dotenv import load_dotenv
from openai import AsyncOpenAI
from common.constants.environment_constants import EnvironmentConstants
from common.helpers.environment_helper import EnvironmentHelper as Env
from client.response import TextDelta, TokenUsage, StreamEvent, EventType

load_dotenv()


class LLMClient:
    def __init__(self) -> None:
        self._client: AsyncOpenAI | None = None

    def get_client(self) -> AsyncOpenAI:
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=Env.get_env_variable(EnvironmentConstants.OPEN_ROUTER_API_KEY),
                base_url=Env.get_env_variable(EnvironmentConstants.OPEN_ROUTER_BASE_URL),
            )
        return self._client

    async def close(self) -> None:
        if self._client is not None:
            await self._client.close()
            self._client = None
    
    async def chat_completion(self, messages: list[dict[str, Any]], stream: bool = True) -> AsyncGenerator[StreamEvent, None] :
        client: AsyncOpenAI = self.get_client()

        kwargs: dict[str, Any] = {
            "model": Env.get_env_variable(EnvironmentConstants.DEFAULT_MODEL_NAME),
            "messages": messages,
            "stream": stream,
        }
        if stream:
            await self._stream_response(client, kwargs)
        else:
            event = await self._non_stream_response(client, kwargs)
            yield event
        return
    
    async def _stream_response(self, client: AsyncOpenAI, kwargs: dict[str, Any]):
        pass

    async def _non_stream_response(self, client: AsyncOpenAI, kwargs: dict[str, Any]) -> StreamEvent:
        response = await client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        message = choice.message

        text_delta = None
        if message.content:
            text_delta = TextDelta(content=message.content)
        
        usage = None
        if response.usage:
            usage = TokenUsage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                cached_tokens=response.usage.prompt_tokens_details.cached_tokens
            )
        
        return StreamEvent(
            type=EventType.TEXT_DELTA,
            text_delta=text_delta,
            finish_reason=choice.finish_reason,
            usage=usage
        )