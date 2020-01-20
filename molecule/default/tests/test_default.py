import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_ood_is_installed(host):
    assert host.package("ondemand").is_installed


def test_httpd_running(host):
    httpd_process = host.process.filter(comm="httpd", user="apache")
    assert len(httpd_process) > 0


def test_ood_portal_conf(host):
    hostname = host.check_output('hostname -s')
    ood_portal_conf = '/opt/rh/httpd24/root/etc/httpd/conf.d/ood-portal.conf'

    if hostname == 'custom':
        header = '# Generated using ood-portal-generator version'
    elif hostname == 'instance':
        header = '# Ansible managed:'

    # By default use ood-portal template
    assert host.file(ood_portal_conf).contains(header)


def test_httpd_running_and_enabled(host):
    httpd = host.service("httpd24-httpd")
    assert httpd.is_running
    assert httpd.is_enabled
