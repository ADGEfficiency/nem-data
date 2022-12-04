from setuptools import find_packages, setup

setup(
    name="nemdata",
    version="0.0.4",
    description="CLI for downloading AEMO Australian electricity grid data for the NEM.",
    author="Adam Green",
    author_email="adam.green@adgefficiency.com",
    url="http://www.adgefficiency.com/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    install_requires=["Click"],
    entry_points="""
            [console_scripts]
            nemdata=nemdata.cli:cli
        """,
)
