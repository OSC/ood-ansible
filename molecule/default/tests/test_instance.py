import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('instance')


def test_ood_portal_conf(host):
    ood_portal_conf = '/opt/rh/httpd24/root/etc/httpd/conf.d/ood-portal.conf'
    header = '# Ansible managed:'
    assert host.file(ood_portal_conf).contains(header)

def test_ood_portal_defaults(host):
    portal_yml = f"/etc/ood/config/ood_portal.yml"
    assert host.file(portal_yml).exists
    assert host.file(portal_yml).contains("servername: localhost")
    assert host.file(portal_yml).contains("#proxy_server: null")
    assert host.file(portal_yml).contains("port: 80")
    assert host.file(portal_yml).contains("# Default: null (no SSL support)")
    assert host.file(portal_yml).contains("logroot: \"/var/log/httpd24\"")
    assert host.file(portal_yml).contains("use_rewrites: false")
    assert host.file(portal_yml).contains("use_maintenance: false")
    assert host.file(portal_yml).contains('maintenance_ip_whitelist: \\[\\]')
    assert host.file(portal_yml).contains("lua_root: \"/opt/ood/mod_ood_proxy/lib\"")
    assert host.file(portal_yml).contains("lua_log_level: \"info\"")
    assert host.file(portal_yml).contains("user_map_cmd: '/opt/ood/ood_auth_map/bin/ood_auth_map.regex'")
    assert host.file(portal_yml).contains("#user_env: null")
    assert host.file(portal_yml).contains("#map_fail_uri: null")
    assert host.file(portal_yml).contains("pun_stage_cmd: \"sudo /opt/ood/nginx_stage/sbin/nginx_stage\"")
    assert host.file(portal_yml).contains("auth:")
    assert host.file(portal_yml).contains("- 'AuthType Basic'")
    assert host.file(portal_yml).contains("- 'AuthName \"private\"'")
    assert host.file(portal_yml).contains("- 'AuthUserFile \"/opt/rh/httpd24/root/etc/httpd/.htpasswd\"'")
    assert host.file(portal_yml).contains("- 'RequestHeader unset Authorization'")
    assert host.file(portal_yml).contains("- 'Require valid-user'")
    assert host.file(portal_yml).contains("root_uri: /pun/sys/dashboard")
    assert host.file(portal_yml).contains("#analytics: null")
    assert host.file(portal_yml).contains("public_uri: \"/public\"")
    assert host.file(portal_yml).contains("public_root: \"/var/www/ood/public\"")
    assert host.file(portal_yml).contains("logout_uri: \"/logout\"")
    assert host.file(portal_yml).contains("logout_redirect: \"/pun/sys/dashboard/logout\"")
    assert host.file(portal_yml).contains("host_regex: '\\[^/\\]+'")
    assert host.file(portal_yml).contains("#node_uri: null")
    assert host.file(portal_yml).contains("#rnode_uri: null")
    assert host.file(portal_yml).contains("nginx_uri: /nginx")
    assert host.file(portal_yml).contains("pun_uri: \"/pun\"")
    assert host.file(portal_yml).contains("pun_socket_root: \"/var/run/ondemand-nginx\"")
    assert host.file(portal_yml).contains("pun_max_retries: 5")
    assert host.file(portal_yml).contains("#oidc_uri: null")
    assert host.file(portal_yml).contains("#oidc_discover_uri: null")
    assert host.file(portal_yml).contains("#oidc_discover_root: null")
    assert host.file(portal_yml).contains("#register_uri: null")
    assert host.file(portal_yml).contains("#register_root: null")

