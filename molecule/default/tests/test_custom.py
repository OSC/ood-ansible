import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('custom')
apps_d = "/etc/ood/config/apps"


def test_cluster_is_configured(host):
    cluster_d = "/etc/ood/config/clusters.d"
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


def test_nginx_min_uid(host):
    nginx_conf = '/etc/ood/config/nginx_stage.yml'
    assert host.file(nginx_conf).contains("min_uid: 500")


def test_ood_portal_conf(host):
    ood_portal_conf = '/opt/rh/httpd24/root/etc/httpd/conf.d/ood-portal.conf'
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
    assert host.file(f"{files_d}/env").contains('OOD_SHELL=/bin/bash')


def test_apps_dashboard(host):
    dashboard_d = f"{apps_d}/dashboard"
    assert host.file(f"{dashboard_d}").is_directory
    assert host.file(f"{dashboard_d}/env").exists
    assert host.file(f"{dashboard_d}/env").contains('MOTD_FORMAT=markdown')


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
