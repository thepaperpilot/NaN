from distutils.core import setup
import py2exe, sys

sys.argv.append('py2exe')

setup(
	name = 'NaN',
	url = 'https://github.com/thepaperpilot/NaN',
	windows = [{'script': "nan/core.py"}],
	options = {'py2exe': {'packages': ['esper', 'pygame']}},
	packages = ['nan'],
    package_data={'': ['*.png', 'kenpixel.ttf', 'README.txt']},
)
