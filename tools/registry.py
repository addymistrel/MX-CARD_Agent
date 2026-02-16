import logging
from pathlib import Path
from typing import Any
from tools.base import Tool, ToolInvocation, ToolResult
from tools.builtin import ReadFileTool, get_all_builtin_tools

logger = logging.getLogger(__name__)

class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            logger.warning(f"Tool '{tool.name}' is already registered. Overwriting.")

        self._tools[tool.name] = tool
        logger.debug(f"Registered tool: {tool.name}")

    def unregister(self, tool_name: str) -> bool:
        if tool_name in self._tools:
            del self._tools[tool_name]
            logger.debug(f"Unregistered tool: {tool_name}")
            return True
        else:
            logger.warning(f"Attempted to unregister non-existent tool: {tool_name}")
            return False

    def get(self, name: str) -> Tool | None:
        if name in self._tools:
            return self._tools[name]
        return None

    def get_tools(self) -> list[Tool]:
        return list(self._tools.values())

    def get_schemas(self) -> list[dict]:
        return [tool.to_openai_schema() for tool in self.get_tools()]

    async def invoke(self, name: str, params: dict[str, Any], cwd: Path | None):
        tool = self.get(name)
        if not tool:
            return ToolResult.error_result(
                f"Unknown tool: {name}",
                metadata={"tool_name": name}
            )

        logger.debug(f"Invoking tool '{name}' with params: {params} and cwd: {cwd}")
        validation_errors = tool.validate_params(params)
        if validation_errors:
            return ToolResult.error_result(
                f"Invalid parameters: {'; '.join(validation_errors)}",
                metadata={"tool_name": name, "validation_errors": validation_errors}
            )
        cwd_path = cwd if cwd else Path.cwd()
        invocation = ToolInvocation(params=params, cwd=cwd_path)
        try:
            await tool.execute(invocation)
        except Exception as e:
            logger.exception(f"Tool {name} raised unexpected error during execution")
            return ToolResult.error_result(
                f"Internal Error: {str(e)}",
                metadata={"tool_name": name}
            )

def create_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    BUILTIN_TOOLS = [ReadFileTool]

    for tool_class in get_all_builtin_tools():
        registry.register(tool_class())
        
    return registry