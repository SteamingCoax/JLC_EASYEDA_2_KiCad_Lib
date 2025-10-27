# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main_qt.py'],
    pathex=['/Users/robertcecere/Desktop/Code/JLC2Kicad/.venv/lib/python3.14/site-packages'],
    binaries=[],
    datas=[
        ('/Users/robertcecere/Desktop/Code/JLC2Kicad/.venv/lib/python3.14/site-packages/JLC_EASYEDA_2_KICAD_LIB', 'JLC_EASYEDA_2_KICAD_LIB'),
        ('/Users/robertcecere/Desktop/Code/JLC2Kicad/.venv/lib/python3.14/site-packages/KicadModTree', 'KicadModTree'),
    ],
    hiddenimports=['JLC_EASYEDA_2_KICAD_LIB', 'KicadModTree'],
    hookspath=['.'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='JLC_EASYEDA_2_KICAD_LIB Converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='JLC_EASYEDA_2_KICAD_LIB Converter',
)