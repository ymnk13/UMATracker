import os


datas = [('./data', 'data'),
        ('./lib/blockly', 'lib/blockly'),
        ('./lib/closure-library', 'lib/closure-library'),
        ('./lib/editor', 'lib/editor'),]

binaries = []
for dir_path, dir_names, file_names in os.walk("dll"):
    for file_name in file_names:
        binaries.append((os.path.join('.\\', dir_path, file_name), 'dll'))

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
