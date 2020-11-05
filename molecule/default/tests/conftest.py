import pytest

pytest_plugins = ['helpers_namespace']

@pytest.helpers.register
def httpd(host):
    if rhel_7(host):
        return "httpd24-httpd"
    else:
        return "httpd"

@pytest.helpers.register
def httpd_root_dir(host):
    if rhel_7(host):
        return "/opt/rh/httpd24/root"
    else:
        return ""

@pytest.helpers.register
def httpd_log_dir(host):
    if rhel_7(host):
        return "/var/log/httpd24"
    else:
        return "/var/log/httpd"

@pytest.helpers.register
def mod_auth_openidc(host):
    if rhel_7(host):
        return "httpd24-mod_auth_openidc"
    else:
        return "mod_auth_openidc"

def rhel_7(host):
    dist = host.system_info.distribution
    release = host.system_info.release
    if (dist == 'redhat' or dist == 'centos') and float(release) < 8.0:
        return True
    else:
        return False
