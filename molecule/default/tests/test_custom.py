import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')
apps_d = "/etc/ood/config/apps"
cluster_d = "/etc/ood/config/clusters.d"


def test_cluster_is_configured(host):
    cluster_yml = f"{cluster_d}/my_cluster.yml"
    assert host.file(cluster_d).is_directory
    assert host.file(cluster_yml).exists
    assert host.file(cluster_yml).contains("v2:")
    assert host.file(cluster_yml).contains("metadata:")
    assert host.file(cluster_yml).contains("title: my_cluster")
    assert host.file(cluster_yml).contains("login:")
    assert host.file(cluster_yml).contains("host: my_host")
    assert host.file(cluster_yml).contains("job:")
    assert host.file(cluster_yml).contains("adapter: slurm")
    assert host.file(cluster_yml).contains("bin: /usr/local")
    assert host.file(cluster_yml).contains("batch_connect:")


def test_multiple_clusters_conf(host):
    cluster_yml_1 = f"{cluster_d}/my_cluster.yml"
    assert host.file(cluster_yml_1).exists

    cluster_yml_2 = f"{cluster_d}/another_cluster.yml"
    assert host.file(cluster_yml_2).exists
    assert host.file(cluster_yml_2).contains("v2:")
    assert host.file(cluster_yml_2).contains("metadata:")
    assert host.file(cluster_yml_2).contains("title: Another Cluster")


def test_custom_nginx_stage(host):
    actual = host.file('/etc/ood/config/nginx_stage.yml').content_string
    expected = open('fixtures/nginx_stage.yml.custom', 'r').read()
    assert actual == expected


def test_ood_portal_conf(host):
    httpd_root = pytest.helpers.httpd_root_dir(host)
    ood_portal_conf = "{0}/etc/httpd/conf.d/ood-portal.conf".format(httpd_root)
    header = '# Generated using ood-portal-generator version'
    assert host.file(ood_portal_conf).contains(header)


def test_apps(host):
    assert host.file(apps_d).is_directory


def test_apps_bc_desktop_config(host):
    bc_desktop_d = f"{apps_d}/bc_desktop"
    bc_desktop_yml = f"{bc_desktop_d}/my_cluster.yml"
    assert host.file(bc_desktop_d).is_directory
    assert host.file(bc_desktop_yml).exists
    assert host.file(bc_desktop_yml).contains('title: remote desktop')
    assert host.file(bc_desktop_yml).contains("cluster: my_cluster")
    assert host.file(bc_desktop_yml).contains("attributes:")
    assert host.file(bc_desktop_yml).contains("desktop: xfce")


def test_apps_bc_desktop_submit(host):
    bc_desktop_d = f"{apps_d}/bc_desktop"
    bc_desktop_yml = f"{bc_desktop_d}/my_cluster.yml"

    submit_d = f"{bc_desktop_d}/submit"
    submit_erb = f"{submit_d}/submit.yml.erb"

    assert host.file(submit_d).is_directory
    assert host.file(submit_erb).exists
    assert host.file(submit_erb).contains('script:')
    assert host.file(submit_erb).contains('native:')
    assert host.file(submit_erb).contains("- '1'")
    assert host.file(submit_erb).contains(
        "- '<%= bc_num_slots.blank? ? 1 : bc_num_slots.to_i %>'"
    )
    assert host.file(bc_desktop_yml).contains('submit: submit/submit.yml.erb')
    assert not host.file(bc_desktop_yml).contains('script:')


def test_apps_file(host):
    files_d = f"{apps_d}/files"
    assert host.file(f"{files_d}").is_directory
    assert host.file(f"{files_d}/env").exists
    assert host.file(f"{files_d}/env").contains('OOD_SHELL="/bin/bash"')


def test_apps_dashboard(host):
    dashboard_d = f"{apps_d}/dashboard"
    assert host.file(f"{dashboard_d}").is_directory
    assert host.file(f"{dashboard_d}/env").exists
    assert host.file(f"{dashboard_d}/env").contains('MOTD_FORMAT="markdown"')
    assert host.file(f"{dashboard_d}/env").contains('OOD_DATAROOT="/mnt/newfs/$USER"')


def test_oidc_httpd_module(host):
    oidc_mod = pytest.helpers.mod_auth_openidc(host)
    assert host.package(oidc_mod).is_installed


def test_oidc_auth_openidc_conf(host):
    httpd_root = pytest.helpers.httpd_root_dir(host)
    auth_oidc_cnf = "{0}/etc/httpd/conf.d/auth_openidc.conf".format(httpd_root)

    assert host.file(auth_oidc_cnf).exists
    assert host.file(auth_oidc_cnf).contains(
        'OIDCSessionInactivityTimeout 28800'
    )
    assert host.file(auth_oidc_cnf).contains(
        'OIDCSessionMaxDuration 28888'
    )
    assert host.file(auth_oidc_cnf).contains(
        'OIDCRedirectURI https://localhost/custom-oidc-path'
    )
    assert host.file(auth_oidc_cnf).contains('OIDCClientID myid')


def test_apps_install(host):
    sys_apps_d = "/var/www/ood/apps/sys"
    jupyter_d = f"{sys_apps_d}/jupyter"

    assert host.file(jupyter_d).is_directory
    assert host.file(f"{jupyter_d}/.git/config").contains(
        "OSC/bc_example_jupyter"
    )

    customdir_d = "/var/www/ood/apps/dev/customdir"

    assert host.file(customdir_d).is_directory
    assert host.file(f"{customdir_d}/.git/config").contains(
        "OSC/bc_example_jupyter"
    )
    assert host.file(f"{customdir_d}/.git/HEAD").contains(
        "1f770d1c00be4ec281a7d016c5471d55ae28fca1"
    )

def test_custom_ood_portal(host):
    actual = host.file("/etc/ood/config/ood_portal.yml").content_string
    fixture = "fixtures/ood_portal.yml.custom.{0}".format(pytest.helpers.httpd(host))
    expected = open(fixture, 'r').read()
    assert actual == expected