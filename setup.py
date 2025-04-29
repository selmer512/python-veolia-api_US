from setuptools import setup, find_packages

setup(
    name="pyolia-us",  # New unique name
    version="0.1.0",
    author="selmer512",
    author_email="admin@cyberhoney.one",  # (PyPI will require a valid email)
    description="Python API for Veolia US Water Portal",
    long_description="Python async client to access Veolia US water consumption data.",
    long_description_content_type="text/markdown",
    url="https://github.com/selmer512/python-veolia-api_US",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "beautifulsoup4>=4.10.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
