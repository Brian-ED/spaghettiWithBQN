from setuptools import setup, find_packages

setup(
    name='spaghettiWithBQN',
    version='0.1.1',
    description="BQN evaluation in python.",
    license='MIT',
    author="Brian Ellingsgaard",
    author_email='brianellingsgaard9@gmail.com',
    packages=find_packages('./'),
    package_dir={'./': 'src'},
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