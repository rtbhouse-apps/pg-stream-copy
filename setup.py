from setuptools import setup, find_packages
from pg_batch_inserter import __version__ as version


setup(
    name='pg_batch_inserter',
    version=version,
    description='RTB apps PostgreSQL Batch Inserter',
    url='git@github.com:rtbhouse-apps/rtb-apps-pylib.git',
    author='rtb apps team',
    author_email='apps@rtbhouse.com',

    packages=find_packages(exclude=['tests']),
    install_requires=[
    ],
    extras_require={
        'dev': [
            'pytest==5.2.0',
        ],
        'test': [
            'psycopg2-binary==2.8.4'
        ],
    },
)
