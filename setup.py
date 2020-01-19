from setuptools import setup, find_packages

setup(
        name             = 'forest_puller',
        version          = '1.0.0',
        description      = 'A package for retrieving data concerning forests on the European continent.',
        long_description = open('README.md').read(),
        license          = 'MIT',
        url              = 'https://gitlab.com/bioeconomy/puller/forest_puller',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        packages         = find_packages(),
        install_requires = ['pandas', 'numpy', 'autopaths', 'plumbing', 'lxml', 'requests', 'tqdm'],
)
