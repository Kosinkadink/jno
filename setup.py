#!/user/bin/env python
from setuptools import setup

#install requirements provided by requirements.txt
install_requirements = open("requirements.txt").read().split('\n')
#readme from repo
readme_contents = open("README.md").read()

jno_data = ['jno.jno']

#input into setup
setup(
	name='jno',
	version='0.1.0',
	description='Command line interface wrapper for Arduino IDE, inspired by ino',
	long_description=readme_contents,
	url = 'https://github.com/kosinkadink/jno',
	download_url = 'https://github.com/kosinkadink/jno/archive/0.1.0.tar.gz',
	author='Jedrzej Kosinski',
	license='MIT',
	keywords='arduino interface wrapper',
	packages=['jno','jno.commands'],
	package_data={'jno':jno_data},
	scripts=['bin/jno'],
	classifers=[]
)