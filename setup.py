from setuptools import setup

#install requirements provided by requirements.txt
install_requirements = open("requirements.txt").read().split('\n')
#readme from repo
readme_contents = open("README.md").read()

jno_version = "0.5.0"

#input into setup
setup(
	name="jno",
	version=jno_version,
	description="Command line interface wrapper for Arduino IDE, inspired by ino",
	long_description=readme_contents,
	long_description_content_type="text/markdown",
	url = "https://github.com/kosinkadink/jno",
	author="Jedrzej Kosinski",
	author_email="kosinkadink1@gmail.com",
	license="MIT",
	keywords="arduino interface ide wrapper",
	packages=["jno","jno.commands"],
	include_package_data=True,
	install_requires=install_requirements,
	entry_points = {
		"console_scripts": [
			"jno=jno.__main__:main",
		]
	},
	classifiers=[
		"Development Status :: 4 - Beta",
		"License :: OSI Approved :: MIT License",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 3",
		"Topic :: Software Development :: Embedded Systems"
	],
)