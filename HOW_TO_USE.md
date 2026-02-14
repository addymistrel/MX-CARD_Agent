# 📘 HOW TO USE — MX-CARD Agent

A comprehensive guide covering **every feature, command, tool, and configuration option** of the MX-CARD AI Agent.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Quick Start](#3-quick-start)
4. [Running Modes](#4-running-modes)
5. [Interactive Commands](#5-interactive-commands)
6. [Built-in Tools](#6-built-in-tools)
7. [Subagents](#7-subagents)
8. [MCP (Model Context Protocol) Integration](#8-mcp-model-context-protocol-integration)
9. [Configuration](#9-configuration)
10. [Approval & Safety Policies](#10-approval--safety-policies)
11. [Hooks System](#11-hooks-system)
12. [Session Management](#12-session-management)
13. [Context Management](#13-context-management)
14. [Loop Detection](#14-loop-detection)
15. [AGENT.MD Support](#15-agentmd-support)
16. [Environment Variables](#16-environment-variables)
17. [Examples & Workflows](#17-examples--workflows)
18. [Troubleshooting](#18-troubleshooting)

---

## 1. Prerequisites

- **Python 3.11+**
- An **API key** from an OpenAI-compatible LLM provider (e.g., OpenRouter, OpenAI, etc.)
- A **Base URL** for the LLM API endpoint

---

## 2. Installation

```bash
# Clone the repository
git clone https://github.com/addymistrel/MX-CARD_Agent.git
cd MX-CARD_Agent

# Install dependencies
pip install -r requirements.txt
```

### Setting Up Environment Variables

Create a `.env` file in the project root:

```env
API_KEY=your-api-key-here
BASE_URL=https://openrouter.ai/api/v1
```

Or export them directly in your shell:

```bash
# Linux / macOS
export API_KEY="your-api-key-here"
export BASE_URL="https://openrouter.ai/api/v1"

# Windows (PowerShell)
$env:API_KEY = "your-api-key-here"
$env:BASE_URL = "https://openrouter.ai/api/v1"
```

---

## 3. Quick Start

```bash
# Start interactive mode (chat with the agent)
python main.py

# Run a single prompt (non-interactive)
python main.py "Explain what this project does"

# Run with a custom working directory
python main.py --cwd /path/to/project
python main.py -c /path/to/project
```

---

## 4. Running Modes

### Interactive Mode

Start the agent without a prompt argument. You get a persistent chat session with the agent where you can type messages and use slash commands.

```bash
python main.py
```

On launch, you'll see a welcome panel showing:
- The model in use
- The current working directory
- Available commands

Type your message at the `>` prompt and press Enter. The agent will respond, call tools as needed, and stream the output in real-time.

### Single-Run Mode

Pass a prompt as an argument. The agent processes the message once and exits.

```bash
python main.py "Fix the bug in main.py"
python main.py "Write a Python script to sort a list of numbers"
```

### Custom Working Directory

Use `--cwd` or `-c` to specify which directory the agent should operate in:

```bash
python main.py --cwd /home/user/my-project
python main.py -c D:\Projects\MyApp "Add error handling to the API routes"
```

---

## 5. Interactive Commands

When running in interactive mode, the following slash commands are available:

| Command | Description |
|---|---|
| `/help` | Show the help menu with all available commands |
| `/exit` or `/quit` | Exit the agent |
| `/clear` | Clear conversation history and loop detector state |
| `/config` | Display current configuration (model, temperature, approval, cwd, max_turns, hooks) |
| `/model <name>` | Change the LLM model (e.g., `/model gpt-4o`) |
| `/model` | Show the current model name |
| `/approval <mode>` | Change the approval policy (see [Approval Policies](#10-approval--safety-policies)) |
| `/approval` | Show the current approval policy |
| `/stats` | Display session statistics (turns, token usage, etc.) |
| `/tools` | List all available tools (built-in + MCP) |
| `/mcp` | Show status of all connected MCP servers |
| `/save` | Save the current session to disk |
| `/sessions` | List all previously saved sessions |
| `/resume <session_id>` | Resume a saved session by its ID |
| `/checkpoint` | Create a checkpoint of the current session state |
| `/restore <checkpoint_id>` | Restore a session from a checkpoint |

### Examples

```
> /model gpt-4o-mini
✓ Model changed to: gpt-4o-mini

> /approval auto
✓ Approval policy changed to: auto

> /config
Current Configuration
  Model: gpt-4o-mini
  Temperature: 1
  Approval: auto
  Working Dir: /home/user/project
  Max Turns: 100
  Hooks Enabled: False

> /stats
Session Statistics
  turns: 5
  total_input_tokens: 12500
  total_output_tokens: 3200

> /tools
Available tools (14)
  • read_file
  • write_file
  • edit
  • shell
  ...

> /save
✓ Session saved: a1b2c3d4-e5f6-7890-abcd-ef1234567890

> /sessions
Saved Sessions
  • a1b2c3d4-e5f6-7890-abcd-ef1234567890 (turns: 5, updated: 2026-02-11T10:30:00)

> /resume a1b2c3d4-e5f6-7890-abcd-ef1234567890
✓ Resumed session: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

---

## 6. Built-in Tools

The agent has access to a suite of built-in tools it uses autonomously to accomplish your tasks. You don't invoke these directly — the agent decides when and how to use them based on your prompt.

### 📄 `read_file` — Read File Contents

Reads the contents of a text file with line numbers. Supports reading specific portions of large files.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `path` | string | ✅ | — | File path (relative or absolute) |
| `offset` | int | ❌ | `1` | Line number to start from (1-based) |
| `limit` | int | ❌ | All | Max number of lines to read |

- Max file size: **10 MB**
- Max output tokens: **25,000**
- Cannot read binary files (images, executables, etc.)

---

### ✏️ `write_file` — Create or Overwrite a File

Writes content to a file. Creates the file (and parent directories) if it doesn't exist, or overwrites if it does.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `path` | string | ✅ | — | File path (relative or absolute) |
| `content` | string | ✅ | — | Content to write |
| `create_directories` | bool | ❌ | `true` | Auto-create parent directories |

---

### 🔧 `edit` — Surgical Text Replacement

Edit a file by finding and replacing exact text. The `old_string` must match exactly (including whitespace/indentation).

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `path` | string | ✅ | — | File path |
| `old_string` | string | ❌ | `""` | Exact text to find and replace (empty = create new file) |
| `new_string` | string | ✅ | — | Replacement text |
| `replace_all` | bool | ❌ | `false` | Replace all occurrences |

- If `old_string` is empty and the file doesn't exist, a new file is created.
- If `old_string` matches multiple locations and `replace_all` is `false`, the tool returns an error asking for more context.

---

### 💻 `shell` — Execute Shell Commands

Runs shell commands on the system. Uses `bash` on Linux/macOS and `cmd.exe` on Windows.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `command` | string | ✅ | — | The shell command to run |
| `timeout` | int | ❌ | `120` | Timeout in seconds (1–600) |
| `cwd` | string | ❌ | Working dir | Working directory for the command |

**Blocked commands** (always rejected for safety):
- `rm -rf /`, `rm -rf ~`, `rm -rf /*`
- `dd if=/dev/zero`, `dd if=/dev/random`
- `mkfs`, `fdisk`, `parted`
- Fork bombs (`:(){ :|:& };:`)
- `chmod 777 /`, `chmod -R 777`
- `shutdown`, `reboot`, `halt`, `poweroff`
- `init 0`, `init 6`

**Environment variables** with patterns matching `*KEY*`, `*TOKEN*`, `*SECRET*` are automatically excluded from the shell environment for security.

---

### 📂 `list_dir` — List Directory Contents

Lists the contents of a directory, sorted with directories first.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `path` | string | ❌ | `.` (current dir) | Directory to list |
| `include_hidden` | bool | ❌ | `false` | Include hidden files/dirs |

---

### 🔍 `grep` — Search File Contents with Regex

Searches for a regular expression pattern across files. Returns matching lines with file paths and line numbers.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `pattern` | string | ✅ | — | Regex pattern to search for |
| `path` | string | ❌ | `.` (current dir) | File or directory to search in |
| `case_insensitive` | bool | ❌ | `false` | Case-insensitive search |

- Automatically skips `node_modules`, `__pycache__`, `.git`, `.venv`, `venv` directories.
- Skips hidden files and binary files.
- Searches up to **500 files**.

---

### 🌐 `glob` — Find Files by Pattern

Finds files matching a glob pattern. Supports `**` for recursive matching.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `pattern` | string | ✅ | — | Glob pattern (e.g., `**/*.py`) |
| `path` | string | ❌ | `.` (current dir) | Directory to search in |

- Returns up to **1,000** results.

---

### 🌍 `web_search` — Search the Web

Searches the web using DuckDuckGo and returns results with titles, URLs, and snippets.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | ✅ | — | Search query |
| `max_results` | int | ❌ | `10` | Max results to return (1–20) |

---

### 🔗 `web_fetch` — Fetch Web Page Content

Fetches the content of a URL and returns the response body as text.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `url` | string | ✅ | — | URL to fetch (http/https only) |
| `timeout` | int | ❌ | `30` | Request timeout in seconds (5–120) |

- Content is truncated at **100 KB**.

---

### 🧠 `memory` — Persistent Memory Store

Stores and retrieves persistent key-value data across sessions. Saved to `user_memory.json` in the app's data directory.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `action` | string | ✅ | — | `set`, `get`, `delete`, `list`, or `clear` |
| `key` | string | ❌ | — | Memory key (required for set/get/delete) |
| `value` | string | ❌ | — | Value to store (required for set) |

**Actions:**
- `set` — Store a key-value pair
- `get` — Retrieve a value by key
- `delete` — Remove a key
- `list` — List all stored memories
- `clear` — Clear all memories

---

### ✅ `todos` — Task List Management

Tracks multi-step tasks within the current session. Useful for complex, multi-step workflows.

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `action` | string | ✅ | — | `add`, `complete`, `list`, or `clear` |
| `id` | string | ❌ | — | Todo ID (required for `complete`) |
| `content` | string | ❌ | — | Todo description (required for `add`) |

**Actions:**
- `add` — Add a new task (auto-generates a unique ID)
- `complete` — Mark a task as done by ID
- `list` — Show all pending tasks
- `clear` — Remove all tasks

---

## 7. Subagents

Subagents are **specialized, isolated AI agents** that run within the main agent to perform focused tasks. They have limited tool access and isolated context.

### 🕵️ `subagent_codebase_investigator` — Codebase Investigator

Explores and analyzes code to answer questions about code structure, patterns, and implementations.

- **Allowed tools:** `read_file`, `grep`, `glob`, `list_dir`
- **Max turns:** 20
- **Timeout:** 600 seconds (10 minutes)
- **Read-only** — does NOT modify any files

| Parameter | Type | Required | Description |
|---|---|---|---|
| `goal` | string | ✅ | The investigation task or question |

---

### 📝 `subagent_code_reviewer` — Code Reviewer

Reviews code and provides feedback on quality, bugs, security issues, and improvement opportunities.

- **Allowed tools:** `read_file`, `grep`, `list_dir`
- **Max turns:** 10
- **Timeout:** 300 seconds (5 minutes)
- **Read-only** — does NOT modify any files

| Parameter | Type | Required | Description |
|---|---|---|---|
| `goal` | string | ✅ | The code review task |

---

## 8. MCP (Model Context Protocol) Integration

The agent can connect to external **MCP servers** to extend its capabilities with additional tools.

### Supported Transports

| Transport | Config Key | Description |
|---|---|---|
| **stdio** | `command` | Launches a local process and communicates via stdin/stdout |
| **HTTP/SSE** | `url` | Connects to a remote MCP server via HTTP with Server-Sent Events |

### Configuring MCP Servers

Add MCP server configurations to your `config.toml` file:

```toml
# stdio transport example
[mcp_servers.my_server]
enabled = true
command = "node"
args = ["path/to/mcp-server.js"]
env = { MY_VAR = "value" }
cwd = "/path/to/working/dir"
startup_timeout_sec = 10

# HTTP/SSE transport example
[mcp_servers.remote_server]
enabled = true
url = "http://localhost:3000/mcp"
startup_timeout_sec = 10
```

### MCP Server Configuration Options

| Option | Type | Required | Default | Description |
|---|---|---|---|---|
| `enabled` | bool | ❌ | `true` | Enable/disable the server |
| `command` | string | ❌* | — | Command to launch (stdio transport) |
| `args` | list[str] | ❌ | `[]` | Arguments for the command |
| `env` | dict | ❌ | `{}` | Environment variables |
| `cwd` | string | ❌ | — | Working directory for the process |
| `url` | string | ❌* | — | URL for HTTP/SSE transport |
| `startup_timeout_sec` | float | ❌ | `10` | Connection timeout in seconds |

> \*Either `command` (stdio) or `url` (http/sse) must be provided, but not both.

### Managing MCP Servers at Runtime

```
> /mcp
MCP Servers (2)
  • my_server: connected (5 tools)
  • remote_server: disconnected (0 tools)
```

Tools from connected MCP servers are automatically registered and available to the agent. They appear with the naming convention `servername__toolname`.

---

## 9. Configuration

### Configuration File Locations

The agent loads configuration from **two sources** (merged together, project config overrides system config):

| Source | Path | Description |
|---|---|---|
| **System config** | `<user_config_dir>/mx-card-agent/config.toml` | Global settings for all projects |
| **Project config** | `<project_root>/.mx-card-agent/config.toml` | Project-specific settings |

The `<user_config_dir>` varies by OS:
- **Windows:** `%APPDATA%\mx-card-agent\`
- **macOS:** `~/Library/Application Support/mx-card-agent/`
- **Linux:** `~/.config/mx-card-agent/`

### Full Configuration Reference (`config.toml`)

```toml
# Model Settings
[model]
name = "arcee-ai/trinity-large-preview:free"   # LLM model name
temperature = 1.0                                # Sampling temperature (0.0 – 2.0)
context_window = 256000                          # Max context window in tokens

# General Settings
cwd = "/path/to/project"                         # Working directory (default: current dir)
approval = "on-request"                          # Approval policy (see below)
max_turns = 100                                  # Max agent loop iterations
debug = false                                    # Enable debug mode
hooks_enabled = false                            # Enable the hooks system

# Developer/user instructions
developer_instructions = "Use TypeScript for all new files"
user_instructions = "I prefer concise responses"

# Restrict available tools (optional — omit to allow all)
# allowed_tools = ["read_file", "write_file", "edit", "shell", "grep"]

# Shell Environment Policy
[shell_environment]
ignore_default_excludes = false                  # If true, skips filtering env vars
exclude_patterns = ["*KEY*", "*TOKEN*", "*SECRET*"]  # Env var patterns to exclude
set_vars = { MY_VAR = "value" }                  # Extra env vars to set

# MCP Servers
[mcp_servers.example]
enabled = true
command = "node"
args = ["server.js"]

# Hooks
[[hooks]]
name = "pre-flight"
trigger = "before_agent"
command = "python check.py"
timeout_sec = 30
enabled = true
```

### All Configuration Options

| Option | Type | Default | Description |
|---|---|---|---|
| `model.name` | string | `arcee-ai/trinity-large-preview:free` | LLM model identifier |
| `model.temperature` | float | `1.0` | Sampling temperature (0.0–2.0) |
| `model.context_window` | int | `256000` | Max context window (tokens) |
| `cwd` | string | Current directory | Working directory |
| `approval` | string | `on-request` | Approval policy |
| `max_turns` | int | `100` | Max agentic loop iterations |
| `debug` | bool | `false` | Debug mode |
| `hooks_enabled` | bool | `false` | Enable hooks system |
| `developer_instructions` | string | — | Instructions for the agent (from project maintainer) |
| `user_instructions` | string | — | Custom user instructions |
| `allowed_tools` | list[str] | All tools | Restrict which tools are available |
| `shell_environment.ignore_default_excludes` | bool | `false` | Bypass default env var filtering |
| `shell_environment.exclude_patterns` | list[str] | `["*KEY*","*TOKEN*","*SECRET*"]` | Env var name patterns to exclude |
| `shell_environment.set_vars` | dict | `{}` | Additional env vars to inject |

---

## 10. Approval & Safety Policies

The approval policy controls when the agent asks for user confirmation before executing **mutating operations** (writing files, running shell commands, etc.).

### Available Policies

| Policy | Value | Behavior |
|---|---|---|
| **On Request** | `on-request` | Asks for approval on mutating operations that aren't auto-safe. Safe read-only commands are auto-approved. **(Default)** |
| **On Failure** | `on-failure` | Auto-approves all operations; only asks after a failure |
| **Auto** | `auto` | Auto-approves all operations including shell commands |
| **Auto Edit** | `auto-edit` | Auto-approves file edits; asks for shell commands that aren't recognized as safe |
| **Never** | `never` | Only runs safe read-only commands; rejects everything else |
| **YOLO** | `yolo` | Approves **everything** without any checks (⚠️ use with caution) |

### Changing the Policy

```bash
# In config.toml
approval = "auto"

# At runtime (interactive mode)
> /approval auto
> /approval on-request
> /approval yolo
```

### Safety Features

**Dangerous Command Detection** — The following patterns are always blocked (except in `yolo` mode):

- `rm -rf /`, `rm -rf ~`, `rm -rf /*`
- `dd if=/dev/zero`, `dd if=/dev/random`
- Disk tools (`mkfs`, `fdisk`, `parted`)
- System control (`shutdown`, `reboot`, `halt`, `poweroff`)
- Permission escalation (`chmod 777 /`, `chmod -R 777`)
- Code execution from network (`curl ... | bash`, `wget ... | bash`)
- Fork bombs

**Safe Command Auto-Approval** — These commands are recognized as safe and auto-approved:

- Info commands: `ls`, `dir`, `pwd`, `cat`, `head`, `tail`, `wc`, `find`, `which`, `file`, `stat`
- Read-only git: `git status`, `git log`, `git diff`, `git show`, `git branch`
- Package info: `npm list`, `pip list`, `pip show`, `pip freeze`, `cargo tree`
- Text processing: `grep`, `awk`, `sed`, `cut`, `sort`, `uniq`, `diff`
- System info: `date`, `whoami`, `hostname`, `uname`, `ps`, `top`

**Path Safety** — File operations outside the working directory trigger additional confirmation prompts.

**Environment Variable Filtering** — Sensitive environment variables matching `*KEY*`, `*TOKEN*`, `*SECRET*` are automatically stripped from the shell environment.

---

## 11. Hooks System

Hooks let you run custom scripts or commands at specific points during the agent's lifecycle.

### Enabling Hooks

```toml
# In config.toml
hooks_enabled = true
```

### Hook Triggers

| Trigger | When it fires | Available Env Vars |
|---|---|---|
| `before_agent` | Before the agent processes a user message | `MX_CARD_AGENT_USER_MESSAGE` |
| `after_agent` | After the agent finishes responding | `MX_CARD_AGENT_USER_MESSAGE`, `MX_CARD_AGENT_RESPONSE` |
| `before_tool` | Before a tool is executed | `MX_CARD_AGENT_TOOL_NAME`, `MX_CARD_AGENT_TOOL_PARAMS` |
| `after_tool` | After a tool completes | `MX_CARD_AGENT_TOOL_NAME`, `MX_CARD_AGENT_TOOL_PARAMS`, `MX_CARD_AGENT_TOOL_RESULT` |
| `on_error` | When an error occurs | `MX_CARD_AGENT_ERROR` |

### Common Environment Variables (set for all hooks)

| Variable | Description |
|---|---|
| `MX_CARD_AGENT_TRIGGER` | The trigger type (e.g., `before_agent`) |
| `MX_CARD_AGENT_CWD` | The agent's working directory |

### Hook Configuration

```toml
# Run a command
[[hooks]]
name = "lint-check"
trigger = "after_tool"
command = "npm run lint"
timeout_sec = 30
enabled = true

# Run a script
[[hooks]]
name = "pre-flight-checks"
trigger = "before_agent"
script = """
echo "Running pre-flight checks..."
python validate_env.py
"""
timeout_sec = 60
enabled = true
```

### Hook Configuration Options

| Option | Type | Required | Default | Description |
|---|---|---|---|---|
| `name` | string | ✅ | — | Hook identifier |
| `trigger` | string | ✅ | — | When to fire (`before_agent`, `after_agent`, `before_tool`, `after_tool`, `on_error`) |
| `command` | string | ❌* | — | Shell command to run |
| `script` | string | ❌* | — | Inline script content |
| `timeout_sec` | float | ❌ | `30` | Execution timeout |
| `enabled` | bool | ❌ | `true` | Enable/disable the hook |

> \*Either `command` or `script` must be provided.

---

## 12. Session Management

### Saving & Resuming Sessions

Sessions preserve the full conversation history and token usage, allowing you to pick up exactly where you left off.

```
> /save
✓ Session saved: a1b2c3d4-...

> /sessions
Saved Sessions
  • a1b2c3d4-... (turns: 12, updated: 2026-02-11T14:30:00)
  • e5f6a7b8-... (turns: 5, updated: 2026-02-10T09:15:00)

> /resume a1b2c3d4-...
✓ Resumed session: a1b2c3d4-...
```

### Checkpoints

Checkpoints are timestamped snapshots of a session. You can create multiple checkpoints and restore any of them.

```
> /checkpoint
✓ Checkpoint created: a1b2c3d4-..._20260211_143000

> /restore a1b2c3d4-..._20260211_143000
✓ Resumed session: a1b2c3d4-..., checkpoint: a1b2c3d4-..._20260211_143000
```

### Storage Location

Sessions and checkpoints are stored in:
- **Windows:** `%LOCALAPPDATA%\mx-card-agent\`
- **macOS:** `~/Library/Application Support/mx-card-agent/`
- **Linux:** `~/.local/share/mx-card-agent/`

Subdirectories:
- `sessions/` — Saved sessions (`<session_id>.json`)
- `checkpoints/` — Checkpoints (`<session_id>_<timestamp>.json`)

Files are created with restricted permissions (`0o600`) for security.

---

## 13. Context Management

### Automatic Context Compression

When the conversation reaches **80% of the model's context window**, the agent automatically compresses the conversation history:

1. The full conversation is summarized into a structured continuation prompt
2. The summary preserves: original goal, completed actions, current state, remaining tasks
3. The conversation is replaced with the summary to free up context space
4. The agent seamlessly continues from where it left off

### Tool Output Pruning

To manage context size, old tool outputs are automatically pruned:
- The most recent **40,000 tokens** of tool output are always protected
- Older tool outputs are pruned if doing so would free at least **20,000 tokens**
- Pruned outputs are replaced with a short summary

### Token Tracking

View token usage at any time:

```
> /stats
Session Statistics
  turns: 15
  total_input_tokens: 45000
  total_output_tokens: 12000
  total_tokens: 57000
```

---

## 14. Loop Detection

The agent has built-in protection against getting stuck in repetitive loops:

- **Exact repeat detection:** If the same action is repeated **3 times** consecutively, the agent is prompted to try a different approach.
- **Cycle detection:** If a repeating cycle of **2–3 actions** is detected (e.g., A→B→A→B), the agent is alerted and asked to break the pattern.

The loop detector tracks the last **20 actions** and automatically injects a system prompt to redirect the agent when loops are detected.

---

## 15. AGENT.MD Support

Place an `AGENT.MD` file in the root of your project directory to provide project-specific instructions to the agent. These instructions are automatically loaded as `developer_instructions` in the configuration.

```markdown
<!-- AGENT.MD -->
# Project Guidelines

- Use TypeScript with strict mode enabled
- Follow the existing code style (2-space indentation)
- All new functions must have JSDoc comments
- Run `npm test` before considering a task complete
- Use the `src/utils/` folder for utility functions
```

The agent reads this file on startup and follows the instructions throughout the session.

---

## 16. Environment Variables

| Variable | Required | Description |
|---|---|---|
| `API_KEY` | ✅ | API key for the LLM provider |
| `BASE_URL` | ✅ | Base URL for the LLM API endpoint |

These can be set in a `.env` file (loaded automatically via `python-dotenv`) or as system environment variables.

---

## 17. Examples & Workflows

### Example 1: Fixing a Bug

```
> There's a bug in the login function where empty passwords are accepted. Fix it.
```

The agent will:
1. Search for the login function using `grep`
2. Read the relevant file with `read_file`
3. Identify the issue
4. Apply the fix with `edit`
5. Run tests with `shell` if applicable

---

### Example 2: Adding a Feature

```
> Add a rate limiter middleware to the Express API that limits each IP to 100 requests per 15 minutes
```

The agent will:
1. Explore the project structure with `list_dir` and `glob`
2. Read existing middleware patterns
3. Create the rate limiter using `write_file` or `edit`
4. Wire it into the application
5. Verify with tests or manual checks

---

### Example 3: Code Review via Subagent

```
> Review the code in src/auth/ for security issues
```

The agent may invoke the `subagent_code_reviewer` to perform a focused, isolated review of the authentication module.

---

### Example 4: Codebase Exploration

```
> How is the database connection managed in this project? What patterns are used?
```

The agent may invoke the `subagent_codebase_investigator` to explore and report back.

---

### Example 5: Web Research

```
> What's the latest version of React and what are the breaking changes?
```

The agent uses `web_search` and `web_fetch` to find and return current information.

---

### Example 6: Multi-Step Task with Todos

```
> Refactor the user module: extract validation into a separate file, add input sanitization, and write unit tests
```

The agent will:
1. Use `todos` to break down the task into subtasks
2. Work through each subtask systematically
3. Mark each as complete when done

---

### Example 7: Using Memory

```
> Remember that I prefer using pytest over unittest for Python projects
```

The agent stores this in `memory`, and in future sessions it will use pytest when writing tests.

---

### Example 8: Session Workflow

```
> /save                         # Save progress before leaving
# ... come back later ...
> /sessions                     # List saved sessions
> /resume abc123-def456         # Pick up where you left off
```

---

## 18. Troubleshooting

### "No API key found"

Set the `API_KEY` environment variable in your `.env` file or shell:
```bash
API_KEY=your-key-here
```

### "Working directory does not exist"

Ensure the `--cwd` path exists:
```bash
python main.py --cwd /valid/existing/path
```

### "Invalid TOML in config"

Check your `config.toml` for syntax errors. Use a TOML validator.

### MCP Server Not Connecting

- Verify the MCP server command/URL is correct
- Check `startup_timeout_sec` is sufficient
- Ensure the server is installed and accessible
- Use `/mcp` to check connection status

### Agent Stuck in a Loop

The loop detector should handle this automatically. If it persists:
- Use `/clear` to reset the conversation
- Rephrase your request more specifically
- Try breaking your request into smaller steps

### Context Too Long

The agent automatically compresses context when approaching limits. If you still hit issues:
- Use `/clear` to start fresh
- Use `/checkpoint` before long tasks so you can `/restore` if needed
- Consider using a model with a larger context window by changing `model.context_window` in your config

### Tool Not Available

Use `/tools` to see all available tools. If a tool is missing:
- Check if `allowed_tools` is set in your config (it restricts the tool list)
- For MCP tools, verify the server is connected with `/mcp`

---

## 📝 Summary of CLI Arguments

```
python main.py [PROMPT] [OPTIONS]

Arguments:
  PROMPT              Optional prompt to run in single-shot mode

Options:
  -c, --cwd PATH      Set the working directory
```

---

## 📝 Summary of All Interactive Commands

```
/help                       Show help menu
/exit, /quit                Exit the agent
/clear                      Clear conversation history
/config                     Show current configuration
/model [name]               Show or change the LLM model
/approval [mode]            Show or change approval policy
/stats                      Show session statistics
/tools                      List all available tools
/mcp                        Show MCP server status
/save                       Save current session
/sessions                   List saved sessions
/resume <session_id>        Resume a saved session
/checkpoint                 Create a session checkpoint
/restore <checkpoint_id>    Restore from a checkpoint
```

---

*Made with ❤️ by [addymistrel](https://github.com/addymistrel)*
