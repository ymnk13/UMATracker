import os

datas = [('./data', 'data'),
        ('./lib/blockly', 'lib/blockly'),
        ('./lib/closure-library', 'lib/closure-library'),
        ('./lib/editor', 'lib/editor'),]

binaries = [(r'/usr/local/Cellar/ffms2/2.21/lib/libffms2.dylib', 'lib'), ]

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

tmp = []

lib_path_list = [
        '/usr/local/Cellar/ffmpeg/',
        '/usr/local/Cellar/x264/',
        '/usr/local/Cellar/lame/',
        '/usr/local/Cellar/libvo-aacenc/'
        ]

for lib_path in lib_path_list:
    for dir_path, dir_names, file_names in os.walk(lib_path):
        for file_name in file_names:
            full_path = os.path.join(dir_path, file_name)
            if os.path.splitext(file_name)[1]=='.dylib':
                tmp.append(
                        (
                            file_name,
                            full_path,
                            'BINARY'
                            )
                        )
a.binaries += tmp

pyz = PYZ(a.pure, cipher=None)
exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        a.binaries,
        name='UMATracker-FilterGenerator',
        debug=False,
        strip=None,
        upx=True,
        console=False, icon='./icon/icon.icns')

coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name=os.path.join('dist', 'UMATracker'))

app = BUNDLE(coll,
        name=os.path.join('dist', 'UMATracker-FilterGenerator.app'),
        appname="UMATracker-FilterGenerator",
        version = '0.1', icon='./icon/icon.icns'
        )
