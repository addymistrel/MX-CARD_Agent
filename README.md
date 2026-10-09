# MX-CARD Agent

A sophisticated AI agent system built with Python and LangGraph, designed to provide intelligent assistance through a rich TUI interface and powerful tool ecosystem.

## Overview

MX-CARD Agent is a state-of-the-art AI assistant that combines:
- **LangGraph-based workflow orchestration** for complex task management
- **Rich Terminal User Interface (TUI)** for interactive conversations
- **Extensive tool ecosystem** (14+ built-in tools + MCP support)
- **Advanced safety systems** with configurable approval policies
- **Session persistence** for maintaining context across conversations
- **Subagent architecture** for specialized tasks

## Quick Start

### Prerequisites

- Python 3.11+
- OpenAI-compatible LLM API key (OpenRouter, OpenAI, etc.)
- Base URL for the LLM API endpoint

### Installation

```bash
# Clone the repository
git clone https://github.com/addymistrel/MX-CARD_Agent.git
cd MX-CARD_Agent

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
MX_CARD_API_KEY=your-api-key-here
MX_CARD_BASE_URL=https://openrouter.ai/api/v1
```

Alternatively, set environment variables directly:

```bash
# Linux / macOS
export MX_CARD_API_KEY="your-api-key-here"
export MX_CARD_BASE_URL="https://openrouter.ai/api/v1"

# Windows (PowerShell)
$env:MX_CARD_API_KEY = "your-api-key-here"
$env:MX_CARD_BASE_URL = "https://openrouter.ai/api/v1"
```

### Usage

```bash
# Start interactive mode (recommended for exploration)
python main.py

# Run a single prompt (non-interactive)
python main.py "Explain what this project does"

# Run with a custom working directory
python main.py --cwd /path/to/project
python main.py -c D:\Projects\MyApp "Add error handling to the API routes"
```

## Key Features

### 🎯 Interactive & Single-Run Modes

- **Interactive Mode**: Persistent chat sessions with slash commands
- **Single-Run Mode**: One-time processing of prompts with immediate output
- **Custom Working Directory**: Specify project root for targeted operations

### 🛠️ Built-in Tools

The agent has access to powerful tools for development and analysis:

| Tool | Description | Safe (Auto-Approved) |
|------|-------------|---------------------|
| `read_file` | Read file contents with line numbers | ✅ |
| `write_file` | Create/overwrite files | ⚠️ (approval needed) |
| `edit` | Surgical text replacement | ⚠️ (approval needed) |
| `shell` | Execute shell commands | ✅ (safe commands only) |
| `grep` | Search file contents with regex | ✅ |
| `glob` | Find files by pattern | ✅ |
| `list_dir` | List directory contents | ✅ |
| `web_search` | Search the web | ✅ |
| `web_fetch` | Fetch web page content | ✅ |
| `memory` | Store/retrieve persistent data | ✅ |
| `todos` | Manage task lists | ✅ |

### 🔒 Approval Policies

Choose your safety level:

- **On Request** (default): Asks for approval on mutating operations
- **On Failure**: Auto-approves all, asks only after failure
- **Auto**: Auto-approves everything (use with caution)
- **Auto Edit**: Auto-approves file edits, asks for shell commands
- **Never**: Only runs read-only commands
- **YOLO**: Approves everything without checks

### 🔄 Session Management

- **Save/Resume**: Pick up exactly where you left off
- **Checkpoints**: Create timestamped session snapshots
- **Statistics**: View token usage, turns, and performance metrics
- **Context Management**: Automatic conversation compression

### 🤖 Subagents

Specialized AI agents for focused tasks:

- **`subagent_codebase_investigator`**: Explores code structure, patterns, and implementations (read-only)
- **`subagent_code_reviewer`**: Reviews code for quality, bugs, and improvements (read-only)

### 🔌 MCP Integration

Connect to external Model Context Protocol servers to extend capabilities:

- **stdio transport**: Launch local processes
- **HTTP/SSE transport**: Connect to remote MCP servers
- Automatic tool registration from connected servers

### 📊 Advanced Features

- **Loop Detection**: Prevents repetitive patterns
- **Context Compression**: Manages conversation history intelligently
- **Tool Output Pruning**: Controls memory usage
- **Hooks System**: Run scripts at specific trigger points
- **Environment Variable Filtering**: Automatic security filtering

## Interactive Commands

When running in interactive mode, use these slash commands:

| Command | Description |
|---------|-------------|
| `/help` | Show help menu |
| `/exit`, `/quit` | Exit the agent |
| `/clear` | Clear conversation history |
| `/config` | Show current configuration |
| `/model [name]` | Show or change LLM model |
| `/approval [mode]` | Show or change approval policy |
| `/stats` | Show session statistics |
| `/tools` | List all available tools |
| `/mcp` | Show MCP server status |
| `/save` | Save current session |
| `/sessions` | List saved sessions |
| `/resume <session_id>` | Resume a saved session |
| `/checkpoint` | Create session checkpoint |
| `/restore <checkpoint_id>` | Restore from checkpoint |

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
  • ...

> /save
✓ Session saved: a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## Development

### Project Structure

```
MX-CARD_Agent/
├── agent/              # Core agent logic
│   ├── agent.py        # LangGraph-based agent implementation
│   ├── events.py       # Event system
│   └── session.py      # Session management
├── ui/                 # Terminal UI components
│   └── tui.py         # Rich TUI interface
├── tools/             # Built-in tools
│   └── builtin/       # Core tools
├── config/            # Configuration system
├── prompts/           # System prompts
├── mx-ui/             # Web UI components
├── scripts/           # Automation scripts
└── docs/              # Documentation
```

### Configuration

The agent uses a hierarchical configuration system:

1. **System config** (`%APPDATA%\mx-card-agent\config.toml` on Windows)
2. **Project config** (deprecated, can be re-enabled with `MX_CARD_ENABLE_PROJECT_CONFIG=1`)

Example `config.toml`:

```toml
[model]
name = "arcee-ai/trinity-large-preview:free"
temperature = 1.0
context_window = 256000

[general]
cwd = "/path/to/project"
approval = "on-request"
max_turns = 100
debug = false
hooks_enabled = false
```

### Developer Instructions

Place an `AGENT.MD` file in your project root to provide project-specific instructions:

```markdown
<!-- AGENT.MD -->
# Project Guidelines

- Use TypeScript with strict mode enabled
- Follow the existing code style (2-space indentation)
- All new functions must have JSDoc comments
- Run `npm test` before considering a task complete
- Use the `src/utils/` folder for utility functions
```

## Security

- **Command Blocking**: Dangerous commands are always blocked
- **Environment Filtering**: Sensitive env vars (keys, tokens, secrets) are automatically filtered
- **Path Safety**: Operations outside working directory require additional confirmation
- **File Permissions**: Session files use restricted permissions (`0o600`)

## Community & Support

- **GitHub Issues**: Report bugs, request features
- **Contributing**: See `CONTRIBUTING.md` for guidelines
- **Discussions**: Ask questions and share ideas
- **Roadmap**: See `FUTURE_UPDATES.md` for planned features

## License

This project is open source under the MIT License.

## Project Metrics

- **Language**: Python 3.11+
- **Dependencies**: 120+ packages (see `requirements.txt`)
- **Architecture**: LangGraph + Rich TUI
- **Safety**: Multi-layer approval system
- **Scalability**: Built for enterprise use

*This project is made with ❤️ by [addymistrel](https://github.com/addymistrel)*