"""
    Setup.py for deploying this distribution
"""
import pathlib

from setuptools import find_packages, setup

# Get the directory that this file is in
DIR = pathlib.Path(__file__).parent

# Read the text of the markdown file
README = (DIR / "README.md").read_text()

# Setup the pip package
setup(
    name="deepdos",
    version="0.9.95",
    description="A machine learning/AI based approach to protecting your devices against ddos attacks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/C3NZ/deepdos",
    author="C3NZ",
    author_email="cenz@cenz.io",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Security",
        "Environment :: Console",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Development Status :: 2 - Pre-Alpha",
    ],
    packages=find_packages(),
    include_package_data=True,
    setup_requires=["wheel"],
    install_requires=[
        "psutil==5.6.6",
        "pandas==0.25.1",
        "numpy==1.17.2",
        "python_iptables==0.14.0",
        "scikit_learn==0.21.3",
        "wheel==0.32.3",
        "tinydb==3.15.0",
        "colorama==0.4.1",
    ],
    entry_points={"console_scripts": ["deepdos=deepdos.__main__:start_execution"]},
)
