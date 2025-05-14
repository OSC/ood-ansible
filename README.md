# Open OnDemand Ansible Role

[![Molecule Tests](https://github.com/OSC/ood-ansible/workflows/Molecule%20Tests/badge.svg)](https://github.com/OSC/ood-ansible/actions)

This ansible role installs and configures [Open OnDemand](https://openondemand.org/) on various Linux distributions.

## Table of Contents

- [Version compatibility](#version-compatibility)
- [Tags](#tags)
- [Overrides](#overrides)
  - [Using this role to manage cluster and apps](#using-this-role-to-manage-cluster-and-apps)
    - [clusters](#clusters)
    - [ood_install_apps](#ood_install_apps)
    - [ood_apps](#ood_apps)
  - [Open ID Connect](#open-id-connect)
    - [Install Dex](#install-dex)
  - [OnDemand.d Configurations](#ondemandd-configurations)
- [Contributing](#contributing)

## Version compatibility

This role's versioning will loosely follow the Open OnDemand versions it installs. The Major and
minor versions of this role will be compatible with the corresponding major and minor versions of
Open OnDemand.  Patch releases in this role will be compatible with the version of Open OnDemand
it installs and configures but provide bug fixes or new features.

As an example 1.8.0 of this role will be compatible with versions of Open OnDemand 1.8.x (which is currently 1.8.20).
Version 1.8.1 of this role will still install version 1.8.20 of Open OnDemand but provide some bug fixes or
new features to _this role_.

## Supported Operating Systems
* CentOS
* Debian
* Fedora
* RedHat
* Rocky Linux
* Suse
* Ubuntu 18
* Ubuntu 20

## Installing a specific version

The `ondemand_package` variable controls the version of the rpm/dep package installed. The default value of `ondemand` will install the latest version from the relevant repository, but will not upgrade an
existing installation. You can install a specific version using the full package name (e.g. `ondemand-3.0.3`) or use the comparison operators supported by the `name` parameter of the ansible [yum](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_module.html)
or [apt](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/apt_module.html) modules. Use `latest` to upgrade an existing installation.

### Installing from latest or nightly

If you'd like to install a package from our `latest` or `nightly` repositories simply change the
`rpm_repo_url` configuration to download the appropriate RPM. For example
`'https://yum.osc.edu/ondemand/latest/ondemand-release-web-latest-1-6.noarch.rpm'`. **Check yum
for the correct version of this RPM.**

When installing packages from latest or nightly you may have to exclude packages depending on the
state of project.  As an example, when developing 2.1, 2.0 RPMs on latest or nightly
need to exclude packages.

Use `ondemand_package_excludes` to specify a list of packages to exclude during the yum install.
Here's an example to exclude all `2.1` packages when installing `2.0.20`.

```yaml
ondemand_package: 'ondemand-2.0.20'
ondemand_package_excludes:
  - '*-2.1'
```

## Tags

This role has these tags when you want to only run certain tasks.

- configure - will configure Open OnDemand and any apps
- install - will install Open OnDemand and any apps
- deps - install dependencies (only valid when building from source)
- build - build the source code (only valid when building from source)

## Overrides

[The defaults directory](defaults/main) has configurations broken out by which file they apply
to when configuring or options during building from source or installation.

Check these files for variables you can override.  Save all these overrides to a file that
you can then call with `--extra-vars=@overrides.yml`

All the default files are grouped by what they apply to. Some files are for documentation purposes
and only have comments. They're hidden for ansible 2.9.X compatability and
[this error loading empty files](https://github.com/OSC/ood-ansible/issues/121).

* `.apps.yml` - configurations for installing apps (hidden because it's emtpy).
* `build.yml` - configurations for building OnDemand from the source.
* `install.yml` - configurations for installing OnDemand.
* `nginx_stage.yml` - configurations that apply to `/etc/ood/config/nginx_stage.yml`
* `.ondemand.yml` - configurations that apply to `/etc/ood/config/ondemand.d/ondemand.yml` (hidden because it's empty).
* `ood_portal.yml` - configurations that apply to `/etc/ood/config/ood_portal.yml`

### Using this role to manage cluster and apps

There are a few variables in this role that enable Open OnDemand customizations
and configuration.

#### `clusters`

This configuration writes its content to `/etc/ood/config/clusters.d/<cluster_key>.yml`
for each cluster item on this dictionary.  Each dictionary item is a multiline string.

For example

```yaml
clusters:
  my_cluster: |
    ---
    v2:
      metadata:
        title: my_cluster
      login:
        host: my_host
      job:
        adapter: slurm
        bin: /usr/local
      batch_connect:
        basic:
          script_wrapper: "module restore\n%s"
  another_cluster: |
    ---
    v2:
      metadata:
        title: Another Cluster
```

Will produce `/etc/ood/config/clusters.d/my_cluster.yml` and `/etc/ood/config/clusters.d/another_cluster.yml` with the exact content.

##### my_cluster.yml

```yaml
v2:
  metadata:
    title: my_cluster
  ...
```

##### another_cluster.yml

```yaml
v2:
  metadata:
    title: Another Cluster
```

More details can be found on [Open OnDemand documentation](https://osc.github.io/ood-documentation/latest/installation/add-cluster-config.html)
and [Cluster Config Schema v2](https://osc.github.io/ood-documentation/latest/installation/cluster-config-schema.html).

#### `ood_install_apps`

This configuration installs applications from custom repositories into the apps directory (default or custom).
It accepts a dictionary like those of [git module](https://docs.ansible.com/ansible/latest/modules/git_module.html).
The main key is the resulting directory name where `repo` is cloned under the `dest` directory.

Only `repo:` is required.

##### ood_install_apps example

```yaml
ood_install_apps:
  jupyter:
    repo: https://github.com/OSC/bc_example_jupyter.git
    dest: "{{ ood_sys_app_dir }}"  # defaults (optional)
    version: master                # defaults (optional)
  customdir: # will create /var/www/ood/apps/my/dir/customdir
    repo: https://github.com/OSC/bc_example_rstudio
    dest: /var/www/ood/apps/my/dir
    version: v1.0.1
```

The above example will

- clone `OSC/bc_example_jupyter` to `/var/www/ood/apps/sys/jupyter`
- clone `OSC/bc_example_rstudio` to `/var/www/ood/apps/my/dir/customdir`

#### `ood_apps`

This allows you to configure the `bc_desktop` application and write environment files for other applications.

In the simplest case, when given an `env` key it will write out key value pairs an env file.

In the more complex case of `bc_desktop`, it writes its content to a `<cluster>.yml` file (where the filename is
the `cluster` attribute of the content) _and_ writes the the content of `submit` key to the `submit.yml.erb` file.

The examples below should illustrate these two points.

##### ood_apps example

```yaml
ood_apps:
  bc_desktop:
    title: "xfce desktop"
    cluster: "my_cluster"
    form:
      - desktop
      - hours
    attributes:
      hours:
        value: 1
      desktop: "xfce"
    submit: |
      ---
      script:
        native:
          - "-t"
          - "<%= '%02d:00:00' % hours %>"
  files:
    env:
      ood_shell: /bin/bash
```

The above example will create

```text
/etc/ood/config
└── apps
    ├── bc_desktop
    │   ├── my_cluster.yml
    │   └── submit
    │       └── submit.yml.erb
    └── files
        └── env
```

`env` produce a `key=value` file.  Note the capitalization of the keys.

```bash
$ cat /etc/ood/config/apps/files/env
OOD_SHELL=/bin/bash
```

`submit` create _submit_ directory with a `submit.yml.erb` containing the
raw string data you've configured. Note that configuration is raw data and
not yaml like the other configurations. This is to support Ruby ERB templating
that is not easily formatted when read by Ansible as yaml.

```bash
$ cat /etc/ood/config/apps/bc_desktop/submit/submit.yml.erb
---
script:
  native:
    - "-t"
    - "<%= '%02d:00:00' % hours %>"

$ cat /etc/ood/config/apps/bc_desktop/submit/my_cluster.yml
title: "remote desktop"
cluster: my_cluster
attributes:
  hours:
    value: 1
  desktop: "xfce"
```

### Open Id Connect

There are two ways you can [configure Apache for mod_auth_openidc](https://osc.github.io/ood-documentation/latest/authentication/tutorial-oidc-keycloak-rhel7/install_mod_auth_openidc.html#add-keycloak-config-to-ondemand-apache-for-mod-auth-openidc)

The first and simplest is by using the `ood_auth_openidc` dictionary to generate a separate config file
for OIDC related configs.

The second is to have ood-portal-generator write the OIDC configs directly into the `ood-portal.conf`
file by using the named `oidc_*` variables like `oidc_provider_metadata_url` and `oidc_client_id`.
You can view [the oidc defaults](defaults/main.yml#L235) to see a full list available.
If you're using the ansible template to generate `ood-portal.conf` then you'll need the extra
flag `oidc_settings_samefile` set to true.

#### ood_auth_openidc example

```yaml
ood_auth_openidc:
  OIDCSessionMaxDuration: 28888
  OIDCClientID: myid
  OIDCProviderMetadataURL: https://localhost/
  OIDCCryptoPassphrase: mycryptopass
  "LDAPTrustedGlobalCert CA_BASE64": /etc/ssl/my/cert/path

default_auth_openidc:
  OIDCRedirectURI: "https://{{ servername }}{{ oidc_uri }}"
  OIDCSessionInactivityTimeout: 28800
  OIDCSessionMaxDuration: 28800
  OIDCRemoteUserClaim: preferred_username
  OIDCPassClaimsAs: environment
  OIDCStripCookies: mod_auth_openidc_session mod_auth_openidc_session_chunks mod_auth_openidc_session_0 mod_auth_openidc_session_1
```

It produces an `auth_openidc.conf` file with listed `key value` merged with default values.
Values defined on `ood_auth_openidc` overwrites any `default_auth_openidc` values.

See [auth\_openidc](https://github.com/zmartzone/mod_auth_openidc) for more information on that module.

#### Install Dex

To install dex for OIDC use set the flag `install_ondemand_dex` to true and it will install the package.
You can use the `ondemand_dex_service_state` and `ondemand_dex_service_enabled` variables in [default/main/install.yml](defaults/main/install.yml#L43) to set the state of the service (default: started / enabled).

### OnDemand.d Configurations

In the 4.0 release of this role, configurations for `ondemand.d` files was changed.
While this role will continue to support the old way of specifing each
variable and writing them all out to a single `ondemand.d/ondemand.yml` file,
users should begin to migrate to the new way to write these files.

4.0 introduced `ood_ondemand_d_configs` which will in turn write out as many files
as you've provided.

Each configuration at a minimum needs `content` which will be the content of
the file that's begin written. It can additionally accept ``group`` and ``mode``
to set the file's group ownership and file access mode. These files are always
owned by the ``root`` user.

In this example, we're writing out two files, ``motd.yml`` and ``globus.yml``.
These filenames are given by the top level keys under ``ood_ondemand_d_configs``.

``content`` specifies the content of the file that's going to be written out.
This should be in YAML and will be written out in YAML.

In this configuration ``motd.yml`` will be written out with ``644 root:root``
permissions.  ``globus.yml`` on the other hand will be written out with
``640 root:specialusers`` permissions so it'll only be available for certain
users.

```yaml
ood_ondemand_d_configs:
  motd:
    content:
      motd_render_html: true
  globus:
    content:
      globus_endpoints:
        - path: "<%= CurrentUser.home %>"
          endpoint: "716de4ac-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          endpoint_path: "/"

        - path: "/project"
          endpoint: "9f1fe759-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          endpoint_path: "/"
    group: specialusers
    mode: 640
```

## Contributing

If you run into an issue or have a feature request or fixed some issue, let us know! PRs welcome! Even if you
just have a question, feel free to open a ticket.
