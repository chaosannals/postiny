import sys
from cx_Freeze import setup, Executable

base = 'Win32GUI' if sys.platform == 'win32' else None

setup(
    name='postiny',
    version='0.0.1',
    description='yet a post client',
    executables=[
        Executable(
            'app.py',
            base=base,
            icon='app.ico',
            copyright='Copyright © 2022 ChaosAnnals',
            shortcut_name='postiny',
            shortcut_dir='DesktopFolder',
        ),
    ],
    options={
        'build_exe': {
            'optimize': 2,
            'include_msvcr': True,
            'excludes': [
                'tkinter',
            ],
            'packages': [
                'peewee',
                'pyside6',
                'loguru',
            ],
        },
        'bdist_msi': {
            'all_users': True,
        },
    },
)