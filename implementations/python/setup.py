"""
Setup script for SLD Python package
"""

from setuptools import setup, find_packages

with open("../../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sld-format",
    version="1.1.0",
    author="SLD Project Contributors",
    author_email="",
    description="Single Line Data (SLD) and Multi Line Data (MLD) format parser and encoder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/proteo5/sld",
    project_urls={
        "Bug Tracker": "https://github.com/proteo5/sld/issues",
        "Documentation": "https://github.com/proteo5/sld#readme",
        "Source Code": "https://github.com/proteo5/sld",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing",
    ],
    py_modules=["sld"],
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    keywords="sld mld data-format parser encoder serialization",
)
