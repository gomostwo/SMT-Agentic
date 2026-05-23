# PyInstaller spec — builds a portable no-console smt_agent.exe
# Build:   pyinstaller smt_agent.spec --clean

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs

block_cipher = None
binaries = collect_dynamic_libs("win32")

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=collect_data_files("pywinauto"),
    hiddenimports=[
        # pywinauto
        "pywinauto",
        "pywinauto.application",
        "pywinauto.controls",
        "pywinauto.controls.uia_controls",
        "pywinauto.uia_defines",
        "pywinauto.uia_element_info",
        "pywinauto.keyboard",
        # pywin32
        "win32api",
        "win32con",
        "win32gui",
        "win32process",
        "pywintypes",
        # COM
        "comtypes",
        "comtypes.client",
        # keyring (Windows Credential Manager backend)
        "keyring",
        "keyring.backends",
        "keyring.backends.Windows",
        # tkinter (config dialog)
        "tkinter",
        "tkinter.ttk",
        "tkinter.filedialog",
        "tkinter.messagebox",
    ],
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
    name="smt_agent",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
