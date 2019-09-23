# Open Ondemand Ansible Role

## Disclaimer

This is currently a work in progress. It may or may not work on all systems and **is not yet production ready**.
Please only use this for developmental or proof of concept purposes while we work to harden it.

It was tested on Ubuntu Bionic, Opensuse Tumbleweed 20190921, and Fedora 30.

## Getting Started

First you're going to create a new working directory and get this playbook.

```bash
mkdir ood-ansible
git clone https://github.com/OSC/ood-ansible.git roles/ondemand
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
Save all these overrides to a file in the root directory (../.. from this file).

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

### Configuring

`ansible-playbook -i inventory open-ondemand.yml --tags configure --extra-vars=@overrides.yml`

### Installing

`ansible-playbook -i inventory open-ondemand.yml --tags install --extra-vars=@overrides.yml`

### Everything except dependencies and building

`ansible-playbook -i inventory open-ondemand.yml --skip-tags="deps,build" --extra-vars=@overrides.yml`

### Only site specific tasks

`ansible-playbook -i inventory open-ondemand.yml --tags="site" --skip-tags="configure" --extra-vars=@overrides.yml`

## Toggles and advanced uses

### Using your own Passgenger/nginx stack

If you've built your own Passgener/nginx stack then set `passenger_remote_dl` to `false` and the playbook
won't download Passgenger's tars from GitHub.

It will still expect them locally in `passenger_src_dir` though, so you'll have to tar them up appropriately
with versions and so on. See [this task](tasks/passenger.yml) for more details.

## Contributing

If you run into an issue or have a feature request or fixed some issue, let us know! PRs welcome!
