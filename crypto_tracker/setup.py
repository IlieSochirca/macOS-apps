from setuptools import setup

APP = ['./src/main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': './src/coin.png',
    'packages': ['rumps', 'requests'],
}

setup(
    app=APP,
    name='Crypto Tracker',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)