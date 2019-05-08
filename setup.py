import setuptools
from seedrandom import __version__

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="seedrandom",
    version=__version__,
    author="BananaLoaf",
    author_email="bananaloaf@protonmail.com",
    keywords=["random", "seed", "generator", "hash", "int", "float", "bool", "bytes"],
    license="MIT",
    description="Random number generation based on the seed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/BananaLoaf/seedrandom",
    download_url=f"https://github.com/BananaLoaf/seedrandom/archive/v{__version__}.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"])
