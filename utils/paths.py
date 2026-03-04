from pathlib import Path


class PathTraversalError(ValueError):
    """Raised when a resolved path escapes the allowed working directory."""
    pass


def resolve_path(base: str | Path, path: str | Path, allow_absolute: bool = False):
    base = Path(base).resolve()
    path = Path(path)

    if path.is_absolute():
        resolved = path.resolve()
    else:
        resolved = (base / path).resolve()

    if not allow_absolute and not resolved.is_relative_to(base):
        raise PathTraversalError(
            f"Path '{path}' resolves to '{resolved}' which is outside the working directory '{base}'"
        )

    return resolved


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
