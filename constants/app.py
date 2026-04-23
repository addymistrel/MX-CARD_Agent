"""Application-level constants: names, paths, file names."""

# Application identity
APP_NAME = "MX-CARD Agent"
APP_DIR_NAME = "mx-card-agent"
APP_PROJECT_DIR = ".mx-card-agent"

# Configuration files
CONFIG_FILE_NAME = "config.toml"
AGENT_MD_FILE = "AGENT.MD"

# Default system config template (global, user-level)
# Location (Windows): %APPDATA%\mx-card-agent\config.toml
DEFAULT_SYSTEM_CONFIG = """# MX-CARD Agent - System Configuration (Global)
# This file lives in your user config directory and applies to ALL projects.
#
# Windows: %APPDATA%\\mx-card-agent\\config.toml
# macOS : ~/Library/Application Support/mx-card-agent/config.toml
# Linux : ~/.config/mx-card-agent/config.toml

[model]
# name = "gpt-4.1-mini"
# temperature = 0.7

# --- MCP (Model Context Protocol) servers ---
# Add one or more servers under [mcp_servers.<name>].
# The agent will try to connect at startup. If a server fails, it will
# automatically fall back to builtin tools.

# Filesystem server via stdio (requires Node + npx)
# Provides file operations in a sandboxed directory.
[mcp_servers.filesystem]
enabled = false
startup_timeout_sec = 2.0
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "."]

# Git server via stdio (requires Node + npx)
[mcp_servers.git]
enabled = false
startup_timeout_sec = 2.0
command = "npx"
args = ["-y", "@modelcontextprotocol/server-git"]

# Example 3: Remote MCP server over SSE/HTTP
# Uncomment and set a URL:
#
# [mcp_servers.remote]
# enabled = true
# startup_timeout_sec = 2.0
# url = "http://127.0.0.1:8080/sse"
"""

# Default per-project config template
# Auto-created in <cwd>/.mx-card-agent/config.toml on first run
DEFAULT_PROJECT_CONFIG = """# MX-CARD Agent - Project Configuration
# This file is specific to this project and overrides the global system config.
# Location: <project_root>/.mx-card-agent/config.toml

# --- MCP (Model Context Protocol) servers ---
# Enable or configure MCP servers for this project.
# These settings merge on top of your global config.

# Filesystem server via stdio (requires Node + npx)
# [mcp_servers.filesystem]
# enabled = true
# startup_timeout_sec = 5.0
# command = "npx"
# args = ["-y", "@modelcontextprotocol/server-filesystem", "."]

# Git server via stdio (requires Node + npx)
# [mcp_servers.git]
# enabled = true
# startup_timeout_sec = 5.0
# command = "npx"
# args = ["-y", "@modelcontextprotocol/server-git"]

# Remote MCP server over SSE/HTTP
# [mcp_servers.remote]
# enabled = true
# startup_timeout_sec = 5.0
# url = "http://127.0.0.1:8080/sse"
"""

# Data / persistence
MEMORY_FILE_NAME = "user_memory.json"
SESSIONS_DIR_NAME = "sessions"
CHECKPOINTS_DIR_NAME = "checkpoints"
CHECKPOINT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Environment variable names
ENV_API_KEY = "MX_CARD_API_KEY"
ENV_BASE_URL = "MX_CARD_BASE_URL"
