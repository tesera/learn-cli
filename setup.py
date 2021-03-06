from setuptools import setup, find_packages

setup(
    name='learn-cli',
    version='1.0.0',
    description=u"Learn Model Builder",
    classifiers=[],
    keywords='',
    author=u"Spencer Cox",
    author_email='spencer.cox@tesera.com',
    url='https://github.com/tesera/learn-cli',
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
    entry_points={
        'console_scripts': [
            'learn=learn.cli:cli'
        ]
    }
)
