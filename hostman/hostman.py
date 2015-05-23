#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hostman.

Usage:
  hostman add [-fqbcvq] [--force] [--path=PATH]
              ( [ENTRY ...] | [--input-file=FILE] | [--input-url=URL] )
  hostman remove [-qbcvq] ([--address=<address>] [--names=<names>]) [--path=PATH]
                 [--input-file=FILE] [--input-url=URL]
  hostman --version

Options:
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
"""
from docopt import docopt
from hosts import Hosts, HostsEntry, utils
import sys
import time
import shutil


def backup_hosts(source=None):
    epoch_time = int(time.time())
    dest_split = source.split('/')
    new_filename = ".{0}.{1}".format(dest_split[-1], epoch_time)
    dest_split[-1] = new_filename
    dest = "/".join(dest_split)
    print dest
    try:
        shutil.copy(source, dest)
    except shutil.Error as e:
        print('Error: %s' % e)
    except IOError as e:
        print('Error: %s' % e.strerror)

def output_message(message=None):
    if isinstance(message, dict):
        print("result: {0}".format(message.get('result')))
        print("message: {0}".format(message.get('message')))
    else:
        print("Failed to output message")

def add(entry=None, path=None, force=False, input_file=None):
    """
    Add the specified entry
    :param entry: The entry to add
    :param path: The path of the hosts file
    :param force: Remove all matching entries before adding
    :return:
    """
    if path:
        hosts = Hosts(path)
    else:
        hosts = Hosts()
    if input_file and utils.is_readable(input_file):
        with open(input_file, 'r') as infile:
            for line in iter(infile.readline, ''):
                hosts.add(line)
    output_message(hosts.add(entry, force=force))

def add_file(input_file=None):
    if path:
        hosts = Hosts(path)
    else:
        hosts = Hosts()
    output_message(hosts.import_file(input_file))

def remove(address=None, names=None, partial=False, path=None):
    """
    Remove entries matching
    :param entry: The entry to add
    :param path: The path of the hosts file
    :param force: Remove all matching entries before adding
    :return:
    """
    if path:
        hosts = Hosts(path)
    else:
        hosts = Hosts()
    output_message(hosts.remove(address=address, names=names))

def format_entry(value):
    if isinstance(value, list):
        entry_string = ' '.join(value)
        return entry_string.strip()
    if isinstance(value, str):
        return value.strip()

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.0')
    print(arguments)
    entry = arguments.get('ENTRY')
    path = arguments.get('--path')
    force = arguments.get('--force')
    backup = arguments.get('--backup')
    address = arguments.get('--address')
    names = arguments.get('--names')
    input_file = arguments.get('--input-file')

    new_entry = None
    if entry:
        new_entry = format_entry(entry)

    if not path:
        if sys.platform.startswith('win'):
            path = r'c:\windows\system32\drivers\etc\hosts'
        else:
            path = '/etc/hosts'

    if backup:
        if utils.is_readable(path):
            backup_hosts(source=path)

    if utils.is_writeable(path):
        if arguments.get('add'):
            if new_entry:
                add(entry=new_entry, path=path, force=force)
            if input_file:
                add_file(input_file)

        if arguments.get('remove'):
            remove(address=address, names=names, path=path)
    else:
        print "Cannot open path: {}\nCheck you have the necessary permissions.".format(path)

