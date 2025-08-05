"""
Setup script for IGNOU Question Paper Downloader
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ignou-qp-downloader",
    version="1.0.0",
    author="Samiran Kakoty",
    author_email="samiran.kakoty@gmail.com",
    description="A Python tool to download previous year question papers for IGNOU students",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samirank/qp_downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ignou-qp-downloader=qp_downloader:main",
        ],
    },
    keywords="ignou, question-papers, downloader, education, bca, mca",
    project_urls={
        "Bug Reports": "https://github.com/samirank/qp_downloader/issues",
        "Source": "https://github.com/samirank/qp_downloader",
        "Documentation": "https://github.com/samirank/qp_downloader#readme",
    },
)