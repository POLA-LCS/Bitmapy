from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Bitmapy",
    version="0.1.3",
    author="Baltazar Zara Pilling",
    author_email="zara.pilling18@gmail.com",
    description="A bitmap multitool (read, write, convert)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/POLA-LCS/Bitmapy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "Pillow",
    ],
)
