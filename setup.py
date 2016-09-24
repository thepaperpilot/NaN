from distutils.core import setup
import py2exe

setup(
    options = {'py2exe': {'packages': ['esper', 'pygame']}},
    windows = [{'script': "core.py"}],
)