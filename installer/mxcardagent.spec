# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for mxcardagent.exe — single self-contained exe.

Bundles EVERYTHING:
  - main.py + all source modules
  - All pip dependencies (openai, rich, click, tiktoken, etc.)
  - .env file (API key & base URL baked in)

No installer needed. No Python needed on target. Just run it.

Build:
  cd installer
  build.bat
"""

import os
from pathlib import Path
from PyInstaller.utils.hooks import copy_metadata

block_cipher = None

# Project root is one level up from installer/
PROJECT_ROOT = os.path.abspath(os.path.join(SPECPATH, '..'))

# ── Collect all project source as datas ──────────────────────────────────────
# We add the project source dirs so that relative imports like
# `from agent.agent import Agent` work inside the frozen bundle.

SOURCE_DIRS = [
    'agent',
    'client',
    'config',
    'constants',
    'context',
    'hooks',
    'prompts',
    'safety',
    'tools',
    'ui',
    'utils',
]

datas = []

for dirname in SOURCE_DIRS:
    src_path = os.path.join(PROJECT_ROOT, dirname)
    if os.path.isdir(src_path):
        datas.append((src_path, dirname))

# Bundle .env (API key + base URL)
dotenv = os.path.join(PROJECT_ROOT, '.env')
if os.path.isfile(dotenv):
    datas.append((dotenv, '.'))
else:
    print("WARNING: .env file not found at project root!")
    print("         The exe will not have API keys baked in.")

# ── Package metadata (for importlib.metadata.version() calls) ───────────────
# Some libs (fastmcp, mcp, openai, etc.) call importlib.metadata.version()
# at import time.  PyInstaller strips dist-info by default, so we need to
# re-include it for the packages that need it.
METADATA_PACKAGES = [
    'fastmcp', 'mcp', 'openai', 'tiktoken', 'httpx', 'rich', 'click',
    'pydantic', 'pydantic_core', 'platformdirs', 'tomli', 'ddgs',
    'pyperclip', 'anyio', 'sniffio', 'httpcore', 'colorama', 'pygments',
    'python-dotenv', 'certifi', 'httpx', 'h11', 'idna',
    'starlette', 'uvicorn', 'sse-starlette', 'pydantic-settings',
]
for pkg in METADATA_PACKAGES:
    try:
        datas += copy_metadata(pkg)
    except Exception:
        pass  # package not installed or no metadata — skip

# ── Hidden imports ───────────────────────────────────────────────────────────
# PyInstaller can't always detect dynamic imports. List them explicitly.

hiddenimports = [
    # Our own packages
    'agent', 'agent.agent', 'agent.events', 'agent.persistence', 'agent.session',
    'client', 'client.llm_client', 'client.response',
    'config', 'config.config', 'config.loader',
    'constants', 'constants.__init__', 'constants.agent', 'constants.app',
    'constants.models', 'constants.safety', 'constants.tools', 'constants.ui',
    'context', 'context.compaction', 'context.loop_detector', 'context.manager',
    'hooks', 'hooks.hook_system',
    'prompts', 'prompts.system',
    'safety', 'safety.approval',
    'tools', 'tools.base', 'tools.discovery', 'tools.registry', 'tools.subagents',
    'tools.builtin', 'tools.builtin.__init__',
    'tools.builtin.edit_file', 'tools.builtin.glob', 'tools.builtin.grep',
    'tools.builtin.list_dir', 'tools.builtin.memory', 'tools.builtin.read_file',
    'tools.builtin.shell', 'tools.builtin.todo', 'tools.builtin.web_fetch',
    'tools.builtin.web_search', 'tools.builtin.write_file',
    'tools.mcp', 'tools.mcp.client', 'tools.mcp.mcp_manager', 'tools.mcp.mcp_tool',
    'ui', 'ui.tui',
    'utils', 'utils.errors', 'utils.paths', 'utils.text', 'utils.undo',

    # Third-party deps that PyInstaller may miss
    'click',
    'dotenv',
    'openai',
    'httpx',
    'rich',
    'rich.console',
    'rich.markup',
    'rich.text',
    'pydantic',
    'pydantic_core',
    'tiktoken',
    'tiktoken_ext',
    'tiktoken_ext.openai_public',
    'platformdirs',
    'tomli',
    'ddgs',
    'pyperclip',
    'fastmcp',
    'mcp',
    'anyio',
    'sniffio',
    'httpcore',
    'colorama',
    'pygments',
]

# ── Collect mypyc-compiled binaries ──────────────────────────────────────────
# Some deps (e.g. tomli, black) ship mypyc-compiled .pyd files at top-level
# of site-packages.  PyInstaller misses them because they're not normal packages.
import glob as _glob
import sys as _sys

_site_packages = Path(_sys.prefix) / 'Lib' / 'site-packages'
_mypyc_binaries = []
for pyd in _glob.glob(str(_site_packages / '*__mypyc*.pyd')):
    _mypyc_binaries.append((pyd, '.'))

# ── Analysis ─────────────────────────────────────────────────────────────────

a = Analysis(
    [os.path.join(PROJECT_ROOT, 'main.py')],
    pathex=[PROJECT_ROOT],
    binaries=_mypyc_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', '_tkinter',
        'matplotlib', 'numpy', 'pandas', 'scipy',
        'PIL', 'cv2',
        'unittest', 'test',
        'xmlrpc', 'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='mxcardagent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
    version=None,
    onefile=True,
)
