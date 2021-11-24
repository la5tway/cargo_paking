from setuptools import setup, find_packages

setup(
    name='packer',
    version='0.1.0',

    author='lastway90',
    author_email='lastway90@gmail.com',

    packages=find_packages(where='packer'),
    package_dir={'': 'packer'},

    install_requires=['pillow'],
)
