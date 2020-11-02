import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')


def test_ood_portal_conf(host):
    httpd_root = pytest.helpers.httpd_root_dir(host)
    ood_portal_conf = "{0}/etc/httpd/conf.d/ood-portal.conf".format(httpd_root)
    fixture = "fixtures/ood-portal.conf.custom.{0}".format(pytest.helpers.httpd(host))
    actual = host.file(ood_portal_conf).content_string
    expected = open(fixture, 'r').read()
    assert actual == expected