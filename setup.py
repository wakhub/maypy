from setuptools import setup

import maypy


setup(
    name=maypy.__name__,
    version=maypy.__version__,
    author='wak',
    author_email='wkwkwk0111@gmail.com',
    description="Maybe object for Python",
    license='MIT',
    keywords='optional maybe null',
    url='https://github.com/wakhub/maypy',
    py_modules=['optional'],
    long_description=open('README.rst').read()
)
