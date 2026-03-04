from pathlib import Path


class PathTraversalError(ValueError):
    """Raised when a resolved path escapes the allowed working directory."""
    pass


def resolve_path(base: str | Path, path: str | Path):
    """Resolve a path against a base directory. Allows absolute paths for system-wide access."""
    base = Path(base).resolve()
    path = Path(path)

    if path.is_absolute():
        return path.resolve()

    return (base / path).resolve()


def is_within_directory(path: Path, directory: Path) -> bool:
    """Check if a resolved path is within a given directory."""
    try:
        return path.resolve().is_relative_to(directory.resolve())
    except (ValueError, OSError):
        return False


def is_system_drive(path: Path) -> bool:
    """Check if a path is on the system drive (C:\\ on Windows, / system dirs on Unix)."""
    import sys
    resolved = path.resolve()

    if sys.platform == "win32":
        drive = resolved.drive.upper()
        return drive == "C:"
    else:
        system_dirs = ("/bin", "/sbin", "/usr", "/etc", "/boot", "/lib", "/var", "/sys", "/proc")
        return any(str(resolved).startswith(d) for d in system_dirs)


def display_path_rel_to_cwd(path: str, cwd: Path | None) -> str:
    try:
        p = Path(path)
    except Exception:
        return path

    if cwd:
        try:
            return str(p.relative_to(cwd))
        except ValueError:
            pass

    return str(p)


def ensure_parent_directory(path: str | Path) -> Path:
    path = Path(path)

    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def is_binary_file(path: str | Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(8192)
            return b"\x00" in chunk
    except (OSError, IOError):
        return False
