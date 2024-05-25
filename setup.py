from setuptools import setup, find_packages


setup(
    name='cimple',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'python-jenkins'
    ],
    entry_points={
        'gui_scripts': [
            'cimple = src:main',
        ]
    },
    url='https://github.com/bia1708/cimple',
    license='MIT License',
    author='bia1708',
    author_email='bianca.popu@gmail.com',
    description='User-friendly interface for easily implementing CI/CD pipelines with Jenkins.'
)
