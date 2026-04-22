# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for the MX-CARD Agent INSTALLER exe.

Bundles:
  - installer.py (install/uninstall logic)
  - mxcardagent.exe (the actual agent, embedded as a data file)

Output: mxcagent-installer.exe
"""

import os

block_cipher = None
SPEC_DIR = os.path.abspath(SPECPATH)
PROJECT_ROOT = os.path.abspath(os.path.join(SPEC_DIR, '..'))
AGENT_EXE = os.path.join(SPEC_DIR, 'dist', 'mxcardagent.exe')
DOT_ENV = os.path.join(PROJECT_ROOT, '.env')

if not os.path.isfile(AGENT_EXE):
    raise FileNotFoundError(
        f"mxcardagent.exe not found at {AGENT_EXE}\n"
        "Build the agent first (build.bat step 1)."
    )

if not os.path.isfile(DOT_ENV):
    print(f"WARNING: .env not found at {DOT_ENV}")
    print("         The installer will not have API keys to encrypt.")

_datas = [(AGENT_EXE, '.')]
if os.path.isfile(DOT_ENV):
    _datas.append((DOT_ENV, '.'))

a = Analysis(
    [os.path.join(SPEC_DIR, 'installer.py')],
    pathex=[SPEC_DIR],
    binaries=[],
    datas=_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', '_tkinter', 'matplotlib', 'numpy', 'pandas',
        'scipy', 'PIL', 'cv2', 'unittest', 'test',
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
    name='mxcagent-installer',
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
    uac_admin=False,
)
