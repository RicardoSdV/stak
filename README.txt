# Stak
	- The idea is to pretty print call stacks and all available introspection for debugging purposes
	in python27, planning on supporting python38 -> python314 shortly & Linux too.
	
	
# TODOS:
	- Class decorator or similar, for quick stack logging of entire class / file / module
	
	- Something to deal with complex inheritance chains without PyCharm, like, runtime function e.g.
		combineMRO("ExampleClass"), go through mro, find all the classes in the source and copy paste them 
		into a new file, maybe add some comments.
		
	- This is a logger, if it raises we don't care, the program is fine, handle all exceptions, maybe with except hook
