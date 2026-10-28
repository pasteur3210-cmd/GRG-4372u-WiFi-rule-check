# -*- mode: python ; coding: utf-8 -*-
a = Analysis(['src/main.py'], pathex=['src'], binaries=[], datas=[], hiddenimports=[], hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='ShippingDataValidation_V1.0.0', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False)
