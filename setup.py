"""
setup file for pwnc. Shamelessly inspired by bscan:
https://github.com/welchbj/bscan/blob/master/setup.py
"""

import codecs
import os

from setuptools import (
    find_packages,
    setup)

HERE = os.path.abspath(os.path.dirname(__file__))
PWNC_DIR = os.path.join(HERE, 'pwnc')
VERSION_FILE = os.path.join(PWNC_DIR, 'version.py')

with codecs.open(VERSION_FILE, encoding='utf-8') as f:
    exec(f.read())
    version = __version__  # noqa

setup(
    name='pwnc',
    version=version,
    description='query https://libc.rop in python',
    long_description='Visit the project\'s home page for more information',
    author='Joe Hilbert',
    author_email='jhilbs3@gmail.com',
    url='https://github.com/jhilbs3/pwnc',
    license='GPL-3.0',
    install_requires=['urllib3', 'json', 'typing'],
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ]
)

