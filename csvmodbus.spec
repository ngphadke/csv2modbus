# -*- mode: python -*-

block_cipher = None


a = Analysis(['csv2modbus_singlefile.py'],
             pathex=['D:\\Coding\\Current\\csv2modbus'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='csvmodbus',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='csv2modbus.ico')
