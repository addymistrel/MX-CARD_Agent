from pathlib import Path
from typing import Any

from platformdirs import user_config_dir, user_data_dir
import tomli

from config.config import Config
from constants.app import (
    APP_DIR_NAME,
    CONFIG_FILE_NAME,
    AGENT_MD_FILE,
    APP_PROJECT_DIR,
    DEFAULT_SYSTEM_CONFIG,
    DEFAULT_PROJECT_CONFIG,
)
from utils.errors import ConfigError
import logging

logger = logging.getLogger(__name__)


def get_config_dir() -> Path:
    return Path(user_config_dir(APP_DIR_NAME))


def get_data_dir() -> Path:
    return Path(user_data_dir(APP_DIR_NAME))


def get_system_config_path() -> Path:
    return get_config_dir() / CONFIG_FILE_NAME


def _ensure_system_config() -> None:
    """Create the global config.toml on first run if it doesn't exist."""
    config_dir = get_config_dir()
    config_path = get_system_config_path()

    if config_path.exists():
        return

    try:
        config_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_SYSTEM_CONFIG, encoding="utf-8")
        logger.info(f"Created system config: {config_path}")
    except OSError as e:
        # Non-fatal: the app can still run with defaults.
        logger.warning(f"Could not create system config file: {e}")


def _ensure_project_config(cwd: Path) -> None:
    """Create <cwd>/.mx-card-agent/config.toml if it doesn't exist."""
    agent_dir = cwd.resolve() / APP_PROJECT_DIR
    config_path = agent_dir / CONFIG_FILE_NAME

    if config_path.exists():
        return

    try:
        agent_dir.mkdir(parents=True, exist_ok=True)
        config_path.write_text(DEFAULT_PROJECT_CONFIG, encoding="utf-8")
        logger.info(f"Created project config: {config_path}")
    except OSError as e:
        logger.warning(f"Could not create project config file: {e}")

    _ensure_gitignore(cwd)


def _ensure_gitignore(cwd: Path) -> None:
    """Ensure APP_PROJECT_DIR is listed in the .gitignore at cwd."""
    gitignore_path = cwd.resolve() / ".gitignore"
    entry = APP_PROJECT_DIR

    try:
        if gitignore_path.is_file():
            content = gitignore_path.read_text(encoding="utf-8")
            # Already present — nothing to do
            for line in content.splitlines():
                if line.strip() == entry or line.strip() == f"{entry}/":
                    return
            # Append with a leading newline to be safe
            separator = "" if content.endswith("\n") else "\n"
            gitignore_path.write_text(
                f"{content}{separator}\n# MX-CARD Agent local config\n{entry}/\n",
                encoding="utf-8",
            )
        else:
            gitignore_path.write_text(
                f"# MX-CARD Agent local config\n{entry}/\n",
                encoding="utf-8",
            )
        logger.info(f"Added {entry}/ to {gitignore_path}")
    except OSError as e:
        logger.warning(f"Could not update .gitignore: {e}")


def _parse_toml(path: Path):
    try:
        with open(path, "rb") as f:
            return tomli.load(f)
    except tomli.TOMLDecodeError as e:
        raise ConfigError(f"Invalid TOML in {path}: {e}", config_file=str(path)) from e
    except (OSError, IOError) as e:
        raise ConfigError(
            f"Failed to read config file {path}: {e}", config_file=str(path)
        ) from e


def _get_project_config(cwd: Path) -> Path | None:
    current = cwd.resolve()
    agent_dir = current / APP_PROJECT_DIR

    if agent_dir.is_dir():
        config_file = agent_dir / CONFIG_FILE_NAME
        if config_file.is_file():
            return config_file

    return None


def _get_agent_md_files(cwd: Path) -> str | None:
    current = cwd.resolve()

    if current.is_dir():
        agent_md_file = current / AGENT_MD_FILE
        if agent_md_file.is_file():
            content = agent_md_file.read_text(encoding="utf-8")
            return content

    return None


def _merge_dicts(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value

    return result


def load_config(cwd: Path | None) -> Config:
    cwd = cwd or Path.cwd()

    # System config is global and applies to all projects.
    _ensure_system_config()

    # Per-project config: auto-create .mx-card-agent/config.toml if missing.
    _ensure_project_config(cwd)

    system_path = get_system_config_path()

    config_dict: dict[str, Any] = {}

    if system_path.is_file():
        try:
            config_dict = _parse_toml(system_path)
        except ConfigError:
            logger.warning(f"Skipping invalid system config: {system_path}")

    # Per-project config: if <cwd>/.mx-card-agent/config.toml exists, merge it
    # on top of the system config. Project settings override global ones.
    project_path = _get_project_config(cwd)
    if project_path:
        try:
            project_config_dict = _parse_toml(project_path)
            config_dict = _merge_dicts(config_dict, project_config_dict)
            logger.info(f"Loaded project config: {project_path}")
        except ConfigError:
            logger.warning(f"Skipping invalid project config: {project_path}")

    if "cwd" not in config_dict:
        config_dict["cwd"] = cwd

    if "developer_instructions" not in config_dict:
        agent_md_content = _get_agent_md_files(cwd)
        if agent_md_content:
            config_dict["developer_instructions"] = agent_md_content

    try:
        config = Config(**config_dict)
    except Exception as e:
        raise ConfigError(f"Invalid configuration: {e}") from e

    return config
