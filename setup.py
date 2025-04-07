from setuptools import setup, find_packages

# Read the contents of the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="yellowchangerapi",
    version="1.0.4",
    author="Fluf",
    author_email="support@yellowchanger.com",
    description="A Python library for interacting with the YellowChanger service API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yellowfluf/YellowChangerAPI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "requests",
        "httpx",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/yellowfluf/YellowChangerAPI/issues',
        'Source': 'https://github.com/yellowfluf/YellowChangerAPI/tree/main',
    },
)
