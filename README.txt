# Stak
	- The idea is to pretty print call stacks and all available introspection for debugging purposes
	in python27, planning on supporting python38 -> python314 shortly

# Requirements for using:
	- Windows / Linux
	- Python27

## Compilation:
	Compilation is dependent on the OS, the machine specs, the python version, ...
	it is too onerous to provide binaries for all the combinations, so, the solution
	is for the user to compile their own binaries. A python script is provided, it
	ought to work, in most cases, see ## Compile script requirements

	Some binaries will be provided though, they can be found in stak/stak/lib/pyds, for now:
		- x86_64, Linux, Ubuntu, python27


## Compile script requirements
	# Python versions supported:
		- 2.7.18
		- (Python 3 will be supported soon)

	# Requirements for compiling with compile.py in Linux:
		- packages: g++, make, cmake

		- python: For running the script itself, one of the supported versions
				  by stak is recommended. Also, headers are taken for compilation
				  from this version, so it must be the target version.

		- pybind11: You need specific pybind11 versions matching specific python versions
					for python versions explicitly supported by stak, the necessary
					version is bundled with the project, in stak/stak/c/compile/lib/

	# Requirements for compiling with compile.py in Windows: TODO: windows compilation has not been set up yet
		- MSVC: You need to compile with MSVC, with a different version of it for different versions of python,
				for python27 you would need MSVC 2008
