from setuptools import setup, find_packages


setup(
    name='nemdata',
    version='0.0.2',

    description='downloading useful data for the Australian NEM',
    author='Adam Green',
    author_email='adam.green@adgefficiency.com',
    url='http://www.adgefficiency.com/',

    packages=find_packages(exclude=['tests', 'tests.*']),

    # setup_requires=['pytest-runner'],
    # tests_require=['pytest'],
    install_requires=['Click'],
    entry_points='''
            [console_scripts]
            nem=nemdata.cli:main
        '''
)
