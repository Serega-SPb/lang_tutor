# -*- mode: python ; coding: utf-8 -*-
import os
import shutil

block_cipher = None

shutil.rmtree('dist', ignore_errors=True)

a = Analysis(['launcher.py'],
             pathex=['.'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='launcher',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)


shutil.copyfile('config.yaml', '{0}/config.yaml'.format(DISTPATH))
shutil.copytree('locales', '{0}/locales'.format(DISTPATH))
shutil.copytree('scenarios', '{0}/scenarios'.format(DISTPATH))
os.system('python utils/modules_zipper.py modules _modules')
shutil.copytree('_modules', '{0}/modules'.format(DISTPATH))
