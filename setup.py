# http://bugs.python.org/issue15881#msg170215
import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

subpackages = [x.replace('/', '.') for x in glob.glob('tripaille/commands/*') if not x.endswith('.py') and not x.endswith('.pyc')]
subpackages += [x.replace('/', '.') for x in glob.glob('tripal/*') if not x.endswith('.py') and not x.endswith('.pyc')]

with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="tripal",
    version='3.2.1',
    description="Tripal library",
    author="Anthony Bretaudeau",
    author_email="anthony.bretaudeau@inra.fr",
    url="https://github.com/galaxy-genome-annotation/python-tripal",
    install_requires=requires,
    packages=[
        'tripal',
        'tripaille',
        'tripaille.commands',
    ] + subpackages,
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    entry_points='''
        [console_scripts]
        tripaille=tripaille.cli:tripaille
    ''',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ])
