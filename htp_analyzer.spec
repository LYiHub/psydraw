# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['htp_analyzer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('src', 'src')
    ],
    hiddenimports=['pydantic.deprecated.decorator', 'langchain_openai', 'langchain', 'langchain_core'],
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
    [],
    exclude_binaries=True,
    name='htp_analyzer',
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
    icon="assets/logo2.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='htp_analyzer',
)
app = BUNDLE(
    coll,
    name='htp_analyzer',
    icon="assets/logo2.ico",
    bundle_identifier='com.linyihub.htpanalyzer',
)
