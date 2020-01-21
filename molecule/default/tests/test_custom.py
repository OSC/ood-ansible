import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')


def test_nginx_min_uid(host):
    nginx_conf = '/etc/ood/config/nginx_stage.yml'
    assert host.file(nginx_conf).contains("min_uid: 500")
