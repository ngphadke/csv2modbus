# -*- mode: python -*-

block_cipher = None


a = Analysis(['csv2modbus_singlefile.py'],
             pathex=['C:\\Python27', 'D:\\Coding\\tmp\\bestpaper'],
             binaries=None,
             datas=None,
             hiddenimports=['cryptography.hazmat.backends.openssl'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='csv2modbus_singlefile',
          debug=True,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='csv2modbus_singlefile')
