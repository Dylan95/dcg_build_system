
Table of Contents:
	1.  Introduction
	2.  Dependancies
	3.  Installation
	4.  Usage
	5.  Under the Hood
	6.  Legal

1.  Introduction
	Hello.  This is a portable, cross platform, c++ build system written in python.


2.  Dependancies
	1.  Python version 3.  If you try to use it with an earlier version of python, it will not work.
	2.  A Compiler and Linker.  Currently only gcc/g++ is supported.


3.  Installation
	You should install the build system for each project you wish to use it for by copy and pasting "install/dcg_build_system" into your projects directory.  Think of it kind of like a makefile.  


4.  Usage
	run the script "dcg_build_system/scripts/buildSys.py" located in your project directory to build and clean the project.  Run the command without any extra arguments to get a usage message.

	there are six things you can do with the build system:
		1.  clean everything
		2.  clean a specific configuration
		3.  clean a specific module in a specific configuration
		4.  build everything
		5.  build a specific configuration
		6.  build a specific module in a specific configuration

	Configuration file: "dcg_build_system/config.json"
		If you get an error that looks something like "Expecting , line ... column ...".  Then you probably have a badly formatted "config.json" file.  Look at the line and column specified to see if you forgot a comma, quotes, or have an extra comma, or something like that.
		Modify this file to configure the build system.  It tells it where to look for source files, compiler and linker flags, and other such information.  For all path names, if you want them to work cross-platform, such as for local directories, then use Unix-like path names.
		It supports multiple configurations.  Which is usefull if you want a debug version that generates debug information but reduces performance, and a release version that maximizes performance.
		It supports multiple modules, which is usefull for large projects which often are broken into smaller libraries which individual programmers work on.  To add a module, copy and paste the empty module "MAIN" in "install/dcg_build_system/config.json" into your config file, into the "modules" object.  Then configure it as you see fit.  You may want to keep a "module.json" right with the module, and copy and paste it into the "config.json" for any project you wish to use it with.  Logically, a module is a group of source files that are compiled using the same settings.

	static and shared libraries can be created instead of a program.  Use the -shared flag with the linker to create a shared library.  To create a static library you'll have to use "rcs" or a similar tool.  On Unix-like systems, something like this should work: 'find dcg_build_system/build/DEBUG/modules/MAIN/objs/ -name "*" | ar rcs my_library.a'.


5.  Under the Hood
	I tried to make the build system as simple as I could.  It finds the project directory by using the python "__file__" variable to get the directory of the directory of the directory of "buildSys.py" file.  So it doesn't matter what your current directory is when you run the command.  In the scripts folder: "target/Target.py" is a class that represents one build target, it does a similar thing as a makefile: it checks to see if the dependances for the target are out of date, and then builds the dependancies and the target if nessecary.  In "util/Util.py" there's nothing special, just a lot of convenience functions.  in "project/" there's the files that parse the "config.json" file and setup build targets.  And in "cpp/*.py" there's all the classes of c++ targets.  In "cpp/toolsets/" there's the interface for the compiler and linker, so far the only toolset supported is "GCC", if you want to add more: implement "Linker" and "Compiler" for the particular toolset, and then modify "Toolset.py" to check for that toolset.


6.  Legal
	There is a file named "LICENCE" located in "install/dcg_build_system/scripts/".  Please read it.  This is the standard MIT licence.  It essentially says that you can do whatever you want so long as you keep the licence.  I hope it's clear that this only applies to the build system itself and not the software it's used to build; just keep that "LICENCE" file in that scripts folder.



