import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypackage-chris633",
    version="1.0.1",
    author="chris633",
    author_email="chris63388@outlook.com",
    description="My Packaging Note",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chris633/python_packaging_learning",
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    install_requires=['flask>=1.0.0'],
    entry_points={
        'console_scripts': [
            
   		],
	},
)