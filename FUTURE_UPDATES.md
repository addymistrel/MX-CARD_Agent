# 🚀 Future Updates — MX-CARD Agent Roadmap

This document outlines planned advancements for the MX-CARD Agent, organized by priority. Each section describes the **current state**, the **proposed future state**, and the **impact** of the change.

---

## Table of Contents

1. [Multi-Model / Multi-Provider Support](#1-multi-model--multi-provider-support)
2. [Parallel Tool Execution](#2-parallel-tool-execution)
3. [Streaming Tool Output & Progressive Rendering](#3-streaming-tool-output--progressive-rendering)
4. [Structured Planning / Chain-of-Thought (ReAct Pattern)](#4-structured-planning--chain-of-thought-react-pattern)
5. [Multi-File Apply Patch Tool](#5-multi-file-apply-patch-tool)
6. [Richer Memory System (RAG / Vector Store)](#6-richer-memory-system-rag--vector-store)
7. [Better Subagent Architecture](#7-better-subagent-architecture)
8. [Codebase Indexing & Semantic Search](#8-codebase-indexing--semantic-search)
9. [Git Integration Tools](#9-git-integration-tools)
10. [Image & Multi-Modal Support](#10-image--multi-modal-support)
11. [Cost Tracking & Budget Controls](#11-cost-tracking--budget-controls)
12. [Enhanced Error Recovery & Self-Healing](#12-enhanced-error-recovery--self-healing)
13. [Plugin System / Custom Tool SDK](#13-plugin-system--custom-tool-sdk)
14. [Web UI / API Server Mode](#14-web-ui--api-server-mode)
15. [Test Generation & Auto-Verification](#15-test-generation--auto-verification)
16. [Priority Summary Matrix](#priority-summary-matrix)

---

## 1. Multi-Model / Multi-Provider Support

**Priority:** 🔴 High &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** High

### Current State

The LLM client (`client/llm_client.py`) is **tightly coupled to OpenAI** through the `AsyncOpenAI` SDK. All API calls — streaming, tool calling, retry logic — are written directly against OpenAI's interface. To use any other model provider (Anthropic Claude, Google Gemini, Mistral, or a local model via Ollama), the entire client would need to be rewritten.

```
┌──────────┐      ┌──────────────┐      ┌──────────┐
│  Agent   │ ───▶ │  LLMClient   │ ───▶ │  OpenAI  │
│          │      │ (AsyncOpenAI)│      │   API    │
└──────────┘      └──────────────┘      └──────────┘
                   No abstraction         Only provider
```

### Future State

Introduce a `BaseLLMClient` abstract interface that defines a standard contract (`chat_completion`, `close`, etc.). Each provider gets its own implementation — `OpenAIClient`, `AnthropicClient`, `GeminiClient`, `OllamaClient`. The config file gets a `provider` field, and the correct client is instantiated at startup.

```
┌──────────┐      ┌────────────────┐      ┌──────────────┐
│  Agent   │ ───▶ │ BaseLLMClient  │ ───▶ │ OpenAIClient │
│          │      │  (abstract)    │      ├──────────────┤
└──────────┘      └────────────────┘      │ AnthropicCl. │
                   ▲ Factory Pattern      ├──────────────┤
                   │                      │ GeminiClient │
                   │                      ├──────────────┤
                   config.provider ──────▶│ OllamaClient │
                                          └──────────────┘
```

### Why It Matters

- **Provider lock-in is eliminated** — users can choose the best model for their use case (cost, speed, capability).
- **Local model support via Ollama** enables fully offline, private operation — critical for enterprise and air-gapped environments.
- **Cost optimization** — use cheaper models (GPT-4o-mini, Gemini Flash) for simple tasks and powerful models (Claude Opus, GPT-4o) for complex reasoning.

---

## 2. Parallel Tool Execution

**Priority:** 🔴 High &nbsp;|&nbsp; **Effort:** Low &nbsp;|&nbsp; **Impact:** High

### Current State

In `agent/agent.py`, when the LLM returns multiple tool calls, they are executed **one at a time** in a sequential `for` loop:

```python
for tool_call in tool_calls:
    result = await self.session.tool_registry.invoke(...)
```

If the LLM asks to read 5 files simultaneously, each file read waits for the previous one to finish — even though they are completely independent operations.

### Future State

Independent tool calls will be executed concurrently using `asyncio.gather()` or `asyncio.TaskGroup`:

```python
tasks = [
    self.session.tool_registry.invoke(tc.name, tc.arguments, ...)
    for tc in tool_calls
]
results = await asyncio.gather(*tasks)
```

A dependency analysis step will determine which calls are independent (e.g., multiple `read_file` calls) vs. dependent (e.g., `write_file` then `read_file` on the same path), and only parallelize the independent ones.

### Why It Matters

- **2–5x faster turns** when the LLM requests multiple reads, greps, or web fetches.
- Particularly impactful during the "understand" phase of a task, where the agent often reads 5–10 files in sequence.
- Near-zero risk since read-only operations have no side effects.

---

## 3. Streaming Tool Output & Progressive Rendering

**Priority:** 🟠 Medium &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** Medium

### Current State

Tool execution is a black box to the user. When the agent runs a long shell command (e.g., `npm install`, `pytest`, `docker build`), the TUI shows the tool call start, then **nothing** until the entire command finishes. The shell tool (`tools/builtin/shell.py`) uses `process.communicate()` which buffers all output until completion.

```
[Tool: shell] npm install
  ...                          ← User sees nothing for 30+ seconds
[Tool: shell] ✓ (completed)   ← Everything appears at once
```

### Future State

Introduce a `TOOL_OUTPUT_DELTA` event type in `agent/events.py`. Tool implementations (especially `shell`) will stream output line-by-line as it becomes available:

```
[Tool: shell] npm install
  ├── added lodash@4.17.21
  ├── added express@4.18.2
  ├── added 48 packages in 3.2s
[Tool: shell] ✓ (completed)
```

The shell tool will read from `process.stdout` and `process.stderr` incrementally using `asyncio.StreamReader` instead of `communicate()`.

### Why It Matters

- **Dramatically improved UX** for long-running commands — users can see progress and identify issues early.
- Enables the user to interrupt commands that are clearly going wrong, rather than waiting for timeout.
- Makes the agent feel responsive and transparent rather than opaque.

---

## 4. Structured Planning / Chain-of-Thought (ReAct Pattern)

**Priority:** 🟠 Medium &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** High

### Current State

The agent has **no explicit planning mechanism**. It relies entirely on the LLM's internal reasoning to decide what to do next. The agentic loop in `agent/agent.py` simply passes messages to the LLM and executes whatever tool calls come back. The `todos` tool exists but is optional — the LLM may or may not use it.

```
User message → LLM → Tool calls → LLM → Tool calls → ... → Final response
              (no structured reasoning visible)
```

### Future State

Implement a **ReAct (Reasoning + Acting)** pattern where the agent explicitly alternates between thinking and acting:

```
User message → THINK (plan) → ACT (tool call) → OBSERVE (result) → THINK → ACT → ... → Final response
```

Concrete additions:
- A `think` tool / scratchpad that lets the LLM reason without taking any action. This reasoning is visible to the user but not sent as a tool result.
- An explicit **planning phase** before the first tool call — the agent outputs a numbered plan, then executes it step by step.
- Automatic plan updates when the situation changes (e.g., a tool returns an unexpected error).

### Why It Matters

- **Higher accuracy on complex tasks** — structured reasoning reduces the chance of the LLM going off-track.
- **Transparency** — users can see *why* the agent is doing something, not just *what* it's doing.
- **Debuggability** — when something goes wrong, the reasoning trace makes it easy to identify where the logic broke down.

---

## 5. Multi-File Apply Patch Tool

**Priority:** 🟠 Medium &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** High

### Current State

The `edit` tool (`tools/builtin/edit_file.py`) handles single-file, single-replacement edits using string matching (`old_string` → `new_string`). For multi-file changes (e.g., renaming a function across 10 files), the agent must make 10 separate `edit` tool calls, each requiring its own LLM turn. There is no rollback if one edit fails midway.

### Future State

Add two new capabilities:

1. **`apply_patch` tool** — Accepts a unified diff (or structured multi-file edit spec) and applies changes across multiple files atomically. If any file fails, all changes are rolled back.

2. **Undo / Rollback system** — Before any file modification, the original content is snapshotted. A `/undo` command or `undo` tool reverts the last set of changes.

```
apply_patch:
  files:
    - path: src/utils.py
      edits: [{old: "foo", new: "bar"}]
    - path: src/main.py
      edits: [{old: "foo()", new: "bar()"}]
    - path: tests/test_utils.py
      edits: [{old: "foo", new: "bar"}]
  atomic: true  ← all succeed or all rollback
```

### Why It Matters

- **Faster refactoring** — multi-file renames, import updates, and signature changes happen in one tool call instead of many.
- **Atomicity** — no more half-applied changes when an edit fails midway through a batch.
- **Safety** — rollback provides a safety net, encouraging the agent (and user) to make bolder changes confidently.

---

## 6. Richer Memory System (RAG / Vector Store)

**Priority:** 🟡 Medium-Low &nbsp;|&nbsp; **Effort:** High &nbsp;|&nbsp; **Impact:** High

### Current State

Memory (`tools/builtin/memory.py`) is a **flat JSON key-value store** saved to disk. The session loads all memory entries into the system prompt as plain text (`session.py:_load_memory()`). This approach has severe limitations:

- **No semantic retrieval** — the agent can't search memory by meaning, only by exact key.
- **Scalability ceiling** — all memory is injected into the system prompt, consuming context window tokens proportionally.
- **No project-level memory** — there's no separation between user preferences and project-specific knowledge.

```
memory.json:
{
  "entries": {
    "preferred_language": "Python",
    "test_framework": "pytest"
  }
}
→ All entries dumped into system prompt
```

### Future State

A three-tier memory architecture:

1. **User Memory** (persists across all projects) — preferences, style, common patterns. Stored as structured data.

2. **Project Memory** (persists per project) — codebase architecture notes, key decisions, file purposes. Stored with embeddings for semantic retrieval.

3. **Episodic Memory** (persists per session history) — what was done in past sessions, what worked, what failed. Enables "remember last time we tried X and it didn't work because Y."

Semantic retrieval using vector embeddings (via `chromadb` or `faiss`):

```
User: "How does authentication work in this project?"
→ Vector search over project memory
→ Returns: "Auth is handled by src/auth/middleware.py using JWT tokens.
   Key decisions: We chose JWT over sessions for stateless API support.
   See also: src/config/auth.py for token settings."
```

### Why It Matters

- **Long-term learning** — the agent gets smarter over time as it accumulates project knowledge.
- **Context efficiency** — only relevant memories are retrieved, rather than dumping everything into the prompt.
- **Continuity across sessions** — the agent remembers past work without the user needing to re-explain context.

---

## 7. Better Subagent Architecture

**Priority:** 🟡 Medium-Low &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** Medium

### Current State

Subagents (`tools/subagents.py`) are independent `Agent` instances with their own `Config` and context. The parent agent has **no visibility** into what a subagent is doing — it only receives the final result. Two subagents exist: `codebase_investigator` and `code_reviewer`. Subagents cannot communicate with each other or share findings.

```
Parent Agent
  │
  ├── spawn(codebase_investigator, goal="...")
  │     └── runs independently, returns final text
  │
  └── spawn(code_reviewer, goal="...")
        └── runs independently, returns final text
```

### Future State

- **Progress streaming** — subagents emit progress events that the parent can relay to the user (e.g., "Subagent: Found 3 relevant files, analyzing...").
- **Parallel subagent execution** — the parent can spawn multiple subagents concurrently for different aspects of a task.
- **Shared workspace context** — subagents can write findings to a shared scratchpad that other subagents and the parent can read.
- **New subagent types:**
  - `test_writer` — generates unit tests for code changes
  - `documentation_writer` — updates docs based on code changes
  - `security_auditor` — scans changes for security issues
  - `refactoring_specialist` — handles complex multi-file refactoring

```
Parent Agent
  │
  ├── spawn(investigator, goal="understand auth") ──┐
  ├── spawn(test_writer, goal="write auth tests") ──┼── Shared Context
  └── spawn(security_auditor, goal="audit auth") ───┘
        │
        ▼
  All findings merged → Parent continues
```

### Why It Matters

- **Divide-and-conquer** — complex tasks are broken into specialized subtasks, each handled by an expert subagent.
- **Transparency** — progress streaming means the user isn't left in the dark during long subagent operations.
- **Quality** — specialized subagents (security, testing, docs) catch issues that a generalist agent might miss.

---

## 8. Codebase Indexing & Semantic Search

**Priority:** 🟡 Medium-Low &nbsp;|&nbsp; **Effort:** High &nbsp;|&nbsp; **Impact:** High

### Current State

Code search relies on **text-based tools only** — `grep` for pattern matching and `glob` for file path matching. The agent has no understanding of code structure (AST, symbols, imports, class hierarchies). Finding how a function is used requires multiple grep calls and manual reasoning by the LLM.

```
Agent wants to find where `authenticate()` is used:
  1. grep for "authenticate"        → finds 47 matches (many false positives)
  2. Read each file to filter       → 5+ tool calls
  3. LLM reasons about context      → token-expensive
```

### Future State

On session start (or on-demand), build a **codebase index** that includes:

- **Symbol table** — all functions, classes, methods, variables with their locations.
- **Import graph** — which files import what, dependency chains.
- **Call graph** — which functions call which other functions.
- **Semantic embeddings** — code chunks embedded for meaning-based search.

New tools:
- `semantic_search` — find code by meaning ("where is user authentication handled?")
- `find_references` — find all usages of a symbol across the codebase
- `find_definition` — jump to where a symbol is defined
- `dependency_graph` — show what a file depends on and what depends on it

```
Agent wants to find where `authenticate()` is used:
  1. find_references("authenticate") → returns 5 precise locations with context
  Done in 1 tool call.
```

### Why It Matters

- **Dramatically faster codebase navigation** — 1 tool call instead of 5–10.
- **Fewer false positives** — structural search understands code semantics, not just text patterns.
- **Better refactoring** — the agent can confidently find all usages before making changes.

---

## 9. Git Integration Tools

**Priority:** 🟡 Medium-Low &nbsp;|&nbsp; **Effort:** Low &nbsp;|&nbsp; **Impact:** Medium

### Current State

The agent has **no built-in git tools**. Any git operation requires the shell tool, which means:
- The agent must construct raw git commands (error-prone).
- Output parsing is unstructured (raw text).
- No awareness of git state when making changes.

```
Agent: shell("git status")     → raw text output, must parse
Agent: shell("git diff HEAD")  → raw diff text, must interpret
Agent: shell("git commit -m 'fix: ...'") → no structured result
```

### Future State

Dedicated, structured git tools:

| Tool | Description |
|------|-------------|
| `git_status` | Returns structured data: staged, unstaged, untracked files |
| `git_diff` | Returns parsed diffs with file-level granularity |
| `git_commit` | Commits with auto-generated or user-provided message |
| `git_log` | Returns structured commit history |
| `git_create_branch` | Creates and optionally switches to a new branch |
| `git_stash` | Stash/pop changes |

Additional capabilities:
- **Auto-generated commit messages** based on the changes made during the session.
- **PR description generation** summarizing all changes, their rationale, and testing done.
- **Change awareness** — the agent automatically knows what files have been modified.

### Why It Matters

- **Workflow completeness** — the agent can manage the entire development lifecycle from code change to commit to PR.
- **Reliability** — structured git tools eliminate the risk of malformed git commands.
- **Automation** — auto-generated commit messages and PR descriptions save significant developer time.

---

## 10. Image & Multi-Modal Support

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** Medium

### Current State

The agent is **text-only**. It cannot process images, screenshots, or any non-text input. The LLM client sends only text messages and tool calls.

### Future State

- **Image input support** — users can paste or reference images (screenshots, diagrams, mockups) in their messages.
- **Vision API integration** — leverage OpenAI's GPT-4o vision, Anthropic's Claude vision, or Google's Gemini vision to analyze images.
- **Screenshot tool** — capture the current terminal state or a window for the agent to analyze.

Use cases:
- "Here's a screenshot of the error — fix it."
- "Here's the UI mockup — implement it."
- "Here's the architecture diagram — explain the data flow."

### Why It Matters

- **Reduced friction** — users can share visual context instead of describing it in text.
- **UI development** — the agent can compare mockups to implementations.
- **Error diagnosis** — screenshots of error dialogs, browser devtools, or terminal output are instantly understood.

---

## 11. Cost Tracking & Budget Controls

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** Low &nbsp;|&nbsp; **Impact:** Medium

### Current State

Token usage is tracked in `TokenUsage` (prompt, completion, total, cached tokens) and aggregated in `ContextManager.total_usage`. However:
- **No cost calculation** — token counts are tracked but never converted to dollar amounts.
- **No budget limits** — the agent will keep running (and spending) until `max_turns` is reached.
- **No per-tool cost attribution** — impossible to identify which tools or operations are most expensive.
- `/stats` shows token counts but not costs.

### Future State

- **Model-aware cost calculation** — each model has its pricing (e.g., GPT-4o at $2.50/$10 per 1M input/output tokens). Cost is calculated per turn and cumulatively.
- **Budget limits** — configurable per-session and global spending caps. The agent warns at 80% and stops at 100%.
- **Cost attribution** — track which tool calls are most expensive (context sent before/after each call).
- **Enhanced `/stats`:**

```
Session Stats:
  Turns: 12
  Tokens: 45,230 (prompt: 38,100 | completion: 7,130 | cached: 12,400)
  Cost: $0.47 (prompt: $0.10 | completion: $0.07 | cached savings: $0.03)
  Budget remaining: $4.53 / $5.00
  Most expensive operation: shell("npm test") — $0.12 (large output)
```

### Why It Matters

- **Cost visibility** — users know exactly how much they're spending per session.
- **Budget safety** — prevents runaway spending from infinite loops or verbose tool outputs.
- **Optimization insights** — cost attribution helps identify and reduce expensive patterns.

---

## 12. Enhanced Error Recovery & Self-Healing

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** Medium

### Current State

Error handling is basic:
- Tool errors return `ToolResult.error_result()` with a string message.
- The loop detector (`context/loop_detector.py`) catches exact repeated actions and simple cycles.
- If the LLM gets stuck, a `loop_breaker_prompt` is injected.
- No automatic retry with alternative strategies.

```
Tool fails → Error message sent to LLM → LLM decides what to do
(often retries the exact same thing → loop detected → generic "try something else" prompt)
```

### Future State

- **Error classification** — categorize errors as transient (network timeout, rate limit), permanent (file not found, permission denied), or user-fixable (missing dependency, wrong path).
- **Automatic retry with strategy adjustment:**
  - Transient errors → retry with exponential backoff (already done for API calls, extend to tools).
  - Permission errors → suggest `sudo` or check file ownership.
  - Missing dependency errors → auto-install and retry.
- **Diagnostic context gathering** — when errors occur, automatically collect relevant system state (disk space, file permissions, network connectivity, running processes) and include it in the error context.
- **Error pattern learning** — remember errors and their solutions in project memory so the same mistake isn't repeated in future sessions.

### Why It Matters

- **Higher autonomy** — the agent can recover from common failures without user intervention.
- **Fewer abandoned tasks** — instead of getting stuck on an error, the agent tries alternative approaches.
- **Faster debugging** — diagnostic context gives the LLM (and the user) better information to work with.

---

## 13. Plugin System / Custom Tool SDK

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** High &nbsp;|&nbsp; **Impact:** Medium

### Current State

Tool discovery (`tools/discovery.py`) loads `.py` files from a `.mx-card/tools/` directory. While functional, it is:
- **Undocumented** — no guide for creating custom tools.
- **No packaging** — tools can't be shared or distributed.
- **No dependency management** — custom tools can't declare their own pip dependencies.
- **No versioning** — no way to track tool versions or compatibility.

### Future State

A full-featured plugin SDK:

```python
# my_plugin/tools/deploy.py
from mx_card_agent.sdk import register_tool, ToolKind

@register_tool(
    name="deploy",
    description="Deploy the application to staging or production",
    kind=ToolKind.SHELL,
    version="1.0.0",
    dependencies=["boto3", "paramiko"],
)
async def deploy(environment: str, branch: str = "main") -> str:
    # deployment logic here
    return f"Deployed {branch} to {environment}"
```

Distribution and sharing:
- `pip install mx-card-tool-docker` — install a community tool pack.
- Tool packs declare their dependencies, which are auto-installed.
- A registry/marketplace for discovering community tools.
- Versioning and compatibility checking with the core agent.

### Why It Matters

- **Extensibility** — teams can build domain-specific tools (deployment, database, cloud infrastructure) without forking the core agent.
- **Community ecosystem** — shared tools accelerate development and adoption.
- **Standardization** — a proper SDK ensures tools are well-structured, documented, and safe.

---

## 14. Web UI / API Server Mode

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** High &nbsp;|&nbsp; **Impact:** High

### Current State

The agent is **CLI/TUI only** (`main.py` + `ui/tui.py`). Interaction requires a terminal. There is no API for programmatic access, no web interface, and no way for multiple users to interact with the same agent.

### Future State

Two new interaction modes:

**1. API Server Mode (FastAPI + WebSocket):**
```
mx-card-agent serve --port 8080
```
- REST API for sending messages and retrieving responses.
- WebSocket endpoint for real-time streaming (text deltas, tool events).
- Authentication and session management.
- Enables integration with IDEs, CI/CD pipelines, and other tools.

**2. Web UI (React / Next.js):**
- Browser-based chat interface with rich formatting.
- File diff viewer for code changes.
- Tool call visualization with expandable details.
- Session history and management.
- Team collaboration — multiple users can observe or interact with the same agent session.

```
┌────────────────────────────────────────┐
│  MX-CARD Agent — Web UI               │
├────────────────────────────────────────┤
│  [Session: abc123]                     │
│                                        │
│  User: Fix the login bug               │
│                                        │
│  Agent: I'll investigate the issue...  │
│  ┌─ Tool: grep ──────────────────┐     │
│  │ pattern: "login"              │     │
│  │ path: "src/"                  │     │
│  │ ✓ 12 matches found           │     │
│  └───────────────────────────────┘     │
│                                        │
│  Agent: Found the issue in...          │
│  ┌─ Diff: src/auth/login.py ────┐     │
│  │ - if user.password == input:  │     │
│  │ + if verify_hash(user, input):│     │
│  └───────────────────────────────┘     │
│                                        │
│  [Type a message...]            [Send] │
└────────────────────────────────────────┘
```

### Why It Matters

- **Accessibility** — not everyone is comfortable in a terminal; a web UI lowers the barrier to entry.
- **Integration** — an API enables the agent to be embedded in other tools and workflows.
- **Collaboration** — teams can share agent sessions, review changes together, and manage approvals through a UI.

---

## 15. Test Generation & Auto-Verification

**Priority:** 🟢 Future &nbsp;|&nbsp; **Effort:** Medium &nbsp;|&nbsp; **Impact:** High

### Current State

The agent has **no automated testing or verification step**. The system prompt instructs the LLM to "verify changes using the project's testing procedures," but this is advisory only — there's no enforcement. The agent may or may not run tests after making changes, and it never automatically generates tests.

### Future State

- **Auto-verification step** — after completing code changes, the agentic loop automatically:
  1. Runs the project's linter/type-checker (detected from project config).
  2. Runs relevant test files (identified by file path patterns).
  3. If any check fails, the agent automatically attempts to fix the issue.

- **Test generation subagent** — a specialized subagent that:
  1. Analyzes the code changes made.
  2. Generates unit tests covering the new/modified code.
  3. Runs the tests to ensure they pass.
  4. Adds the test files to the project.

- **Coverage tracking** — after running tests, report coverage for changed files.

```
Agent workflow (after code changes):
  1. ✅ Lint check (ruff check .) — passed
  2. ✅ Type check (mypy src/) — passed
  3. ⚠️ Tests (pytest tests/) — 1 failure
  4. 🔧 Auto-fix: test_login.py assertion updated
  5. ✅ Tests (pytest tests/) — all passed
  6. 📊 Coverage: src/auth/login.py — 94% (+12%)
```

### Why It Matters

- **Higher code quality** — every change is automatically verified before being presented as "complete."
- **Fewer regressions** — auto-generated tests catch issues that manual testing might miss.
- **Developer confidence** — knowing the agent verifies its own work builds trust in its output.

---

## Priority Summary Matrix

| # | Advancement | Priority | Effort | Impact | Category |
|---|-------------|----------|--------|--------|----------|
| 1 | Multi-provider LLM support | 🔴 High | Medium | High | Core Architecture |
| 2 | Parallel tool execution | 🔴 High | Low | High | Performance |
| 3 | Streaming tool output | 🟠 Medium | Medium | Medium | UX |
| 4 | ReAct planning pattern | 🟠 Medium | Medium | High | Intelligence |
| 5 | Multi-file apply_patch | 🟠 Medium | Medium | High | Tools |
| 6 | Vector-based memory / RAG | 🟡 Med-Low | High | High | Intelligence |
| 7 | Better subagent coordination | 🟡 Med-Low | Medium | Medium | Architecture |
| 8 | Codebase indexing & search | 🟡 Med-Low | High | High | Intelligence |
| 9 | Git integration tools | 🟡 Med-Low | Low | Medium | Tools |
| 10 | Multi-modal support | 🟢 Future | Medium | Medium | Core Architecture |
| 11 | Cost tracking & budgets | 🟢 Future | Low | Medium | Operations |
| 12 | Self-healing error recovery | 🟢 Future | Medium | Medium | Reliability |
| 13 | Plugin SDK & marketplace | 🟢 Future | High | Medium | Ecosystem |
| 14 | Web UI / API server | 🟢 Future | High | High | Platform |
| 15 | Auto test generation | 🟢 Future | Medium | High | Quality |

### Recommended Implementation Order

**Phase 1 — Quick Wins (1–2 weeks):**
- Parallel tool execution (#2) — minimal code change, big performance win.
- Git integration tools (#9) — low effort, fills an obvious gap.

**Phase 2 — Core Upgrades (2–4 weeks):**
- Multi-provider support (#1) — unlocks model flexibility.
- ReAct planning pattern (#4) — improves reasoning quality.
- Multi-file apply_patch (#5) — faster refactoring.

**Phase 3 — Intelligence Layer (4–8 weeks):**
- Codebase indexing (#8) — enables semantic understanding.
- Richer memory system (#6) — enables long-term learning.
- Better subagents (#7) — enables divide-and-conquer.

**Phase 4 — Platform & Ecosystem (8+ weeks):**
- Streaming tool output (#3) — polished UX.
- Web UI / API server (#14) — broader accessibility.
- Auto test generation (#15) — quality assurance.
- Plugin SDK (#13) — community ecosystem.
- Multi-modal (#10), cost tracking (#11), self-healing (#12).

---

*Last updated: February 18, 2026*
