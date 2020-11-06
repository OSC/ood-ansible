import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('templates')

def test_ood_portal_conf(host):
    httpd_root = pytest.helpers.httpd_root_dir(host)
    ood_portal_conf = "{0}/etc/httpd/conf.d/ood-portal.conf".format(httpd_root)
    header = '# Generated using ood-portal-generator version'
    assert host.file(ood_portal_conf).contains(header)