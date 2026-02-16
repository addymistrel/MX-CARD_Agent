from __future__ import annotations
from enum import Enum
import os
from pathlib import Path
from typing import Any
from pydantic import AnyUrl, BaseModel, Field, model_validator

from constants.models import (
    DEFAULT_MODEL_NAME,
    DEFAULT_TEMPERATURE,
    MIN_TEMPERATURE,
    MAX_TEMPERATURE,
    DEFAULT_CONTEXT_WINDOW,
)
from constants.safety import (
    SHELL_ENV_DEFAULT_EXCLUDE_PATTERNS,
    HOOK_DEFAULT_TIMEOUT_SEC,
    MCP_DEFAULT_STARTUP_TIMEOUT_SEC,
)
from constants.agent import DEFAULT_MAX_TURNS
from constants.app import ENV_API_KEY, ENV_BASE_URL


class ModelConfig(BaseModel):
    name: str = DEFAULT_MODEL_NAME
    temperature: float = Field(default=DEFAULT_TEMPERATURE, ge=MIN_TEMPERATURE, le=MAX_TEMPERATURE)
    context_window: int = DEFAULT_CONTEXT_WINDOW


class ShellEnvironmentPolicy(BaseModel):
    ignore_default_excludes: bool = False
    exclude_patterns: list[str] = Field(
        default_factory=lambda: list(SHELL_ENV_DEFAULT_EXCLUDE_PATTERNS)
    )
    set_vars: dict[str, str] = Field(default_factory=dict)


class MCPServerConfig(BaseModel):
    enabled: bool = True
    startup_timeout_sec: float = MCP_DEFAULT_STARTUP_TIMEOUT_SEC

    # stdio transport
    command: str | None = None
    args: list[str] = Field(default_factory=list)
    env: dict[str, str] = Field(default_factory=dict)
    cwd: Path | None = None

    # http/sse transport
    url: str | AnyUrl = ""

    @model_validator(mode="after")
    def validate_transport(self) -> MCPServerConfig:
        has_command = self.command is not None
        has_url = bool(self.url)

        if not has_command and not has_url:
            raise ValueError(
                "MCP Server must have either 'command' (stdio) or 'url' (http/sse)"
            )

        if has_command and has_url:
            raise ValueError(
                "MCP Server cannot have both 'command' (stdio) and 'url' (http/sse)"
            )

        return self


class ApprovalPolicy(str, Enum):
    ON_REQUEST = "on-request"
    ON_FAILURE = "on-failure"
    AUTO = "auto"
    AUTO_EDIT = "auto-edit"
    NEVER = "never"
    YOLO = "yolo"


class HookTrigger(str, Enum):
    BEFORE_AGENT = "before_agent"
    AFTER_AGENT = "after_agent"
    BEFORE_TOOL = "before_tool"
    AFTER_TOOL = "after_tool"
    ON_ERROR = "on_error"


class HookConfig(BaseModel):
    name: str
    trigger: HookTrigger
    command: str | None = None  # python3 tests.py
    script: str | None = None  # *.sh
    timeout_sec: float = HOOK_DEFAULT_TIMEOUT_SEC
    enabled: bool = True

    @model_validator(mode="after")
    def validate_hook(self) -> HookConfig:
        if not self.command and not self.script:
            raise ValueError("Hook must either have 'command' or 'script'")
        return self


class Config(BaseModel):
    model: ModelConfig = Field(default_factory=ModelConfig)
    cwd: Path = Field(default_factory=Path.cwd)
    shell_environment: ShellEnvironmentPolicy = Field(
        default_factory=ShellEnvironmentPolicy
    )
    hooks_enabled: bool = False
    hooks: list[HookConfig] = Field(default_factory=list)
    approval: ApprovalPolicy = ApprovalPolicy.ON_REQUEST
    max_turns: int = DEFAULT_MAX_TURNS
    mcp_servers: dict[str, MCPServerConfig] = Field(default_factory=dict)

    allowed_tools: list[str] | None = Field(
        None,
        description="If set, only these tools will be available to the agent",
    )

    developer_instructions: str | None = None
    user_instructions: str | None = None

    debug: bool = False

    @property
    def api_key(self) -> str | None:
        return os.environ.get(ENV_API_KEY)

    @property
    def base_url(self) -> str | None:
        return os.environ.get(ENV_BASE_URL)

    @property
    def model_name(self) -> str:
        return self.model.name

    @model_name.setter
    def model_name(self, value: str) -> None:
        self.model.name = value

    @property
    def temperature(self) -> float:
        return self.model.temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self.model.temperature = value

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.api_key:
            errors.append(f"No API key found. Set {ENV_API_KEY} environment variable")

        if not self.cwd.exists():
            errors.append(f"Working directory does not exist: {self.cwd}")

        return errors

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
