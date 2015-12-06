import os


datas = [('./data', 'data'),
        ('./lib/blockly', 'lib/blockly'),
        ('./lib/closure-library', 'lib/closure-library'),
        ('./lib/editor', 'lib/editor'),]
# binaries = [('ffms2.dll',    os.path.join(os.getcwd(), 'dll', 'ffms2.dll'),    'BINARY'),
#             ('msvcp120.dll', os.path.join(os.getcwd(), 'dll', 'msvcp120.dll'), 'BINARY'),
#             ('msvcr120.dll', os.path.join(os.getcwd(), 'dll', 'msvcr120.dll'), 'BINARY'),
#             ('opencv_ffmpeg300_64.dll', os.path.join(os.getcwd(), 'dll', 'opencv_ffmpeg300_64.dll'), 'BINARY')]

binaries = [(os.path.join(os.getcwd(), 'dll', 'ffms2.dll'), 'dll'),
        (os.path.join(os.getcwd(), 'dll', 'msvcp120.dll'), 'dll'),
        (os.path.join(os.getcwd(), 'dll', 'msvcr120.dll'), 'dll'),
        (os.path.join(os.getcwd(), 'dll', 'opencv_ffmpeg300_64.dll'), 'dll')]

a = Analysis(['./main.py'],
        pathex=['./'],
        binaries=binaries,
        datas=datas,
        hiddenimports=[],
        hookspath=None,
        runtime_hooks=None,
        excludes=None,
        win_no_prefer_redirects=None,
        win_private_assemblies=None,
        cipher=None)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        a.binaries,
        name='UMATracker-FilterGenerator',
        debug=False,
        strip=None,
        upx=False,
        console=False, icon='./icon/icon.ico')
