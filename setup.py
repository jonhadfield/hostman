#!/usr/bin/env python

import os
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

version = "0.1.1"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

long_description = readme + '\n\n' + history

if sys.argv[-1] == 'readme':
    print(long_description)
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='pyhostman',
    version=version,
    author='Jon Hadfield',
    author_email='jon.hadfield@lessknown.co.uk',
    url='http://github.com/jonhadfield/hostman',
    install_requires=['docopt>=0.6.2', 'colorama>=0.3.3', 'python-hosts>=0.3.2'],
    description='A CLI to manage a hosts file',
    long_description=long_description,
    packages=['hostman'],
    platforms='any',
    license='MIT',
    entry_points={
        'console_scripts': ['hostman=hostman.__init__:real_main'],
    },
    package_dir={'hostman': 'hostman'},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Operating System',
        'Topic :: System :: Networking',
    ],
    keywords=(
        'hosts, Python, network'
    ),
    tests_require=['pytest', 'python-hosts==0.3.2'],
    cmdclass={'test': PyTest},
)
