from pathlib import Path
from setuptools import setup, find_packages


DIR = Path(__file__).parent
REQIREMENTS_FILE = DIR / "requirements.txt"
install_requires = REQIREMENTS_FILE.read_text()


setup(
    name='packer',
    version="0.0.1",

    author='lastway90',
    author_email='lastway90@gmail.com',

    packages=find_packages(),

    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            [
                "pack=packer.src.cli:cli",
            ]
        ]
    },
)
