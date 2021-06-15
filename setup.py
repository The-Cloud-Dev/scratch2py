
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scratch2py",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="TheCloudDev",
    license="MIT",        
    description="Python to Scratch API connector",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',                 
    install_requires=["websocket","websocket-client","wsaccel"]                    
)