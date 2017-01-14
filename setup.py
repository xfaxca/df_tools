# setup.py

from setuptools import setup, find_packages


setup(name='df_tools',
      version='1.1',
      description='Tools for the manipulation of pandas DataFrames',
      author='Cameron Faxon',
      author_email='xfaxca@tutamail.com',
      license=license,
      url='https://github.com/xfaxca/df_tools',
      packages=find_packages(exclude=('tests', 'dist')),
      install_requires=['numpy==1.11.2',
                        'pandas==0.18.1',
                        'pathlib2==2.1.0'])
