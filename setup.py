from setuptools import setup, find_packages

setup(name='varselect',
    version='0.0.1',
    description=u"Variable Selection CLI",
    classifiers=[],
    keywords='',
    author=u"Spencer Cox",
    author_email='spencer.cox@tesera.com',
    url='https://github.com/tesere/varselect-cli',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'example', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'docopt',
        'schema',
        'boto3',
        'rpy2'
    ],
    extras_require={
      'test': ['pytest'],
    },
    entry_points="""
    [console_scripts]
    varselect=varselect.cli:cli
    """
)
