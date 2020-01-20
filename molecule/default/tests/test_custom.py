import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')


def test_ood_portal_conf(host):
    ood_portal_conf = '/opt/rh/httpd24/root/etc/httpd/conf.d/ood-portal.conf'
    header = '# Generated using ood-portal-generator version'
    assert host.file(ood_portal_conf).contains(header)
