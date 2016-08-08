# http://bugs.python.org/issue15881#msg170215
from setuptools import setup, find_packages

setup(
    name="tripal",
    version='1.0',
    description="Tripal API library",
    author="Anthony Bretaudeau",
    author_email="anthony.bretaudeau@inra.fr",
    url="https://github.com/abretaud/python-tripal"
    install_requires=['requests>=2.4.3'],
    packages=find_packages(),
    license='MIT',
    platforms="Posix; MacOS X; Windows",
    scripts=[
        'scripts/get_all_jobs.py',
        'scripts/get_job.py',
        'scripts/load_blast.py',
        'scripts/load_fasta.py',
        'scripts/load_gff3.py'
        'scripts/load_interpro.py',
    ],
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
