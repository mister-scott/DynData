from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="NestedDict",
    version="0.2.0",
    author='Scott McGimpsey',
    author_email='scott.mcgimpsey@gmail.com',
    url='https://github.com/mister-scott/NestedDict',
    description="A dynamic nested dictionary with NumPy integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy>=1.18.0',
    ],
)