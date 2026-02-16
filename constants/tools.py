"""Constants related to tool behavior, limits, and configuration."""

# --- ReadFileTool ---
READ_FILE_MAX_SIZE = 1024 * 1024 * 10  # 10 MB
READ_FILE_MAX_OUTPUT_TOKENS = 25_000

# --- ShellTool ---
SHELL_DEFAULT_TIMEOUT = 120
SHELL_MIN_TIMEOUT = 1
SHELL_MAX_TIMEOUT = 600

SHELL_OUTPUT_MAX_BYTES = 100 * 1024  # 100 KB

BLOCKED_COMMANDS = {
    "rm -rf /",
    "rm -rf ~",
    "rm -rf /*",
    "dd if=/dev/zero",
    "dd if=/dev/random",
    "mkfs",
    "fdisk",
    "parted",
    ":(){ :|:& };:",  # Fork bomb
    "chmod 777 /",
    "chmod -R 777",
    "shutdown",
    "reboot",
    "halt",
    "poweroff",
    "init 0",
    "init 6",
}

# --- WebSearchTool ---
WEB_SEARCH_DEFAULT_MAX_RESULTS = 10
WEB_SEARCH_MIN_RESULTS = 1
WEB_SEARCH_MAX_RESULTS = 20
WEB_SEARCH_REGION = "us-en"
WEB_SEARCH_SAFESEARCH = "off"
WEB_SEARCH_TIMELIMIT = "y"

# --- WebFetchTool ---
WEB_FETCH_DEFAULT_TIMEOUT = 30
WEB_FETCH_MIN_TIMEOUT = 5
WEB_FETCH_MAX_TIMEOUT = 120
WEB_FETCH_MAX_CONTENT_BYTES = 100 * 1024  # 100 KB

# --- GrepTool ---
GREP_MAX_FILES = 500

# --- GlobTool ---
GLOB_MAX_RESULTS = 1000

# --- Directory scanning exclusions ---
DIR_SCAN_EXCLUDES = {"node_modules", "__pycache__", ".git", ".venv", "venv"}

# --- Tool arg ordering for TUI display ---
TOOL_ARG_PREFERRED_ORDER = {
    "read_file": ["path", "offset", "limit"],
    "write_file": ["path", "create_directories", "content"],
    "edit": ["path", "replace_all", "old_string", "new_string"],
    "shell": ["command", "timeout", "cwd"],
    "list_dir": ["path", "include_hidden"],
    "grep": ["path", "case_insensitive", "pattern"],
    "glob": ["path", "pattern"],
    "todos": ["id", "action", "content"],
    "memory": ["action", "key", "value"],
}

# --- File extension to language mapping ---
FILE_EXTENSION_LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".jsx": "jsx",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".json": "json",
    ".toml": "toml",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".kt": "kotlin",
    ".swift": "swift",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".hpp": "cpp",
    ".css": "css",
    ".html": "html",
    ".xml": "xml",
    ".sql": "sql",
}
