# -*- mode: python ; coding: utf-8 -*-
import sys 

def get_libs(module_name, pristine=None, sieve=True):
    """Track new modules which were imported
    :param module_name: name of the module
    :param pristine: list of modules previously loaded. By default, use all newly loaded
    :param sieve: set to a string to sieve out on that string, module_name by default
    :return: list of newly loaded modules
    """
    if pristine is None:
        pristine = list(sys.modules.keys())
    __import__(module_name)
    new = [i for i in sys.modules if i not in pristine]
    if sieve:
        if isinstance(sieve, str):
            module = sieve
        else:
            module = module_name
        new = [i for i in new if i.startswith(module)]
    return new

fabio_hiddenimports = get_libs("fabio")

a = Analysis(
    ['eiger2xdi_converter.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=fabio_hiddenimports,
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
    [],
    exclude_binaries=True,
    name='eiger2xdi_converter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='eiger2xdi_converter',
)
