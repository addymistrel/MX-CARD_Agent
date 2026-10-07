from __future__ import annotations

import json
import os
import threading
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

SESSION_TIMEOUT_SECONDS = 30 * 60
SESSION_DIR = Path.home() / ".mx-card-agent"
SESSION_FILE = SESSION_DIR / "session.json"
DEFAULT_AUTH_URL = os.getenv("MX_CARD_SIGN_IN_URL") or os.getenv("MX_CARD_APP_URL", "")
DEFAULT_AUTH_URL = (
    DEFAULT_AUTH_URL.rstrip("/") + "/auth"
    if DEFAULT_AUTH_URL and not DEFAULT_AUTH_URL.endswith("/auth")
    else (DEFAULT_AUTH_URL or "http://localhost:5173/auth")
)


class AgentAuthManager:
    def __init__(
        self,
        state_path: Path | None = None,
        session_timeout_seconds: int = SESSION_TIMEOUT_SECONDS,
        sign_in_url: str = DEFAULT_AUTH_URL,
    ) -> None:
        self.state_path = state_path or SESSION_FILE
        self.session_timeout_seconds = session_timeout_seconds
        self.sign_in_url = sign_in_url
        self._lock = threading.Lock()
        self._callback_server: ThreadingHTTPServer | None = None
        self._server_thread: threading.Thread | None = None
        self._auth_event: threading.Event = threading.Event()

    def _default_state(self) -> dict[str, Any]:
        return {
            "authenticated": False,
            "user": None,
            "logged_in_at": None,
            "expires_at": None,
        }

    def _ensure_state_file(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_state(self) -> dict[str, Any]:
        self._ensure_state_file()
        if not self.state_path.exists():
            return self._default_state()

        try:
            with self.state_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (json.JSONDecodeError, OSError):
            return self._default_state()

        state = self._default_state()
        state.update(data)
        return state

    def _write_state(self, state: dict[str, Any]) -> None:
        self._ensure_state_file()
        with self.state_path.open("w", encoding="utf-8") as handle:
            json.dump(state, handle, indent=2)

    def is_logged_in(self) -> bool:
        state = self._read_state()
        authenticated = bool(state.get("authenticated"))
        expires_at = state.get("expires_at")

        if not authenticated:
            return False

        if expires_at is None:
            self.logout()
            return False

        if float(expires_at) <= time.time():
            self.logout()
            return False

        return True

    def logout(self) -> None:
        with self._lock:
            self._write_state(self._default_state())

    def _record_success(self, user: str | None = None) -> None:
        expires_at = time.time() + self.session_timeout_seconds
        state = {
            "authenticated": True,
            "user": user or "local-user",
            "logged_in_at": time.time(),
            "expires_at": expires_at,
        }
        self._write_state(state)

    def start_sign_in_flow(self, console: Any | None = None) -> bool:
        self.logout()
        self._auth_event.clear()

        callback_url = self._start_callback_server()
        final_url = self._build_sign_in_url(callback_url)

        if console is not None:
            console.print("\n[bold yellow]Authentication required.[/bold yellow]")
            console.print(f"Open this URL to sign in: [cyan]{final_url}[/cyan]")
            console.print(
                "[dim]The terminal will resume after the callback completes.[/dim]"
            )

        try:
            webbrowser.open(final_url)
        except Exception:
            pass

        if not self._wait_for_callback(timeout_seconds=180):
            self.logout()
            if console is not None:
                console.print("[yellow]Sign-in was not completed in time. Continuing without the session.[/yellow]")
            return False

        if console is not None:
            console.print("[green]Sign in successful.[/green]")
        return True


    def ensure_logged_in(self, console: Any | None = None) -> bool:
        if self.is_logged_in():
            return True

        return self.start_sign_in_flow(console)

    def _build_sign_in_url(self, callback_url: str) -> str:
        params = urllib.parse.urlencode({"callback": callback_url})
        return f"{self.sign_in_url}?{params}"

    def _start_callback_server(self) -> str:
        if self._callback_server is not None:
            try:
                self._callback_server.shutdown()
            except Exception:
                pass
            self._callback_server.server_close()
            self._callback_server = None

        port = self._find_free_port()
        self._callback_server = ThreadingHTTPServer(("127.0.0.1", port), self._build_handler())
        self._server_thread = threading.Thread(target=self._callback_server.serve_forever, daemon=True)
        self._server_thread.start()
        return f"http://127.0.0.1:{port}/auth/callback"

    def _wait_for_callback(self, timeout_seconds: int) -> bool:
        """Block until the auth callback fires (via in-memory event) or timeout."""
        signalled = self._auth_event.wait(timeout=timeout_seconds)
        return signalled and self.is_logged_in()

    def _build_handler(self):
        auth_manager = self

        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path != "/auth/callback":
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not found")
                    return

                params = urllib.parse.parse_qs(parsed.query)
                status = (params.get("status", ["failed"])[0] or "failed").strip().lower()
                user = params.get("email", ["local-user"])[0] or "local-user"

                if status == "success":
                    auth_manager._record_success(user)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"Sign in successful. You can return to the terminal.")
                else:
                    auth_manager.logout()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(b"Sign in failed. You can continue working in the terminal.")

                # Unblock _wait_for_callback regardless of success/failure
                auth_manager._auth_event.set()

                try:
                    if auth_manager._callback_server is not None:
                        auth_manager._callback_server.shutdown()
                        auth_manager._callback_server.server_close()
                        auth_manager._callback_server = None
                except Exception:
                    pass


            def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
                return

        return CallbackHandler

    @staticmethod
    def _find_free_port() -> int:
        import socket

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
            return int(sock.getsockname()[1])
