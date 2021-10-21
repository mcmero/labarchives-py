from setuptools import setup, find_packages

setup(
    name='labarchivespy',
    version='0.1.0',
    author='Marek Cmero',
    packages=['labarchivespy'],
    package_dir={'labarchivespy': 'labarchivespy'},
    url='https://github.com/mcmero/labarchives-py',
    description=('A python wrapper for making calls to the LabArchvies API.'),
    install_requires=['requests>=2.25.1', 'pytest>=6.2.4', 'pyyaml>=5.4.1'],
)