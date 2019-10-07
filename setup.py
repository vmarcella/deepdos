import pathlib

from setuptools import setup

DIR = pathlib.Path(__file__).parent

# Reead the text of the markdown file
README = (DIR / "README.md").read_text()

setup(
    name="deepdos",
    version="0.9.0",
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
    packages=["src"],
    include_package_data=True,
    install_requires=[
        "psutil==5.6.3",
        "pandas==0.25.1",
        "numpy==1.17.2",
        "python_iptables==0.14.0",
        "sckit_learn==0.21.3",
    ],
    entry_points={"console_scripts": ["deepdos=src.main:start_execution"]},
)
