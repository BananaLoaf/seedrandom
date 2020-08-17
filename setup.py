# Local
from setuptools import setup, find_packages

# Project
from seedrandom import PACKAGE_NAME, __version__


with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name=PACKAGE_NAME,
    version=__version__,
    packages=find_packages(),

    # Metadata for PyPi
    author="BananaLoaf",
    author_email="bananaloaf@protonmail.com",
    # maintainer="BananaLoaf",
    # maintainer_email="bananaloaf@protonmail.com",
    license="MIT",

    description="Deterministic seeded RNG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["random", "seed", "generator", "hash", "int", "float", "bool", "bytes", "rng", "deterministic"],

    url=f"https://github.com/BananaLoaf/seedrandom",
    # download_url=None,
    # project_urls={
    #     "Lord and Saviour": "https://stackoverflow.com/"
    # },

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ])
