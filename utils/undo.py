"""Undo tracker for file write/edit operations."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any
import logging

logger = logging.getLogger(__name__)

MAX_UNDO_HISTORY = 50


@dataclass
class FileChange:
    """Represents a single file change that can be undone."""
    path: Path
    old_content: str | None  # None means file didn't exist (was created)
    new_content: str
    tool_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_new_file: bool = False

    @property
    def display_path(self) -> str:
        return str(self.path)

    @property
    def summary(self) -> str:
        action = "Created" if self.is_new_file else "Modified"
        return f"{action} {self.path.name} via {self.tool_name}"


class UndoTracker:
    """Tracks file changes and allows undoing the most recent ones."""

    def __init__(self) -> None:
        self._history: list[FileChange] = []

    @property
    def history(self) -> list[FileChange]:
        return list(self._history)

    @property
    def has_changes(self) -> bool:
        return len(self._history) > 0

    @property
    def last_change(self) -> FileChange | None:
        return self._history[-1] if self._history else None

    def record(
        self,
        path: Path,
        old_content: str | None,
        new_content: str,
        tool_name: str,
        is_new_file: bool = False,
    ) -> None:
        """Record a file change for potential undo."""
        change = FileChange(
            path=path.resolve(),
            old_content=old_content,
            new_content=new_content,
            tool_name=tool_name,
            is_new_file=is_new_file,
        )
        self._history.append(change)

        # Keep history bounded
        if len(self._history) > MAX_UNDO_HISTORY:
            self._history = self._history[-MAX_UNDO_HISTORY:]

    def undo_last(self) -> tuple[bool, str]:
        """Undo the most recent file change. Returns (success, message)."""
        if not self._history:
            return False, "Nothing to undo"

        change = self._history.pop()

        try:
            if change.is_new_file:
                # File was created - delete it
                if change.path.exists():
                    change.path.unlink()
                    return True, f"Deleted {change.path} (undid file creation)"
                else:
                    return False, f"File already removed: {change.path}"
            else:
                # File was modified - restore old content
                if change.old_content is not None:
                    change.path.write_text(change.old_content, encoding="utf-8")
                    return True, f"Restored {change.path} to previous state"
                else:
                    return False, f"No previous content to restore for {change.path}"
        except OSError as e:
            # Push it back since undo failed
            self._history.append(change)
            return False, f"Failed to undo: {e}"

    def list_recent(self, count: int = 10) -> list[FileChange]:
        """Return the most recent N changes (newest first)."""
        return list(reversed(self._history[-count:]))

    def clear(self) -> None:
        """Clear all undo history."""
        self._history.clear()
