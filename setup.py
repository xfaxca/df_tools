# setup.py

from distutils.core import setup

setup(name='df_tools',
      version='1.1',
      description='An Extension of Tools for pandas DataFrames',
      author='Cameron Faxon',
      license='GNU GPLv3',
      author_email='xfaxca@tutamail.com',
      url='https://github.com/xfaxca/df_tools',
      packages=['df_tools'],
      requires=['pandas', 'numpy', 'pathlib2'])
