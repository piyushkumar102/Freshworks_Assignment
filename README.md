# Freshworks_Assignment

Assignement to create a key-value data store

Language: Python Version: 3.6

Required Packages: portalocker

OS: Windows Code works on Windows since portalocker works on windows and for linux and unix different packages can be
used. Ideally based on the platform locks can be applied using sys.platform() , as i dont have linux to test i have
written code that works in Windows.

As GIL allows only one thread to hold control of python interpreter hence it is thread-safe,yet locks can be pass as
arguments to the functions.

Unit Test cases has been attached.

As there was no restriction in the type of file to be used, I have used JSON format as the complete backend file.
Function Signature:
create()
read(key)
delete(key)
Database(name[,location])

WorkFlow:
Database.py and __init__.py are file of the package created. 
main.py is used to run the Program
