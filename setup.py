#!/user/bin/env python
from setuptools import setup

#install requirements provided by requirements.txt
install_requirements = open("requirements.txt").read().split('\n')
#readme from repo
readme_contents = open("README.md").read()

jno_data = ['jno.jno']

jno_version = '0.1.2'

#input into setup
setup(
	name='jno',
	version=jno_version,
	description='Command line interface wrapper for Arduino IDE, inspired by ino',
	long_description=readme_contents,
	url = 'https://github.com/kosinkadink/jno',
	download_url = 'https://github.com/kosinkadink/jno/archive/{}.tar.gz'.format(jno_version),
	author='Jedrzej Kosinski',
	author_email='kosinkadink1@gmail.com',
	license='MIT',
	keywords='arduino interface wrapper',
	packages=['jno','jno.commands'],
	package_data={'jno':jno_data},
	scripts=['bin/jno'],
	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Programming Language :: Python",
		"Topic :: Software Development :: Embedded Systems"
	],
)