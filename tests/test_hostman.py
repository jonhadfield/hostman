# -*- coding: utf-8 -*-
import sys
import os
print sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hostman')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'hosts')))
print sys.path
import pytest
from hosts import Hosts, HostsEntry, exception, utils
import hostman


def test_add_single_ipv4_host(tmpdir):
    """
    Test the addition of an ipv4 host succeeds
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    new_entry = '3.4.5.6 bob jane.com'
    assert  hostman.add(entry=new_entry, path=hosts_file.strpath)
    #hosts = Hosts(path=hosts_file.strpath)
    #entry_to_check = HostsEntry.str_to_hostentry('3.4.5.6 bob jane')
    #exists_result = hosts.exists(entry_to_check)
    #assert exists_result.get('address_matches') == 1
    #assert exists_result.get('name_matches') == 1


def test_backup_hosts_file(tmpdir):
    """
    Test hosts file backup
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    test_extension = 'test'
    assert hostman.backup_hosts(source=hosts_file.strpath, extension=test_extension)
    #backup_path_split = hosts_file.strpath.split('/')
    #new_filename = ".{0}.{1}".format(backup_path_split[-1], test_extension)
    #backup_path_split[-1] = new_filename
    #backup_path = "/".join(backup_path_split)
    #hosts = Hosts(path=backup_path)
    #assert hosts.count('127.0.0.1\tlocalhost\n').get('address_matches') == 1


def test_backup_hosts_file_fails_with_invalid_source(tmpdir):
    """
    Test backup succeeds with valid source and fails with non-existant source
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    with pytest.raises(Exception):
        hostman.backup_hosts(source="invalid")


def test_output_message_fails_without_dict():
    assert hostman.output_message(message={'result': 'success', 'message:': 'succeeded'})
    assert not hostman.output_message(message='success')


def test_import_hosts_from_file(tmpdir):
    """
    Test the import of a file
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    import_file = tmpdir.mkdir("tmp").join("in")
    import_file.write("8.8.8.8\tgoogledns\n")
    assert hostman.import_from_file(hosts_path=hosts_file.strpath,
                                    file_path=import_file.strpath)
    #hosts = Hosts(path=hosts_file.strpath)
    #assert hosts.count('8.8.8.8 googledns').get('address_matches') == 1


def test_import_hosts_from_url(tmpdir):
    """
    Test the import of a url
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    import_url = "https://dl.dropboxusercontent.com/u/167103/hosts"
    assert hostman.import_from_url(hosts_path=hosts_file.strpath, url=import_url)
    #hosts = Hosts(path=hosts_file.strpath)
    #assert hosts.count('66.66.66.66 example.com example').get('name_matches') == 1


def test_removal_of_entry(tmpdir):
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("15.15.15.15\texample.com\n16.16.16.16\ttest.com\n")
    assert hostman.remove(address='15.15.15.15', path=hosts_file.strpath)
    #hosts = Hosts(path=hosts_file.strpath)
    #assert hosts.count('15.15.15.15 example.com').get('name_matches') == 0
    #assert hosts.count('16.16.16.16 test.com').get('name_matches') == 1


def test_stripping():
    string_with_spaces = " test "
    list_string_with_spaces = [" example.com ", "example "]
    assert hostman.strip_entry_value(list_string_with_spaces) == 'example.com example'
    assert hostman.strip_entry_value(string_with_spaces) == 'test'


#def test_import_hosts_from_url_counters(tmpdir):
#    """
#    Test the import of a url
#    """
#    hosts_file = tmpdir.mkdir("etc").join("hosts")
#    hosts_file.write("127.0.0.1\tlocalhost\n")
#    import_url = "https://dl.dropboxusercontent.com/u/167103/hosts"
#    result = hostman.import_from_url(hosts_path=hosts_file.strpath, url=import_url)
#    print result
#    #hosts = Hosts(path=hosts_file.strpath)
#    #assert hosts.count('66.66.66.66 example.com example').get('name_matches') == 1
#    assert 0
