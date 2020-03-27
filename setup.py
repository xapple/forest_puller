from setuptools import setup, find_packages

setup(
        name             = 'forest_puller',
        version          = '1.2.0',
        description      = 'A package for retrieving data concerning forests on the European continent.',
        long_description = open('README.md').read(),
        long_description_content_type = 'text/markdown',
        license          = 'MIT',
        url              = 'http://github.com/xapple/forest_puller/',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        packages         = find_packages(),
        install_requires = ['pandas', 'numpy', 'autopaths>=2.5.8', 'plumbing>=1.3.5', 'lxml', 'requests', 'tqdm>=4.41.1',
                            'matplotlib', 'brewer2mpl'],
        include_package_data = True,
)
