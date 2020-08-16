from setuptools import setup, find_packages
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
    license="MIT",

    description="Deterministic seeded RNG",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["random", "seed", "generator", "hash", "int", "float", "bool", "bytes"],

    url=f"https://github.com/BananaLoaf/seedrandom",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"])
