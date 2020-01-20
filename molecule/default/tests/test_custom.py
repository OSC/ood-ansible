import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')


def test_cluster_is_configured(host):
    cluster_d = "/etc/ood/config/clusters.d"
    cluster_yml = f"{cluster_d}/my_cluster.yml"
    assert host.file(cluster_d).is_directory
    assert host.file(cluster_yml).exists
    assert host.file(cluster_yml).contains("v2:")
    assert host.file(cluster_yml).contains("  metadata:")
    assert host.file(cluster_yml).contains("    title: my_cluster")
    assert host.file(cluster_yml).contains("  login:")
    assert host.file(cluster_yml).contains("    host: my_host")
    assert host.file(cluster_yml).contains("  job:")
    assert host.file(cluster_yml).contains("    adapter: slurm")
    assert host.file(cluster_yml).contains("    bin: /usr/local")
    assert host.file(cluster_yml).contains("  batch_connect:")

def test_nginx_min_uid(host):
    nginx_conf = '/etc/ood/config/nginx_stage.yml'
    assert host.file(nginx_conf).contains("min_uid: 500")

def test_ood_portal_conf(host):
    ood_portal_conf = '/opt/rh/httpd24/root/etc/httpd/conf.d/ood-portal.conf'
    header = '# Generated using ood-portal-generator version'
    assert host.file(ood_portal_conf).contains(header)
