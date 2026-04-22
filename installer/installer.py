"""
MX-CARD Agent - Installer / Uninstaller
Builds into a standalone .exe via PyInstaller.

When run normally   → installs mxcagent.exe + adds to PATH
When run with --uninstall → fully removes everything
"""

import base64
import ctypes
import hashlib
import os
import shutil
import subprocess
import sys
import winreg
import time

# ── Constants ────────────────────────────────────────────────────────────────

APP_NAME = "MXCardAgent"
EXE_NAME = "mxcagent.exe"
INSTALLER_NAME = "mxcagent-installer.exe"
UNINSTALLER_NAME = "uninstall.exe"
INSTALL_DIR = os.path.join(os.environ["LOCALAPPDATA"], APP_NAME)
REG_KEY = r"Software\Microsoft\Windows\CurrentVersion\Uninstall\MXCardAgent"

# Must match the key in main.py
_ENC_KEY = b"MxC4rd@g3nt!2026#SecureK3y$"


# ── Encryption helpers (same as main.py) ─────────────────────────────────────

def _derive_key(key: bytes, length: int) -> bytes:
    result = b""
    counter = 0
    while len(result) < length:
        result += hashlib.sha256(key + counter.to_bytes(4, "big")).digest()
        counter += 1
    return result[:length]


def _encrypt_bytes(data: bytes) -> bytes:
    key_stream = _derive_key(_ENC_KEY, len(data))
    encrypted = bytes(a ^ b for a, b in zip(data, key_stream))
    return base64.b64encode(encrypted)


def is_admin():
    """Check if running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def get_user_path():
    """Read the current user PATH from the registry."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, "Path")
            return value
    except FileNotFoundError:
        return ""


def set_user_path(new_path):
    """Write the user PATH to the registry."""
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
    # Broadcast WM_SETTINGCHANGE
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", SMTO_ABORTIFHUNG, 5000, ctypes.byref(ctypes.c_ulong())
    )


def add_to_path():
    """Add INSTALL_DIR to user PATH if not already there."""
    current = get_user_path()
    dirs = [d.strip() for d in current.split(";") if d.strip()]
    for d in dirs:
        if os.path.normcase(d) == os.path.normcase(INSTALL_DIR):
            print("  Already in PATH.")
            return
    dirs.append(INSTALL_DIR)
    set_user_path(";".join(dirs))
    print(f"  Added {INSTALL_DIR} to user PATH.")


def remove_from_path():
    """Remove INSTALL_DIR from user PATH."""
    current = get_user_path()
    dirs = [d.strip() for d in current.split(";") if d.strip()]
    norm_install = os.path.normcase(INSTALL_DIR)
    new_dirs = [d for d in dirs if os.path.normcase(d) != norm_install]
    if len(new_dirs) != len(dirs):
        set_user_path(";".join(new_dirs))
        print("  Removed from PATH.")
    else:
        print("  Was not in PATH.")


def add_uninstall_registry():
    """Add entry to Windows 'Apps & Features' / 'Add or Remove Programs'."""
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_KEY) as key:
            uninstall_exe = os.path.join(INSTALL_DIR, UNINSTALLER_NAME)
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "MX-CARD Agent")
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstall_exe}"')
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, os.path.join(INSTALL_DIR, EXE_NAME))
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "MX-CARD")
            winreg.SetValueEx(key, "InstallLocation", 0, winreg.REG_SZ, INSTALL_DIR)
            winreg.SetValueEx(key, "NoModify", 0, winreg.REG_DWORD, 1)
            winreg.SetValueEx(key, "NoRepair", 0, winreg.REG_DWORD, 1)
        print("  Registered in Apps & Features.")
    except Exception as e:
        print(f"  Warning: Could not add registry entry: {e}")


def remove_uninstall_registry():
    """Remove entry from Windows 'Apps & Features'."""
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, REG_KEY)
        print("  Removed from Apps & Features.")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"  Warning: Could not remove registry entry: {e}")


def get_bundled_exe_path():
    """Get the path to the bundled mxcardagent.exe inside the installer."""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "mxcardagent.exe")  # type: ignore[attr-defined]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "dist", "mxcardagent.exe")


def get_bundled_env_path():
    """Get the path to the bundled .env inside the installer."""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, ".env")  # type: ignore[attr-defined]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, "..", ".env")


# ── Install ──────────────────────────────────────────────────────────────────

def do_install():
    print()
    print("=" * 60)
    print("  MX-CARD Agent - Installer")
    print("=" * 60)
    print()

    # 1. Check bundled exe
    src_exe = get_bundled_exe_path()
    if not os.path.isfile(src_exe):
        print("[ERROR] Bundled mxcardagent.exe not found!")
        print(f"        Expected at: {src_exe}")
        input("\nPress Enter to exit...")
        sys.exit(1)

    # 2. Create install directory
    print("[1/5] Creating install directory...")
    os.makedirs(INSTALL_DIR, exist_ok=True)
    print(f"  {INSTALL_DIR}")
    print()

    # 3. Copy main exe
    print("[2/6] Installing mxcagent.exe...")
    dest_exe = os.path.join(INSTALL_DIR, EXE_NAME)
    shutil.copy2(src_exe, dest_exe)
    size_mb = os.path.getsize(dest_exe) / (1024 * 1024)
    print(f"  Copied ({size_mb:.1f} MB)")
    print()

    # 4. Encrypt .env and store as .env.enc
    print("[3/6] Encrypting API keys...")
    env_src = get_bundled_env_path()
    env_enc_dest = os.path.join(INSTALL_DIR, ".env.enc")
    if os.path.isfile(env_src):
        plain = open(env_src, "rb").read()
        encrypted = _encrypt_bytes(plain)
        with open(env_enc_dest, "wb") as f:
            f.write(encrypted)
        print("  Stored encrypted .env.enc")
        # Never leave plain-text .env in install dir
        plain_env = os.path.join(INSTALL_DIR, ".env")
        if os.path.isfile(plain_env):
            os.remove(plain_env)
    else:
        print("  WARNING: .env not found - no API keys stored!")
    print()

    # 5. Copy self as uninstaller
    print("[4/6] Creating uninstaller...")
    if getattr(sys, "frozen", False):
        self_exe = sys.executable
        uninstall_dest = os.path.join(INSTALL_DIR, UNINSTALLER_NAME)
        shutil.copy2(self_exe, uninstall_dest)
        print(f"  Created {UNINSTALLER_NAME}")
    else:
        print("  Skipped (dev mode)")
    print()

    # 6. Add to PATH
    print("[5/6] Adding to PATH...")
    add_to_path()
    print()

    # 7. Register in Apps & Features
    print("[6/6] Registering application...")
    add_uninstall_registry()
    print()

    # Done
    print("=" * 60)
    print()
    print("  mxcagent has been successfully installed!")
    print()
    print("  You can now run it from anywhere using:")
    print()
    print("      mxcagent")
    print()
    print(f"  Install location:")
    print(f"      {INSTALL_DIR}")
    print()
    print("  To uninstall:")
    print(f"      Run {INSTALL_DIR}\\{UNINSTALLER_NAME}")
    print("      Or use 'Apps & Features' in Windows Settings")
    print()
    print("  NOTE: Open a NEW terminal for PATH changes to take")
    print("        effect.")
    print()
    print("=" * 60)
    print()
    input("Press Enter to exit...")


# ── Uninstall ────────────────────────────────────────────────────────────────

def do_uninstall():
    print()
    print("=" * 60)
    print("  MX-CARD Agent - Uninstaller")
    print("=" * 60)
    print()
    print("  This will completely remove MX-CARD Agent from your")
    print("  system.")
    print()

    confirm = input("  Are you sure? [Y/N]: ").strip()
    if confirm.upper() != "Y":
        print("\n  Uninstall cancelled.")
        input("\n  Press Enter to exit...")
        sys.exit(0)

    print()

    # 1. Remove from PATH
    print("[1/3] Removing from PATH...")
    remove_from_path()
    print()

    # 2. Remove registry entry
    print("[2/3] Removing from Apps & Features...")
    remove_uninstall_registry()
    print()

    # 3. Delete files (schedule self-deletion)
    print("[3/3] Removing files...")
    exe_path = os.path.join(INSTALL_DIR, EXE_NAME)
    if os.path.isfile(exe_path):
        try:
            os.remove(exe_path)
            print(f"  Deleted {EXE_NAME}")
        except Exception:
            print(f"  Will delete {EXE_NAME} on cleanup")

    print()
    print("=" * 60)
    print()
    print("  MX-CARD Agent has been completely uninstalled.")
    print()
    print("=" * 60)
    print()
    input("Press Enter to exit...")

    # Self-delete: spawn a background process to remove the install dir
    # after this process exits
    cleanup_cmd = f'ping -n 3 127.0.0.1 >nul & rmdir /s /q "{INSTALL_DIR}"'
    subprocess.Popen(
        cleanup_cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=0x00000008,  # DETACHED_PROCESS
    )


# ── Entry point ──────────────────────────────────────────────────────────────

def main():
    # Determine mode based on exe name or flag
    exe_name = os.path.basename(sys.executable).lower() if getattr(sys, "frozen", False) else ""
    is_uninstall = (
        "--uninstall" in sys.argv
        or exe_name == UNINSTALLER_NAME.lower()
    )

    if is_uninstall:
        do_uninstall()
    else:
        do_install()


if __name__ == "__main__":
    main()
