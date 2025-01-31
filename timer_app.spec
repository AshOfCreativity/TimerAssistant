# -*- mode: python ; coding: utf-8 -*-
import os.path

# Define paths
WINDOWS_BUILD_DIR = 'windows_build'
VERSION_FILE = os.path.join(WINDOWS_BUILD_DIR, 'file_version_info.txt')
ICON_FILE = 'generated-icon.png'

a = Analysis(
    ['timer_app.py'],
    pathex=[],
    binaries=[],
    datas=[(ICON_FILE, '.')],
    hiddenimports=[
        'tkinter',
        'command_interpreter',
        'timer_manager'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TimerAssistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version=VERSION_FILE,
    icon=ICON_FILE,
    uac_admin=False,
    uac_uiaccess=False
)