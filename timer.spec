# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Adjust Sox path for Windows
sox_binary = 'C:/Program Files (x86)/sox-14.4.2/sox.exe'

a = Analysis(
    ['timer_app.py'],
    pathex=[],
    binaries=[
        (sox_binary, '.'),  # Bundle Sox executable
        ('C:/Program Files (x86)/sox-14.4.2/libgcc_s_dw2-1.dll', '.'),  # Required Sox DLLs
        ('C:/Program Files (x86)/sox-14.4.2/libwinpthread-1.dll', '.'),
        ('C:/Program Files (x86)/sox-14.4.2/libgomp-1.dll', '.'),
    ],
    datas=[],
    hiddenimports=['tkinter', 'word2number'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    icon='generated-icon.png',
    version='file_version_info.txt'
)