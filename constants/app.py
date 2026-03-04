"""Application-level constants: names, paths, file names."""

# Application identity
APP_NAME = "MX-CARD Agent"
APP_DIR_NAME = "mx-card-agent"
APP_PROJECT_DIR = ".mx-card-agent"

# Configuration files
CONFIG_FILE_NAME = "config.toml"
AGENT_MD_FILE = "AGENT.MD"

# Default project config template
DEFAULT_PROJECT_CONFIG = """# MX-CARD Agent — Project Configuration
# This file was auto-generated on first run. Customize as needed.
# Docs: https://mxcardagent.com/docs

[model]
# temperature = 1

# hooks_enabled = false

# [[hooks]]
# name = "example_hook"
# trigger = "before_tool"
# command = "python ./scripts/my_hook.py"

# [mcp_servers.example]
# command = "npx"
# args = ["-y", "@modelcontextprotocol/server-filesystem", "."]
"""

# Data / persistence
MEMORY_FILE_NAME = "user_memory.json"
SESSIONS_DIR_NAME = "sessions"
CHECKPOINTS_DIR_NAME = "checkpoints"
CHECKPOINT_TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Environment variable names
ENV_API_KEY = "MX_CARD_API_KEY"
ENV_BASE_URL = "MX_CARD_BASE_URL"
