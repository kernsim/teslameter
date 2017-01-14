# -*- mode: python -*-

block_cipher = None


a = Analysis(['teslameter\\teslameter.py'],
             pathex=['C:\\Users\\Simon\\Documents\\Python Scripts\\teslameter'],
             binaries=None,
             datas=(('teslameter\Icons8-Windows-8-Science-Scale.ico', '.'), ) ,
             hiddenimports=[],
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
          name='teslameter',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='teslameter\\Icons8-Windows-8-Science-Scale.ico')
