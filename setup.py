from setuptools import setup, find_packages


setup(
    name = 'cortex',
    version = '0.1.0',
    author = 'Tom Tsabar',
    description = 'Final Project in Advanced System Design',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)