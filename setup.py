import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scratch2py",
    url="https://github.com/The-Cloud-Dev/scratch2py",
    version="0.3.1",
    author="TheCloudDev",
    license="MIT",
    description="Python to Scratch API connector",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["websocket-client","ScratchEncoder", "requests"]
)
