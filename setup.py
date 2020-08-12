#!/usr/bin/env python
"""This module implements build settings."""
from setuptools import find_packages, setup  # type: ignore


def main():
    """This function implements build settings."""
    with open("README.md", "r", encoding="utf8") as file:
        readme = file.read()

    setup(
        author="Yukihiko Shinoda",
        author_email="yuk.hik.future@gmail.com",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Software Development",
            "Topic :: Software Development :: Testing",
            "Topic :: Software Development :: Testing :: Unit",
            "Topic :: System :: Filesystems",
            "Typing :: Typed",
        ],
        dependency_links=[],
        description=(
            "This project helps you to vacate specific file path "
            "or deploy resource file into specific file path when unit testing."
        ),
        install_requires=[],
        keywords="fixture file vacate deploy unittest pytest testing",
        name="fixturefilehandler",
        long_description=readme,
        long_description_content_type="text/markdown",
        packages=find_packages(exclude=("tests*", "yourproduct*")),
        package_data={"fixturefilehandler": ["py.typed"]},
        python_requires=">3.6.0",
        setup_requires=["pytest-runner"],
        url="https://github.com/yukihiko-shinoda/fixture-file-handler",
        version="1.2.0",
    )


if __name__ == "__main__":
    main()
