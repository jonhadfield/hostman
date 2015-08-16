Usage
=====
**Options**::

 hostman add [-fqbvq] [--force] [--path=PATH]
             ( [ENTRY ...] | [--input-file=FILE] | [--input-url=URL] )
 hostman remove [-qbvq] ([--address=<address>] [--names=<names>]) [--path=PATH]
                [--input-file=FILE] [--input-url=URL]
 hostman --version

Note: if a path is not supplied, the application will attempt to detect the
standard host file path based on the detected operating system being used.

Examples
========
**Add an entry to the default hosts file**::

 $ sudo hostman add 5.6.7.8 example.com example.net

**Remove all entries matching a specific address from the default hosts file**::

 $ sudo hostman remove --address=5.6.7.8 

