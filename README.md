hostman
========
[![Build Status](https://api.travis-ci.org/jonhadfield/hostman.svg?branch=devel)](https://travis-ci.org/jonhadfield/hostman)

A simple command line tool for managing your hosts file.
Add, remove or import entries from file or URLs.

Installation
------------
    pip install hostman


Usage
------------
  hostman add [-fqbcvq] [--force] [--path=PATH]
              ( [ENTRY ...] | [--input-file=FILE] | [--input-url=URL] )
  hostman remove [-qbcvq] ([--address=<address>] [--names=<names>]) [--path=PATH]
                 [--input-file=FILE] [--input-url=URL]
  hostman --version

Options
------------
    -h --help                    show this help message and exit
    --version                    show version and exit
    -f --force                   first remove all existing entries that match
    --address=ADDRESS            ipv6 or ipv4 address
    --names=NAMES                host names
    -q --quiet                   report only failures
    -p --path=PATH               location of hosts file (attempts to detect default)
    -i --input-file=FILE         file containing hosts to import
    -u --input-url=URL           url of file containing hosts to import
    -b --backup                  create a backup before each change
    --exclude=VALUE              comma separated list of names or addresses
                                 to exclude from operation [default: 127.0.0.1]
    -c --count                   count entries added, replaced and removed
    -v --verbose                 print verbose output

Examples
------------
Adding a single entry

    hostman add 1.2.3.4 example.com

Importing a list of host entries by URL

    hostman add --input-url https://dl.dropboxusercontent.com/u/167103/hosts

Requirements
------------
Tested on python 2.6, 2.7 and 3.4


License
-------

MIT
