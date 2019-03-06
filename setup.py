import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="importrc",
    version="0.1.0",
    author="Ben Nuttall",
    description="One command to import your dotfiles from GitHub",
    license="BSD",
    keywords=[],
    url="",
    packages=find_packages(),
    requires=[
        'wget',
    ],
    long_description=read('README.md'),
    entry_points={
        'console_scripts': [
            'importrc = importrc.importrc:main',
        ]
    },
)
