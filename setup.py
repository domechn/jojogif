import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jojogif",
    version="0.0.2",
    author="domgoer",
    author_email="domdoumc@gmail.com",
    description="Convert video to GIF,Add JoJo Ending",
    long_description="Is that part of your calculation, JOJO?",
    long_description_content_type="text/markdown",
    url="https://github.com/domgoer/jojogif",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
