import asyncio
import os
from pathlib import Path
import sys
import click
from dotenv import load_dotenv

# When running from a PyInstaller bundle, files are extracted to sys._MEIPASS.
# When running as a normal script, use the script's own directory.
if getattr(sys, "frozen", False):
    _app_dir = Path(sys._MEIPASS)  # type: ignore[attr-defined]
else:
    _app_dir = Path(__file__).resolve().parent

# Load .env from the bundled/app directory first,
# then from the user's cwd (so user can override if needed).
load_dotenv(_app_dir / ".env")
load_dotenv()


def _ensure_on_path() -> None:
    """On first run of the frozen exe, offer to add its directory to the user PATH."""
    if not getattr(sys, "frozen", False) or sys.platform != "win32":
        return

    exe_dir = str(Path(sys.executable).resolve().parent)

    # Check if already on PATH
    user_path = _get_user_path()
    if user_path is not None:
        dirs = [d.strip().rstrip("\\") for d in user_path.split(";") if d.strip()]
        if exe_dir.rstrip("\\").lower() in [d.lower() for d in dirs]:
            return  # already on PATH

    # Check for a sentinel so we only ask once per location
    sentinel = Path(exe_dir) / ".path_configured"
    if sentinel.exists():
        return

    print(f"\n  The directory containing mxcardagent.exe is not on your PATH.")
    print(f"  Directory: {exe_dir}\n")
    answer = input("  Add it to your PATH so you can run 'mxcardagent' from any terminal? [Y/n] ").strip().lower()

    if answer in ("", "y", "yes"):
        if _add_to_user_path(exe_dir):
            print(f"\n  ✓ Added to PATH. Restart your terminal to use 'mxcardagent' from anywhere.\n")
        else:
            print(f"\n  ✗ Could not update PATH automatically.")
            print(f"    Manually add this directory to your PATH: {exe_dir}\n")
    else:
        print(f"\n  Skipped. You can manually add this directory to your PATH later:")
        print(f"    {exe_dir}\n")

    # Write sentinel so we don't ask again for this location
    try:
        sentinel.write_text("configured")
    except OSError:
        pass


def _get_user_path() -> str | None:
    """Read the current user-level PATH from the Windows registry."""
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
    except (OSError, FileNotFoundError):
        return os.environ.get("PATH", "")


def _add_to_user_path(directory: str) -> bool:
    """Append a directory to the user-level PATH via the Windows registry."""
    try:
        import winreg
        import ctypes

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, r"Environment", 0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        ) as key:
            try:
                current, _ = winreg.QueryValueEx(key, "Path")
            except FileNotFoundError:
                current = ""

            # Don't duplicate
            dirs = [d.strip().rstrip("\\") for d in current.split(";") if d.strip()]
            if directory.rstrip("\\").lower() in [d.lower() for d in dirs]:
                return True

            new_path = current.rstrip(";") + ";" + directory if current else directory
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

        # Broadcast WM_SETTINGCHANGE so new terminals pick it up immediately
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(ctypes.c_ulong(0))
        )
        return True
    except Exception:
        return False

from agent.agent import Agent
from agent.events import AgentEventType
from agent.persistence import PersistenceManager, SessionSnapshot
from agent.session import Session
from config.config import ApprovalPolicy, Config
from config.loader import load_config
from constants.app import APP_NAME
from constants.ui import WELCOME_COMMANDS
from ui.tui import TUI, get_console

console = get_console()


class CLI:
    def __init__(self, config: Config):
        self.agent: Agent | None = None
        self.config = config
        self.tui = TUI(config, console)

    async def run_single(self, message: str) -> str | None:
        async with Agent(self.config) as agent:
            self.agent = agent
            result = await self._process_message(message)
            return result if result is not None else ""

    async def run_interactive(self) -> str | None:
        self.tui.print_welcome(
            APP_NAME,
            lines=[
                f"model: {self.config.model_name}",
                f"cwd: {self.config.cwd}",
                WELCOME_COMMANDS,
            ],
        )

        async with Agent(
            self.config,
            confirmation_callback=self.tui.handle_confirmation,
        ) as agent:
            self.agent = agent

            while True:
                try:
                    user_input = console.input("\n[user]>[/user] ").strip()
                    if not user_input:
                        continue

                    if user_input.startswith("/"):
                        should_continue = await self._handle_command(user_input)
                        if not should_continue:
                            break
                        continue

                    await self._process_message(user_input)
                except KeyboardInterrupt:
                    console.print("\n[dim]Use /exit to quit[/dim]")
                except EOFError:
                    break

        console.print("\n[dim]Goodbye![/dim]")

    def _get_tool_kind(self, tool_name: str) -> str | None:
        if not self.agent:
            return None
        tool = self.agent.session.tool_registry.get(tool_name)
        if not tool:
            return None

        return tool.kind.value

    async def _process_message(self, message: str) -> str | None:
        if not self.agent:
            return None

        assistant_streaming = False
        final_response: str | None = None

        async for event in self.agent.run(message):
            if event.type == AgentEventType.TEXT_DELTA:
                content = event.data.get("content", "")
                if not assistant_streaming:
                    self.tui.begin_assistant()
                    assistant_streaming = True
                self.tui.stream_assistant_delta(content)
            elif event.type == AgentEventType.TEXT_COMPLETE:
                final_response = event.data.get("content")
                if assistant_streaming:
                    self.tui.end_assistant()
                    assistant_streaming = False
            elif event.type == AgentEventType.AGENT_ERROR:
                error = event.data.get("error", "Unknown error")
                console.print(f"\n[error]Error: {error}[/error]")
            elif event.type == AgentEventType.TOOL_CALL_START:
                tool_name = event.data.get("name", "unknown")
                tool_kind = self._get_tool_kind(tool_name)
                self.tui.tool_call_start(
                    event.data.get("call_id", ""),
                    tool_name,
                    tool_kind,
                    event.data.get("arguments", {}),
                )
            elif event.type == AgentEventType.TOOL_CALL_COMPLETE:
                tool_name = event.data.get("name", "unknown")
                tool_kind = self._get_tool_kind(tool_name)
                self.tui.tool_call_complete(
                    event.data.get("call_id", ""),
                    tool_name,
                    tool_kind,
                    event.data.get("success", False),
                    event.data.get("output", ""),
                    event.data.get("error"),
                    event.data.get("metadata"),
                    event.data.get("diff"),
                    event.data.get("truncated", False),
                    event.data.get("exit_code"),
                )

        return final_response

    async def _handle_command(self, command: str) -> bool:
        cmd = command.lower().strip()
        parts = cmd.split(maxsplit=1)
        cmd_name = parts[0]
        cmd_args = parts[1] if len(parts) > 1 else ""
        if cmd_name == "/exit" or cmd_name == "/quit":
            return False
        elif command == "/help":
            self.tui.show_help()
        elif not self.agent:
            console.print("[error]No active agent session[/error]")
        elif command == "/clear":
            ctx = self.agent.session.get_context_manager()
            ctx.clear()
            self.agent.session.loop_detector.clear()
            console.print("[success]Conversation cleared [/success]")
        elif cmd_name == "/undo":
            tracker = self.agent.session.undo_tracker
            if not tracker.has_changes:
                console.print("[warning]Nothing to undo[/warning]")
            else:
                last = tracker.last_change
                if last:
                    console.print(
                        f"\n[bold]Last change:[/bold] {last.summary}"
                    )
                    console.print(f"  Path: {last.display_path}")
                    console.print(
                        f"  Time: {last.timestamp.strftime('%H:%M:%S')}"
                    )
                    response = console.input(
                        "\n[bold]Undo this change? (y/n):[/bold] "
                    ).strip()
                    if response.lower() in {"y", "yes"}:
                        success, message = tracker.undo_last()
                        if success:
                            console.print(f"[success]{message}[/success]")
                        else:
                            console.print(f"[error]{message}[/error]")
                    else:
                        console.print("[dim]Undo cancelled[/dim]")
        elif cmd_name == "/undolist":
            tracker = self.agent.session.undo_tracker
            changes = tracker.list_recent(10)
            if not changes:
                console.print("[dim]No file changes recorded[/dim]")
            else:
                console.print(f"\n[bold]Recent file changes ({len(changes)})[/bold]")
                for i, change in enumerate(changes, 1):
                    action = "Created" if change.is_new_file else "Modified"
                    console.print(
                        f"  {i}. [{change.timestamp.strftime('%H:%M:%S')}] "
                        f"{action} {change.display_path} ({change.tool_name})"
                    )
        elif command == "/config":
            console.print("\n[bold]Current Configuration[/bold]")
            console.print(f"  Model: {self.config.model_name}")
            console.print(f"  Temperature: {self.config.temperature}")
            console.print(f"  Approval: {self.config.approval.value}")
            console.print(f"  Working Dir: {self.config.cwd}")
            console.print(f"  Max Turns: {self.config.max_turns}")
            console.print(f"  Hooks Enabled: {self.config.hooks_enabled}")
        elif cmd_name == "/model":
            if cmd_args:
                self.config.model_name = cmd_args
                console.print(f"[success]Model changed to: {cmd_args} [/success]")
            else:
                console.print(f"Current model: {self.config.model_name}")
        elif cmd_name == "/approval":
            if cmd_args:
                try:
                    approval = ApprovalPolicy(cmd_args)
                    self.config.approval = approval
                    console.print(
                        f"[success]Approval policy changed to: {cmd_args} [/success]"
                    )
                except Exception:
                    console.print(
                        f"[error]Incorrect approval policy: {cmd_args} [/error]"
                    )
                    console.print(
                        f"Valid options: {', '.join(p.value for p in ApprovalPolicy)}"
                    )
            else:
                console.print(f"Current approval policy: {self.config.approval.value}")
        elif cmd_name == "/stats":
            stats = self.agent.session.get_stats()
            console.print("\n[bold]Session Statistics [/bold]")
            for key, value in stats.items():
                console.print(f"   {key}: {value}")
        elif cmd_name == "/tools":
            tools = self.agent.session.tool_registry.get_tools()
            console.print(f"\n[bold]Available tools ({len(tools)}) [/bold]")
            for tool in tools:
                console.print(f"  • {tool.name}")
        elif cmd_name == "/mcp":
            mcp_servers = self.agent.session.mcp_manager.get_all_servers()
            console.print(f"\n[bold]MCP Servers ({len(mcp_servers)}) [/bold]")
            for server in mcp_servers:
                status = server["status"]
                status_color = "green" if status == "connected" else "red"
                console.print(
                    f"  • {server['name']}: [{status_color}]{status}[/{status_color}] ({server['tools']} tools)"
                )
        elif cmd_name == "/save":
            persistence_manager = PersistenceManager()
            ctx = self.agent.session.get_context_manager()
            session_snapshot = SessionSnapshot(
                session_id=self.agent.session.session_id,
                created_at=self.agent.session.created_at,
                updated_at=self.agent.session.updated_at,
                turn_count=self.agent.session.turn_count,
                messages=ctx.get_messages(),
                total_usage=ctx.total_usage,
            )
            persistence_manager.save_session(session_snapshot)
            console.print(
                f"[success]Session saved: {self.agent.session.session_id}[/success]"
            )
        elif cmd_name == "/sessions":
            persistence_manager = PersistenceManager()
            sessions = persistence_manager.list_sessions()
            console.print("\n[bold]Saved Sessions[/bold]")
            for s in sessions:
                console.print(
                    f"  • {s['session_id']} (turns: {s['turn_count']}, updated: {s['updated_at']})"
                )
        elif cmd_name == "/resume":
            if not cmd_args:
                console.print(f"[error]Usage: /resume <session_id> [/error]")
            else:
                persistence_manager = PersistenceManager()
                snapshot = persistence_manager.load_session(cmd_args)
                if not snapshot:
                    console.print(f"[error]Session does not exist [/error]")
                else:
                    session = Session(
                        config=self.config,
                    )
                    await session.initialize()
                    session.session_id = snapshot.session_id
                    session.created_at = snapshot.created_at
                    session.updated_at = snapshot.updated_at
                    session.turn_count = snapshot.turn_count
                    ctx = session.get_context_manager()
                    ctx.total_usage = snapshot.total_usage

                    for msg in snapshot.messages:
                        if msg.get("role") == "system":
                            continue
                        elif msg["role"] == "user":
                            ctx.add_user_message(
                                msg.get("content", "")
                            )
                        elif msg["role"] == "assistant":
                            ctx.add_assistant_message(
                                msg.get("content", ""), msg.get("tool_calls")
                            )
                        elif msg["role"] == "tool":
                            ctx.add_tool_result(
                                msg.get("tool_call_id", ""), msg.get("content", "")
                            )

                    await self.agent.session.client.close()
                    await self.agent.session.mcp_manager.shutdown()

                    self.agent.session = session
                    console.print(
                        f"[success]Resumed session: {session.session_id}[/success]"
                    )
        elif cmd_name == "/checkpoint":
            persistence_manager = PersistenceManager()
            ctx = self.agent.session.get_context_manager()
            session_snapshot = SessionSnapshot(
                session_id=self.agent.session.session_id,
                created_at=self.agent.session.created_at,
                updated_at=self.agent.session.updated_at,
                turn_count=self.agent.session.turn_count,
                messages=ctx.get_messages(),
                total_usage=ctx.total_usage,
            )
            checkpoint_id = persistence_manager.save_checkpoint(session_snapshot)
            console.print(f"[success]Checkpoint created: {checkpoint_id}[/success]")
        elif cmd_name == "/checkpoints":
            persistence_manager = PersistenceManager()
            checkpoints = persistence_manager.list_checkpoints()
            if not checkpoints:
                console.print("[dim]No checkpoints found[/dim]")
            else:
                console.print(f"\n[bold]Checkpoints ({len(checkpoints)})[/bold]")
                for cp in checkpoints:
                    console.print(
                        f"  • {cp['checkpoint_id']}  "
                        f"(turns: {cp['turn_count']}, created: {cp['created_at']})"
                    )
                console.print("\n[dim]Use /restore <checkpoint_id> to restore[/dim]")
        elif cmd_name == "/restore":
            if not cmd_args:
                console.print(f"[error]Usage: /restore <checkpoint_id> [/error]")
            else:
                persistence_manager = PersistenceManager()
                snapshot = persistence_manager.load_checkpoint(cmd_args)
                if not snapshot:
                    console.print(f"[error]Checkpoint does not exist [/error]")
                else:
                    session = Session(
                        config=self.config,
                    )
                    await session.initialize()
                    session.session_id = snapshot.session_id
                    session.created_at = snapshot.created_at
                    session.updated_at = snapshot.updated_at
                    session.turn_count = snapshot.turn_count
                    ctx = session.get_context_manager()
                    ctx.total_usage = snapshot.total_usage

                    for msg in snapshot.messages:
                        if msg.get("role") == "system":
                            continue
                        elif msg["role"] == "user":
                            ctx.add_user_message(
                                msg.get("content", "")
                            )
                        elif msg["role"] == "assistant":
                            ctx.add_assistant_message(
                                msg.get("content", ""), msg.get("tool_calls")
                            )
                        elif msg["role"] == "tool":
                            ctx.add_tool_result(
                                msg.get("tool_call_id", ""), msg.get("content", "")
                            )

                    await self.agent.session.client.close()
                    await self.agent.session.mcp_manager.shutdown()

                    self.agent.session = session
                    console.print(
                        f"[success]Resumed session: {session.session_id}, checkpoint: {cmd_args}[/success]"
                    )
        else:
            console.print(f"[error]Unknown command: {cmd_name}[/error]")

        return True


@click.command()
@click.argument("prompt", required=False)
@click.option(
    "--cwd",
    "-c",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    help="Current working directory",
)
def main(
    prompt: str | None,
    cwd: Path | None,
):
    # On first run of the frozen exe, offer to add to PATH
    _ensure_on_path()

    try:
        try:
            config = load_config(cwd=cwd)
        except Exception as e:
            console.print(f"[error]Configuration Error: {e}[/error]")
            sys.exit(1)

        errors = config.validate()

        if errors:
            for error in errors:
                console.print(f"[error]{error}[/error]")

            sys.exit(1)

        cli = CLI(config)

        # messages = [{"role": "user", "content": prompt}]
        if prompt:
            result = asyncio.run(cli.run_single(prompt))
            if result is None:
                sys.exit(1)
        else:
            asyncio.run(cli.run_interactive())
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted. Goodbye![/dim]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[error]Fatal error: {e}[/error]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        sys.exit(1)


main()
