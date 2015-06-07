#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Hostman.

Usage:
  hostman add [-fqbvq] [--force] [--path=PATH]
              ( [ENTRY ...] | [--input-file=FILE] | [--input-url=URL] )
  hostman remove [-qbvq] ([--address=<address>] [--names=<names>]) [--path=PATH]
                 [--input-file=FILE] [--input-url=URL]
  hostman --version

Options:
  -h --help                    show this help message and exit
  --version                    show version and exit
  -f --force                   replace matching entries
  --address=ADDRESS            ipv6 or ipv4 address
  --names=NAMES                host names
  -q --quiet                   report only failures
  -p --path=PATH               location of hosts file (attempts to detect default)
  -i --input-file=FILE         file containing hosts to import
  -u --input-url=URL           url of file containing hosts to import
  -b --backup                  create a backup before writing any changes
  --exclude=VALUE              comma separated list of names or addresses
                               to exclude from operation [default: 127.0.0.1]
  -v --verbose                 print verbose output
"""
from docopt import docopt
from python_hosts import Hosts, HostsEntry, is_writeable, is_readable
import sys
import os
import datetime
import shutil
from colorama import Fore, init
init(autoreset=True)


def backup_hosts(source=None, extension=None):
    if not extension:
        now = datetime.datetime.now()
        ext = now.strftime('%Y%m%d%H%M%S')
    else:
        ext = extension
    dest_split = source.split('/')
    new_filename = ".{0}.{1}".format(dest_split[-1], ext)
    dest_split[-1] = new_filename
    dest = "/".join(dest_split)
    try:
        shutil.copy(source, dest)
        return {'result': 'success', 'message': 'Backup written to: {0}'.format(dest)}
    except IOError:
        return {'result': 'failed', 'message': 'Cannot create backup file: {0}'.format(dest)}


def output_message(message=None):
    """
    :param message: A dict containing the result and a user notification message
    :return: Exit with 0 or 1, or True if this is not the final output
    """
    res = message.get('result')
    if res == 'success':
        print (Fore.GREEN + message.get('message'))
        sys.exit(0)
    elif res == 'failed':
        print (Fore.RED + message.get('message'))
        sys.exit(1)
    elif res == 'continue':
        print (message.get('message'))
        return True


def add(entry_line=None, hosts_path=None, force_add=False):
    """
    Add the specified entry
    :param entry_line: The entry to add
    :param hosts_path: The path of the hosts file
    :param force_add: Replace matching any matching entries with new entry
    :return:
    """
    hosts_entry = HostsEntry.str_to_hostentry(entry_line)
    if not hosts_entry:
        output_message({'result': 'failed', 'message': '"{0}": is not a valid entry.'.format(entry_line)})

    duplicate_entry = False
    entry_to_add = False

    hosts = Hosts(hosts_path)
    add_result = hosts.add(entries=[hosts_entry], force=force_add)
    if add_result.get('replaced_count'):
        hosts.write()
        return {'result': 'success',
                'message': 'Entry added. Matching entries replaced.'}
    if add_result.get('ipv4_count') or add_result.get('ipv6_count'):
        entry_to_add = True
    if add_result.get('duplicate_count'):
        duplicate_entry = True
    if entry_to_add and not duplicate_entry:
        hosts.write()
        return {'result': 'success',
                'message': 'New entry added.'}
    if not force_add and duplicate_entry:
        return {'result': 'failed',
                'message': 'New entry matches one or more existing.'
                           '\nUse -f to replace similar entries.'}


def import_from_file(hosts_path=None, file_path=None):
    if hosts_path and not os.path.exists(hosts_path):
        return {'result': 'failed', 'message': 'Cannot read hosts file: {0}'.format(hosts_path)}
    if not os.path.exists(file_path):
        return {'result': 'failed', 'message': 'Cannot read import file: {0}'.format(file_path)}
    else:
        hosts = Hosts(path=hosts_path)
        pre_count = len(hosts.entries)
        import_file_output = hosts.import_file(import_file_path=file_path)
        post_count = len(hosts.entries)
        write_result = import_file_output.get('write_result')
        message = 'New entries:\t{0}\nTotal entries:\t{1}\n'.format(
            post_count - pre_count,
            write_result.get('total_written')
        )
    return {'result': import_file_output.get('result'),
            'message': message}


def import_from_url(hosts_path=None, url=None):
    if hosts_path and not os.path.exists(hosts_path):
        return {'result': 'failed', 'message': 'Cannot read hosts file: {0}'.format(hosts_path)}
    else:
        hosts = Hosts(path=hosts_path)
        pre_count = len(hosts.entries)
        import_url_output = hosts.import_url(url=url)
        post_count = len(hosts.entries)
        write_result = import_url_output.get('write_result')
        message = 'New entries:\t{0}\nTotal entries:\t{1}\n'.format(
            post_count - pre_count,
            write_result.get('total_written')
        )
    return {'result': import_url_output.get('result'),
            'message': message}


def remove(address_to_remove=None, names_to_remove=None, remove_from_path=None):
    """
    Remove entries matching address and/or names
    """
    hosts = Hosts(path=remove_from_path)
    remove_result = None
    write_result = False
    if address_to_remove or names_to_remove:
        remove_result = hosts.remove_all_matching(address=address_to_remove, name=names_to_remove)
        write_result = hosts.write()

    if not write_result:
        return {'result': 'failed', 'message': 'Unable to write to path: {0}'.format(hosts.hosts_path)}
    if remove_result:
        str_entry = "entry"
        if remove_result > 1:
            str_entry = 'entries'
        return {'result': 'success', 'message': 'Removed {0} {1}.'.format(remove_result, str_entry)}
    else:
        return {'result': 'failed', 'message': 'No matching entries.'.format(remove_result)}


def strip_entry_value(entry_value):
    """
    :param entry_value: value to strip spaces from
    :return: value minus the leading and trailing spaces
    """
    if isinstance(entry_value, list):
        new_list = []
        for value in entry_value:
            new_list.append(value.strip())
        return ' '.join(new_list)
    if isinstance(entry_value, str):
        return entry_value.strip()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1.0')
    entry = arguments.get('ENTRY')
    path = arguments.get('--path')
    force = arguments.get('--force')
    backup = arguments.get('--backup')
    address = arguments.get('--address')
    names = arguments.get('--names')
    input_file = arguments.get('--input-file')
    input_url = arguments.get('--input-url')

    if not path:
        if sys.platform.startswith('win'):
            path = r'c:\windows\system32\drivers\etc\hosts'
        else:
            path = '/etc/hosts'

    if not is_readable(path):
        output_message({'result': 'failed',
                        'message': 'Unable to read path: {0}.'.format(path)})

    new_entry = None
    if entry:
        new_entry = strip_entry_value(entry)

    if backup:
        result = backup_hosts(source=path)
        if result.get('result') == 'success':
            result['result'] = 'continue'
        output_message(result)

    if arguments.get('add'):
        final_message = None
        if not is_writeable(path):
            output_message({'result': 'failed',
                            'message': 'Unable to write to: {0}'.format(path)})
        if new_entry:
            result = add(entry_line=new_entry, hosts_path=path, force_add=force)
            output_message(result)
        if input_file:
            result = import_from_file(hosts_path=path, file_path=input_file)
            output_message(result)
        if input_url:
            result = import_from_url(hosts_path=path, url=input_url)
            output_message(result)
    else:
        if arguments.get('remove'):
            result = remove(address_to_remove=address, names_to_remove=names, remove_from_path=path)
            output_message(result)
