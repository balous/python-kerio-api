#!/usr/bin/env python

from setuptools import setup
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class MambaTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import sys
        import mamba.cli
        sys.argv = ['mamba', '--format', 'documentation']
        mamba.cli.main()

setup(
        name = 'kerio-api',
        version = '0.2',
        packages = ['kerio'],
        install_requires = [
        ],
        tests_require = [
            'mamba',
            'expects',
            'doublex',
            'doublex_expects',
            'HTTPretty',
            'mock',
        ],
        cmdclass = {'test': MambaTest},
        zip_safe = False,
)
