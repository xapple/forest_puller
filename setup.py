from setuptools import setup, find_packages

setup(
        name             = 'forest_puller',
        version          = '1.2.2',
        description      = 'A package for retrieving data concerning forests on the European continent.',
        long_description = open('README.md').read(),
        long_description_content_type = 'text/markdown',
        license          = 'MIT',
        url              = 'http://github.com/xapple/forest_puller/',
        author           = 'Lucas Sinclair',
        author_email     = 'lucas.sinclair@me.com',
        packages         = find_packages(),
        install_requires = ['pandas>=1.0.0', 'matplotlib>=3.0.0',
                            'numpy', 'brewer2mpl', 'requests', 'lxml',
                            'autopaths>=1.3.6', 'plumbing>=2.6.3',
                            'pymarktex>=1.2.8', 'tqdm>=4.41.1'],
        include_package_data = True,
)
