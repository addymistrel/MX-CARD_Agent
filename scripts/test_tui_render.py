"""Smoke test: TUI must not crash when tool args contain ints/dicts.

Run it directly (it's intentionally dependency-light).
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running this file directly from the repo root.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from config.config import Config
from ui.tui import TUI


def main() -> None:
    cfg = Config(allowed_tools=None)
    tui = TUI(cfg)

    # Simulate a tool call with mixed types.
    tui.tool_call_start(
        call_id="1234567890abcdef",
        name="read_file",
        tool_kind="builtin",
        arguments={
            "filePath": "D:/tmp/example.txt",
            "startLine": 1,
            "endLine": 10,
            "isRegexp": False,
            "maxResults": 50,
            "metadata": {"nested": True, "n": 2},
            "items": [1, 2, 3],
        },
    )

    # And completion panel output.
    tui.tool_call_complete(
        call_id="1234567890abcdef",
        name="read_file",
        tool_kind="builtin",
        success=True,
        output="Showing lines 1-1 of 1\n\n1|hello",
        error=None,
        metadata={"path": "D:/tmp/example.txt", "shown_start": 1, "shown_end": 1, "total_lines": 1},
        diff=None,
        truncated=False,
        exit_code=0,
    )


if __name__ == "__main__":
    main()
