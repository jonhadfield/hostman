# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'python-hosts')))
from hostman import output_message, import_from_file, import_from_url, add, backup_hosts, strip_entry_value, remove
import pytest


def test_output_message_with_failed():
    with pytest.raises(SystemExit) as cm:
        output_message({'result': 'failed', 'message': 'test failed'})
    assert cm.value.code == 1


def test_output_message_with_failed():
    with pytest.raises(SystemExit) as cm:
        output_message({'result': 'failed', 'message': 'test failed'})
    assert cm.value.code == 1


def test_output_message_with_success():
    with pytest.raises(SystemExit) as cm:
        output_message({'result': 'success', 'message': 'test success'})
    assert cm.value.code == 0


def test_add_add_duplicate_ipv4_host_with_force(tmpdir):
    """
    Test that an ipv4 type host is replaced with force set
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("3.4.5.6\tlocalhost\n")
    new_entry = '3.4.5.6 bob jane.com'
    output = add(entry_line=new_entry, hosts_path=hosts_file.strpath, force_add=True)
    assert output.get('result') == 'success'
    assert output.get('message').startswith('Entry added. Matching entries replaced.')


def test_import_hosts_with_invalid_hosts_path(tmpdir):
    """
    Test the import of a file where the hosts path is invalid
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("3.4.5.6\tlocalhost\n")
    import_file = tmpdir.mkdir("tmp").join("in")
    import_file.write("8.8.8.8\tgoogledns\n")
    result = import_from_file(hosts_path='invalid',
                              file_path=import_file.strpath)
    assert result.get('message').startswith('Cannot read hosts file:')


def test_import_hosts_with_invalid_import_file_path(tmpdir):
    """
    Test the import of a file where the import file path is invalid
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("3.4.5.6\tlocalhost\n")
    import_file = tmpdir.mkdir("tmp").join("in")
    import_file.write("8.8.8.8\tgoogledns\n")
    result = import_from_file(hosts_path=hosts_file.strpath,
                              file_path='invalid')
    assert result.get('message').startswith('Cannot read import file:')


def test_add_duplicate_ipv4_host_without_force(tmpdir):
    """
    Test that nothing is added when attempt to replace a similar
    entry without using force option
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("9.9.9.9\tgeorge\n")
    new_entry = '9.9.9.9 george bungle.com'
    output = add(entry_line=new_entry, hosts_path=hosts_file.strpath, force_add=False)
    assert output.get('result') == 'failed'
    assert output.get('message').startswith('New entry matches')


def test_add_new_ipv4_host(tmpdir):
    """
    Test successful addition of an ipv4 host
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    new_entry = '3.4.5.6 bob jane.com'
    output = add(entry_line=new_entry, hosts_path=hosts_file.strpath, force_add=False)
    assert output.get('result') == 'success'


def test_backup_hosts_file(tmpdir):
    """
    Test hosts file backup
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    test_extension = 'test'
    output = backup_hosts(source=hosts_file.strpath, extension=test_extension)
    assert 'Backup written to:' in output.get('message')


def test_backup_hosts_file_fails_with_invalid_source(tmpdir):
    """
    Test backup fails with an invalid source
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    output = backup_hosts(source="invalid")
    assert 'Cannot create backup file:' in output.get('message')


def test_failure_with_invalid_host_entry():
    with pytest.raises(SystemExit) as cm:
        add(entry_line='256.255.255.255 badaddr.com')
    assert cm.value.code == 1


# def test_output_message_with_failure():
#    with pytest.raises(SystemExit) as cm:
#       hostman.output_message({'result': 'failed', 'message': 'test failure'})
#    assert cm.value.code == 1


# def test_output_message_with_failure():
#    with pytest.raises(SystemExit) as cm:
#        hostman.output_message({'result': 'failed', 'message': 'test failure'})
#    assert cm.value.code == 1


# def test_output_message_with_success():
#    with pytest.raises(SystemExit) as cm:
#        hostman.output_message({'result': 'success', 'message': 'test success'})
#    assert cm.value.code == 0


def test_output_message_with_continue():
    assert output_message({'result': 'continue', 'message': 'test continue'})


def test_import_hosts_from_file(tmpdir):
    """
    Test the import of a file
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    import_file = tmpdir.mkdir("tmp").join("in")
    import_file.write("8.8.8.8\tgoogledns\n")
    assert import_from_file(hosts_path=hosts_file.strpath,
                            file_path=import_file.strpath)


def test_import_hosts_from_url(tmpdir):
    """
    Test the import of a url
    """
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("127.0.0.1\tlocalhost\n")
    import_url = "https://dl.dropboxusercontent.com/u/167103/hosts"
    assert import_from_url(hosts_path=hosts_file.strpath, url=import_url)


def test_removal_of_entry(tmpdir):
    hosts_file = tmpdir.mkdir("etc").join("hosts")
    hosts_file.write("15.15.15.15\texample.com\n16.16.16.16\ttest.com\n")
    assert remove(address_to_remove='15.15.15.15', remove_from_path=hosts_file.strpath)


def test_stripping():
    string_with_spaces = " test "
    list_string_with_spaces = [" example.com ", "example "]
    assert strip_entry_value(list_string_with_spaces) == 'example.com example'
    assert strip_entry_value(string_with_spaces) == 'test'
