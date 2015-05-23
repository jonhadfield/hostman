# -*- coding: utf-8 -*-
import sys
import os
print sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'hosts')))
print sys.path
import pytest
from hosts import Hosts, HostsEntry, exception, utils

#def test_add_single_ipv4_host_by_detection(tmpdir):
#    """
#    Test the addition of an ipv4 host succeeds
#    """
#    hosts_file = tmpdir.mkdir("etc").join("hosts")
#    hosts_file.write("127.0.0.1\tlocalhost\n")
#    hosts = Hosts(path=hosts_file.strpath)
#    new_entry = '3.4.5.6 bob jane.com'
#    hosts.add(entry=new_entry, force=False)
#    assert hosts.count(new_entry).get('address_matches') == 1
