import setuptools

NAME = "seedrandom"
VERSION = "1.4"

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name=NAME,
    version=VERSION,
    author="BananaLoaf",
    author_email="bananaloaf@protonmail.com",
    keywords=["random", "seed", "generator", "hash", "int", "float", "bool", "bytes"],
    license="MIT",
    description="Random number generation based on the seed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/BananaLoaf/{NAME}",
    download_url=f"https://github.com/BananaLoaf/{NAME}/archive/v{VERSION}.tar.gz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"])
