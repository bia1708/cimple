from setuptools import setup

setup(
    name='cimple',
    version='1.0',
    packages=['ui', 'ui.views', 'ui.components', 'domain', 'service', 'repository'],
    package_dir={'': 'src'},
    url='https://github.com/bia1708/cimple',
    license='MIT License',
    author='bia1708',
    author_email='bianca.popu@gmail.com',
    description='User-friendly interface for easily implementing CI/CD pipelines with Jenkins.'
)
