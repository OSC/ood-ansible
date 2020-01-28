# Open OnDemand Ansible Role

[![Build Status](https://travis-ci.com/OSC/ood-ansible.svg?branch=master)](https://travis-ci.com/OSC/ood-ansible)

## Usage

This ansible role installs and configures [Open OnDemand](https://openondemand.org/) on various Linux distributions.

### Install from source or RPM

This role was developed for users of non RPM systems like Ubuntu, Debian or Arch because Open OnDemand does not
currently supply packages for those platforms.

There is a toggle provided `install_from_src` which is by default true. When true, this role will git pull the
Open OnDemand source code, build it (after installing dependencies) and push the resulting build to the appropriate
destination directories.

However, there is an RPM provided by the developers and if this flag is set to `false` this role will instead install
the rpm and configure the resulting installation.

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

## Site Specific tasks

You may use the file [site-specific.yml](tasks/site-specific.yml) to run site specific tasks.
This file should never be updated in this repo so are free to modify it without worry that you'll
have to merge it.

Use the command `git update-index --assume-unchanged tasks/site-specific.yml` to get rid of it
showing up all the time in git diffs.

Use the command `git update-index --no-assume-unchanged  tasks/site-specific.yml` if you do want
to start tracking it again.

## Tags

Switch to a given git tag if you want to install a specific older version from the source code.
This is because installation directories changed from 1.6.20 to 1.7.x.

### Configuring

`ansible-playbook -i inventory open-ondemand.yml --tags configure --extra-vars=@overrides.yml`

### Installing

`ansible-playbook -i inventory open-ondemand.yml --tags install --extra-vars=@overrides.yml`

### Everything except dependencies and building

`ansible-playbook -i inventory open-ondemand.yml --skip-tags="deps,build" --extra-vars=@overrides.yml`

### Only site specific tasks

`ansible-playbook -i inventory open-ondemand.yml --tags="site" --skip-tags="configure" --extra-vars=@overrides.yml`

## Toggles and advanced uses

### Using your own Passenger/nginx stack

If you've built your own Passenger/nginx stack then set `passenger_remote_dl` to `false` and the playbook
won't download Passenger's tars from GitHub.  This only applies when `install_from_src` is true.

It will still expect them locally in `passenger_src_dir` though, so you'll have to tar them up appropriately
with versions and so on. See [this task](tasks/passenger.yml) for more details.

## Contributing

If you run into an issue or have a feature request or fixed some issue, let us know! PRs welcome! Even if you
just have a question, feel free to open a ticket.
