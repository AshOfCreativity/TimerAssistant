# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['timer_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'command_interpreter', 
        'timer_manager',
        'tkinter',
        'tkinter.ttk',
        'word2number',
        're',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    target_platform='win32'  # Force Windows target
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
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
    version='windows_build/file_version_info.txt',
    icon='generated-icon.png',
    onefile=True,  # Pack everything into a single EXE
    uac_admin=True,  # Request admin rights when needed
    uac_uiaccess=False,
)