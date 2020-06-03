# Open OnDemand Ansible Role

[![Build Status](https://travis-ci.com/OSC/ood-ansible.svg?branch=master)](https://travis-ci.com/OSC/ood-ansible)

## Usage

This ansible role installs and configures [Open OnDemand](https://openondemand.org/) on various Linux distributions.

### Install from source or RPM

This role was developed for users of non RPM systems like Ubuntu, Debian or Arch because Open OnDemand does not
currently supply packages for those platforms.

There is a toggle provided `install_from_src` which is by default false. When true, this role will git pull the
Open OnDemand source code, build it (after installing dependencies) and push the resulting build to the appropriate
destination directories.

The default behavior is to install the rpm and configure the resulting installation and skip a lot of these tasks
that build the source code.

## Getting Started

First pull this repo into where you keep your roles.  Shown is the `.ansible` folder in your home directory.

```bash
git clone https://github.com/OSC/ood-ansible.git ~/.ansible/roles/ondemand
```

### Simple playbook

Now you can make a simple playbook

```yml
# open-ondemand.yml
- hosts: ondemand-hosts

  roles:
  - ondemand
```

## Overrides

Look at all the variables in [the defaults](defaults/main.yml) and override any of them that you wish or need to.
Save all these overrides to a file that you can then call with `--extra-vars=@overrides.yml`

## Make an inventory file

Make an inventory file of all the hosts you want to install on, like so.

```toml
# inventory
[ondemand-host]
my-cool-site.net
```

## Running

To run simply run the ansible playbook command with all the other files you've just created.

`ansible-playbook -i inventory open-ondemand.yml --extra-vars=@overrides.yml`

## Tags

Switch to a given git tag if you want to install a specific older version from the source code.
This is because installation directories changed from 1.6.20 to 1.7.x.

### Configuring

`ansible-playbook -i inventory open-ondemand.yml --tags configure --extra-vars=@overrides.yml`

### Installing

`ansible-playbook -i inventory open-ondemand.yml --tags install --extra-vars=@overrides.yml`

### Everything except dependencies and building

`ansible-playbook -i inventory open-ondemand.yml --skip-tags="deps,build" --extra-vars=@overrides.yml`

## Toggles and advanced uses

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

More details can be found on [Open OnDemand documentation](https://osc.github.io/ood-documentation/master/installation/add-cluster-config.html) and [Cluster Config Schema v2](https://osc.github.io/ood-documentation/master/installation/cluster-config-schema.html).

#### `ood_install_apps`

This configuration installs applications from custom repositories into the apps directory (default or custom).
It accepts a dictionary like those of [git module](https://docs.ansible.com/ansible/latest/modules/git_module.html).
The main key is the resulting directory name where `repo` is cloned under the `dest` directory.

Only `repo:` is required.

##### ood\_install\_apps example

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

* clone `OSC/bc_example_jupyter` to `/var/www/ood/apps/sys/jupyter`
* clone `OSC/bc_example_rstudio` to `/var/www/ood/apps/my/dir/customdir`

#### `ood_apps`

This allows you to configure the `bc_desktop` application and write environment files for other applications.

In the simplest case, when given an `env` key it will write out key value pairs an env file.

In the more complex case of `bc_desktop`, it writes its content to a `<cluster>.yml` file (where the filename is
the `cluster` attribute of the content) _and_ writes the the content of `submit` key to the `submit.yml.erb` file.

The examples below should illustrate these two points.

##### ood\_apps example

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

#### `ood_auth_openidc`

This variable [configures Apache for mod_auth_openidc](https://osc.github.io/ood-documentation/master/authentication/tutorial-oidc-keycloak-rhel7/install_mod_auth_openidc.html#add-keycloak-config-to-ondemand-apache-for-mod-auth-openidc)

##### Example

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

### Using your own Passenger/nginx stack

If you've built your own Passenger/nginx stack then set `passenger_remote_dl` to `false` and the playbook
won't download Passenger's tars from GitHub.  This only applies when `install_from_src` is true.

It will still expect them locally in `passenger_src_dir` though, so you'll have to tar them up appropriately
with versions and so on. See [this task](tasks/passenger.yml) for more details.

## Contributing

If you run into an issue or have a feature request or fixed some issue, let us know! PRs welcome! Even if you
just have a question, feel free to open a ticket.
