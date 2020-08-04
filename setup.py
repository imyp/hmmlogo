import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hmmlogo",
    version="0.0.4",
    author="Inti Manuel Yabar-Pagaza",
    author_email="intipagaza@live.dk",
    description="Package to plot logos for profile hidden Markov models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imyp/hmmlogo",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'matplotlib',
        'requests',
        'pandas',
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

