
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
	The only dependancy is Python version 3.  If you try to use it with an earlier version of python, it will not work.


3.  Installation
	You should install the build system for each project you wish to use it for by copy and pasting "install/dcg_build_system" into your projects directory.  Think of it kind of like a makefile.  


4.  Usage
	run the script "dcg_build_system/scripts/buildSys.py" located in your project directory to build and clean the project.  Configure the project by modifying the ".txt" files located in "dcg_build_system/config/".

	there are six things you can do with the build system:
		1.  clean everything
		2.  clean a specific configuration
		3.  clean a specific module in a specific configuration
		4.  build everything
		5.  build a specific configuration
		6.  build a specific module in a specific configuration

	Configuration files:
		in "dcg_build_system/config" 
		


6.  Legal
	There is a file named "LICENCE" located in "install/dcg_build_system/scripts/".  Please read it.  This is the standard MIT licence.  It essentially says that you can do whatever you want so long as you keep the licence.  I hope it's clear that this only applies to the build system itself and not the software it's used to build; just keep that "LICENCE" file in that scripts folder.
