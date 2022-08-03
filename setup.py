import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ds2",
    version="0.2.4",
    author="Donald R. Sheehy",
    author_email="don.r.sheehy@gmail.com",
    description="Don Sheehy's Data Structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/donsheehy/datastructures",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
