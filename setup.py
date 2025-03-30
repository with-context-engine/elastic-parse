from setuptools import setup, find_packages

setup(
    name="elastic_parse",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "crawl4ai",  # Add other dependencies as needed
    ],
) 