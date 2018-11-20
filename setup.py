import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pixiv_crawler",
    version="0.0.5",
    author="Akaisorani",
    author_email="cavsolar@gmail.com",
    description="A tool to download pixiv pictures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akaisorani/pixiv-crawler",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)