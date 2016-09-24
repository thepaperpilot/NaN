from distutils.core import setup
import py2exe

setup(
	name = 'NaN',
	url = 'https://github.com/thepaperpilot/NaN',
	options = {'py2exe': {'packages': ['esper', 'pygame']}},
	windows = [{'script': "core.py"}],
	package_dir={'': 'nan'},
	packages=[''],
    package_data={'': ['*.png', 'RobotoMono-Regular.ttf']},
    include_package_data=True,
)