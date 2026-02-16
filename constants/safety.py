"""Constants related to safety, approval, and command pattern matching."""

# Shell environment default exclude patterns
SHELL_ENV_DEFAULT_EXCLUDE_PATTERNS = ["*KEY*", "*TOKEN*", "*SECRET*"]

# Dangerous command regex patterns — always rejected
DANGEROUS_COMMAND_PATTERNS = [
    # File system destruction
    r"rm\s+(-rf?|--recursive)\s+[/~]",
    r"rm\s+-rf?\s+\*",
    r"rmdir\s+[/~]",
    # Disk operations
    r"dd\s+if=",
    r"mkfs",
    r"fdisk",
    r"parted",
    # System control
    r"shutdown",
    r"reboot",
    r"halt",
    r"poweroff",
    r"init\s+[06]",
    # Permission changes on root
    r"chmod\s+(-R\s+)?777\s+[/~]",
    r"chown\s+-R\s+.*\s+[/~]",
    # Network exposure
    r"nc\s+-l",
    r"netcat\s+-l",
    # Code execution from network
    r"curl\s+.*\|\s*(bash|sh)",
    r"wget\s+.*\|\s*(bash|sh)",
    # Fork bomb
    r":\(\)\s*\{\s*:\|:&\s*\}\s*;",
]

# Safe command regex patterns — can be auto-approved
SAFE_COMMAND_PATTERNS = [
    # Information commands
    r"^(ls|dir|pwd|cd|echo|cat|head|tail|less|more|wc)(\s|$)",
    r"^(find|locate|which|whereis|file|stat)(\s|$)",
    # Development tools (read-only)
    r"^git\s+(status|log|diff|show|branch|remote|tag)(\s|$)",
    r"^(npm|yarn|pnpm)\s+(list|ls|outdated)(\s|$)",
    r"^pip\s+(list|show|freeze)(\s|$)",
    r"^cargo\s+(tree|search)(\s|$)",
    # Text processing (usually safe)
    r"^(grep|awk|sed|cut|sort|uniq|tr|diff|comm)(\s|$)",
    # System info
    r"^(date|cal|uptime|whoami|id|groups|hostname|uname)(\s|$)",
    r"^(env|printenv|set)$",
    # Process info
    r"^(ps|top|htop|pgrep)(\s|$)",
]

# Hook default timeout
HOOK_DEFAULT_TIMEOUT_SEC = 30

# MCP server default startup timeout
MCP_DEFAULT_STARTUP_TIMEOUT_SEC = 10
