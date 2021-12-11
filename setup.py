import setuptools

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hstp",
    version="2.0.0",
    author="University Radio Nottingham",
    author_email="web@urn1350.net",
    description="hstp builder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/URN/hstp",
    project_urls={
        "Bug Tracker": "https://github.com/URN/hstp/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
