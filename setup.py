# http://bugs.python.org/issue15881#msg170215
from setuptools import setup, find_packages

setup(
    name="tripal",
    version='2.0',
    description="Tripal library",
    author="Anthony Bretaudeau",
    author_email="anthony.bretaudeau@inra.fr",
    url="https://github.com/galaxy-genome-annotation/python-tripal",
    install_requires=['requests>=2.4.3', 'wrapt', 'click', 'pyyaml'],
    packages=find_packages(),
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    entry_points='''
        [console_scripts]
        tripaille=tripaille.cli:tripaille
    ''',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ])
