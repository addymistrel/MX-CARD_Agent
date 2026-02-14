from urllib.parse import urlparse

import httpx
from tools.base import Tool, ToolInvocation, ToolKind, ToolResult
from pydantic import BaseModel, Field

from constants.tools import WEB_FETCH_DEFAULT_TIMEOUT, WEB_FETCH_MIN_TIMEOUT, WEB_FETCH_MAX_TIMEOUT, WEB_FETCH_MAX_CONTENT_BYTES


class WebFetchParams(BaseModel):
    url: str = Field(..., description="URL to fetch (must be http:// or https://)")
    timeout: int = Field(
        WEB_FETCH_DEFAULT_TIMEOUT,
        ge=WEB_FETCH_MIN_TIMEOUT,
        le=WEB_FETCH_MAX_TIMEOUT,
        description=f"Request timeout in seconds (default: {WEB_FETCH_DEFAULT_TIMEOUT})",
    )


class WebFetchTool(Tool):
    name = "web_fetch"
    description = "Fetch content from a URL. Returns the response body as text"
    kind = ToolKind.NETWORK
    schema: type[BaseModel] = WebFetchParams

    async def execute(self, invocation: ToolInvocation) -> ToolResult:
        params = WebFetchParams(**invocation.params)

        parsed = urlparse(params.url)
        if not parsed.scheme or parsed.scheme not in ("http", "https"):
            return ToolResult.error_result(f"Url must be http:// or https://")

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(params.timeout),
                follow_redirects=True,
            ) as client:
                response = await client.get(params.url)
                response.raise_for_status()
                text = response.text
        except httpx.HTTPStatusError as e:
            return ToolResult.error_result(
                f"HTTP {e.response.status_code}: {e.response.reason_phrase}",
            )
        except Exception as e:
            return ToolResult.error_result(f"Request failed: {e}")

        if len(text) > WEB_FETCH_MAX_CONTENT_BYTES:
            text = text[:WEB_FETCH_MAX_CONTENT_BYTES] + "\n... [content truncated]"

        return ToolResult.success_result(
            text,
            metadata={
                "status_code": response.status_code,
                "content_length": len(response.content),
            },
        )
