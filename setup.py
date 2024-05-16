from setuptools import setup, find_packages

setup(
    name='nested_dict',
    version='0.1.0',
    description='A nested dictionary class for Python',
    author='Scott McGimpsey',
    author_email='scott.mcgimpsey@gmail.com',
    url='https://github.com/mister-scott/nested_dict',
    packages=find_packages(),
    install_requires=[],  # Add any dependencies your package needs
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)