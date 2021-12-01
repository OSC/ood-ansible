# Open OnDemand Ansible Role

[![Molecule Tests](https://github.com/OSC/ood-ansible/workflows/Molecule%20Tests/badge.svg)](https://github.com/OSC/ood-ansible/actions)

This ansible role installs and configures [Open OnDemand](https://openondemand.org/) on various Linux distributions.

## Table of Contents

- [Version compatibility](#version-compatibility)
- [Installing from source](#install-from-source-or-rpm)
- [Tags](#tags)
- [Overrides](#overrides)
  - [Using this role to manage cluster and apps](#using-this-role-to-manage-cluster-and-apps)
    - [clusters](#clusters)
    - [ood_install_apps](#ood_install_apps)
    - [ood_apps](#ood_apps)
  - [Open ID Connect](#open-id-connect)
    - [Install Dex](#install-dex)
- [Using your own Passenger/nginx stack](#using-your-own-passenger/nginx-stack)
- [Contributing](#contributing)

## Version compatibility

This role's versioning will loosely follow the Open OnDemand versions it installs. The Major and
minor versions of this role will be compatible with the corresponding major and minor versions of
Open OnDemand.  Patch releases in this role will be compatible with the version of Open OnDemand
it installs and configures but provide bug fixes or new features.

As an example 1.8.0 of this role will be compatible with versions of Open OnDemand 1.8.x (which is currently 1.8.20).
Version 1.8.1 of this role will still install version 1.8.20 of Open OnDemand but provide some bug fixes or
new features to _this role_.

## Install from source or RPM

This role was developed for users of non RPM systems like Ubuntu, Debian or Arch because Open OnDemand does not
currently supply packages for those platforms.

There is a toggle provided `install_from_src` which is by default false. When true, this role will git pull the
Open OnDemand source code, build it (after installing dependencies) and push the resulting build to the appropriate
destination directories.

It's also important to note the `ood_source_version` configuration. This sets what branch or tag to pull the source
code from. `master` maybe be unstable, while a `release_` branch is much more so. Tags like `v1.8.20` should work best.

The default behavior is to install the rpm and configure the resulting installation and skip a lot of these tasks
that build the source code.

## Installing a specific version

`ondemand_package` defaults to `latest` meaning this will install the latest version on the versioned
yum/deb repository. For example, it'll install the latest version, 2.0.20 from the versioned 2.0 yum
repo.

We use `ondemand_package` for the `name` paramter of the [ansible yum](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/yum_module.html)
so you can speicify a specific version with `ondemand-2.0.20` or use the comparison operators
ansible supports.

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

This configuration writes its content to `/etc/ood/config/clusters.d/<cluster_key>.yml` for each cluster item on this dict.

For example

```yaml
clusters:
  my_cluster:
    v2:
      metadata:
        title: my_cluster
      login:
        host: my_host
      job:
        adapter: slurm
        bin: /usr/local
      batch_connect:
  another_cluster:
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

To install dex for OIDC use set the flag `install_ondemand_dex` to true and it will install the RPM.

## Using your own Passenger/nginx stack

If you've built your own Passenger/nginx stack then set `passenger_remote_dl` to `false` and the playbook
won't download Passenger's tars from GitHub.  This only applies when `install_from_src` is true.

It will still expect them locally in `passenger_src_dir` though, so you'll have to tar them up appropriately
with versions and so on. See [this task](tasks/passenger.yml) for more details.

## Contributing

If you run into an issue or have a feature request or fixed some issue, let us know! PRs welcome! Even if you
just have a question, feel free to open a ticket.
