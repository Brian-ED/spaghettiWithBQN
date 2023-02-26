from setuptools import setup, find_packages

setup(
    name = "spaghettiWithBQN",
    version = "0.1.2",
    description = "BQN evaluation in python.",
    license = "MIT",
    maintainer = "Brian Ellingsgaard",
    author     = "Brian Ellingsgaard",
    author_email     = "brianellingsgaard9@gmail.com",
    maintainer_email = "brianellingsgaard9@gmail.com", 
    packages = find_packages("src"),
    package_dir = {"spaghettiWithBQN": "src"},
    url ="https://github.com/Brian-ED/spaghettiWithBQN",
    keywords ="BQN evaluation in Python.",
    install_requires = [
        "numpy",
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)