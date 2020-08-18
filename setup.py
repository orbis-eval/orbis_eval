from setuptools import setup
from setuptools import find_packages

setup(
    name='orbis',
    version='3.0dev1',
    py_modules=['orbis_eval'],
    install_requires=[
        'Click',
        'orbis_eval_libs'
    ],
    entry_points='''
        [console_scripts]
        orbis=orbis_eval.orbis:cli
    ''',
    package_data={
        'orbis_eval': [
            'data/**/*'
        ]
    }
)