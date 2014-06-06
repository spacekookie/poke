# -*- mode: python -*-
a = Analysis(['source/Controllers.py', 'source/IOHandle.py', 'source/Intro.py', 'source/Poke.py', 'source/Strings.py'],
             pathex=['/Users/spacekookie/Documents/Projects/Python/Poke'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='poke',
          debug=False,
          strip=None,
          upx=True,
          console=True )
