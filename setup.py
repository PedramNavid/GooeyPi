from setuptools import setup, find_packages
setup(name="gooeypi",
	version="0.1a",
	description="wxPython GUI frontend for PyInstaller 2.1",
	license="GPL",
	install_requires=['wx', 'logging', 'configobj'],
	author="Pedram Navid",
	author_email="pedram.navid@gmail.com",
	url="http://github.com/multiphrenic/GooeyPi/",
	packages = find_packages(),
	package_data ={
	'':['configspec.ini'],
	},
	keywords = "pyinstaller, gui, gooeypi",
	zip_safe = True)

