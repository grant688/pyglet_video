# -*- mode: python -*-

block_cipher = None


a = Analysis(['videoplayer.py'],
             pathex=['G:\\Grant_Peng\\Code\\Python\\pyglet_video\\src'],
             binaries=[],
             datas=[('a.wmv','.'),
                    ('b.wmv','.'),
                    ('background.jpg','.'),
                    ('blue.jpg','.'),
                    ('btn1.jpg','.'),
                    ('btn2.png','.'),
                    ('btn3.png','.'),
                    ('btn4.jpg','.'),
                    ('yellow.JPG','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas

# append the 'res' dir
# a.datas += extra_datas('G:\\Grant_Peng\\Code\\Python\\pyglet_video\\res')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='videoplayer',
          debug=True,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
