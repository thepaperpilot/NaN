from distutils.core import setup
import py2exe

setup(
	name = 'NaN',
	url = 'https://github.com/thepaperpilot/NaN',
	windows = [{'script': "core.py"}],
	options = {'py2exe': {'packages': ['esper', 'pygame']}},
    package_data={'': ['*.png', 'RobotoMono-Regular.ttf', 'README.txt']},
)
