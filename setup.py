from setuptools import setup, find_packages
 
with open("readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='spaghettiWithBQN',
    version='0.2',
    description="BQN evaluation in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Brian Ellingsgaard",
    author_email='brianellingsgaard9@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Brian-ED/spaghettiWithBQN',
    keywords='BQN evaluation in Python.',
    install_requires=[
        'numpy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)