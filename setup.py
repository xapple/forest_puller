from setuptools import setup, find_packages

setup(
        name             = 'forest_puller',
        version          = '0.1.0',
        description      = 'A package for retrieving data concerning forest growth and stock on the European continent.',
        long_description = open('README.md').read(),
        license          = 'MIT',
        url              = 'https://gitlab.com/bioeconomy/puller/forest_puller',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        packages         = find_packages(),
        install_requires = ['pandas', 'autopaths', 'plumbing', 'lxml'],
    )
