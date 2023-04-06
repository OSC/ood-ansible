# Changelog

All notable changes to this project will be documented in this file.

The format is keeps the same versions as upstream OnDemand.  See
[the README's version compatability](README.md#version-compatibility) for details.

## [3.0.1] - 2023-04-06

### Added

- Support for EL9 in [184](https://github.com/OSC/ood-ansible/pull/184).
- Support for `server_aliases` in [186](https://github.com/OSC/ood-ansible/pull/186).

### Changed

- `maintenance_ip_whitelist` is now `maintenance_ip_allowlist` in
  [185](https://github.com/OSC/ood-ansible/pull/185).

## [3.0.0] - 2023-04-04

- `install_from_src` has been deprecated. This feature will not receive updates and the option 
  will be removed in future versions.
- `ood_portal_generator` set to `false` has been deprecated. This feature will not receive updates and
  the option will be removed in future versions.
- The default package is now OnDemand 3.0.0 with `ruby_version` updated to 3.0 to meet it's dependencies
  in [182](https://github.com/OSC/ood-ansible/pull/182).
- `cluster` definitions have changed from an object to a multiline string in
  [143](https://github.com/OSC/ood-ansible/pull/143). The [cluster examples](README.md#clusters)
  have been updated as well.


## [2.0.6] - 2022-08-12

### Changed

- Better error messaging for unsupported OSes in [152](https://github.com/OSC/ood-ansible/pull/152).

### Added

- Added support for 2.0 to install .deb files for Ubuntu 18.04 and 20.04 in [157](https://github.com/OSC/ood-ansible/pull/157).
- nginx_stage options `passenger_pool_idle_time` and `passenger_options` in [164](https://github.com/OSC/ood-ansible/pull/164).
- ood_portal option `dex_uri` in [166](https://github.com/OSC/ood-ansible/pull/166).

## [2.0.5] - 2022-02-08

### Added

- Support for Rocky Linux 8 in [133](https://github.com/OSC/ood-ansible/pull/133).
- Support for app initializers in [135](https://github.com/OSC/ood-ansible/pull/135).

### Fixed

- Debian build task now polls for better wait times in [137](https://github.com/OSC/ood-ansible/pull/137).

## [2.0.4] - 2021-12-01

### Added

- This role can now specify the ondemand version to install in [131](https://github.com/OSC/ood-ansible/pull/131).  
  Meaning sites can now pull RPMs safely from the latest or nightly repo.

## [2.0.3] - 2021-08-17

### Fixed

- Ansible 2.9.x can correctly read empty default files in [121](https://github.com/OSC/ood-ansible/pull/121).

## [2.0.2] - 2021-08-02

### Fixed

- OIDC parameters in [117](https://github.com/OSC/ood-ansible/pull/117)
- Ubuntu sudo rules in [119](https://github.com/OSC/ood-ansible/pull/119)

## [2.0.1] - 2021-06-14

### Fixed

- `pun_pre_hook_root_cmd` bug in ood_portal.yml.j2 in [111](https://github.com/OSC/ood-ansible/pull/111)

## [2.0.0] - 2021-06-04

### Added

- Functionality for Open OnDemand 2.0 in these pull requests:
  - [100](https://github.com/OSC/ood-ansible/pull/100) to initialize 2.0 RPMs.
  - [101](https://github.com/OSC/ood-ansible/pull/101) to add 2.0 to Ubuntu.
  - [102](https://github.com/OSC/ood-ansible/pull/102) added support for `user_map_match`.
  - [105](https://github.com/OSC/ood-ansible/pull/105) added support for `ondemand.d` directories & files.
  - [108](https://github.com/OSC/ood-ansible/pull/108) added support for `pun_pre_hook`.

### Changed

- [106](https://github.com/OSC/ood-ansible/pull/106) refactored default files into many separate
  files.  Not a breaking change, just structural reformatting.

## [1.8.1] - 2021-04-30

### Fixed

- Fixed a bug with debain's running `update_ood_portal` - [60](https://github.com/OSC/ood-ansible/pull/60) -
  in [94](https://github.com/OSC/ood-ansible/pull/94)

### Added

- Tests for Debian & Ubuntu platforms in [94](https://github.com/OSC/ood-ansible/pull/94)
- Fixed Ubuntu/20 support in [94](https://github.com/OSC/ood-ansible/pull/94)

### Changed

## 1.8.0 - 2021-04-14

- Initial release that works well

[Unreleased]: https://github.com/OSC/ood-ansible/compare/v3.0.1...HEAD
[3.0.1]: https://github.com/OSC/ondemand/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.com/OSC/ondemand/compare/v2.0.6...v3.0.0
[2.0.6]: https://github.com/OSC/ondemand/compare/v2.0.5...v2.0.6
[2.0.5]: https://github.com/OSC/ondemand/compare/v2.0.4...v2.0.5
[2.0.4]: https://github.com/OSC/ondemand/compare/v2.0.3...v2.0.4
[2.0.3]: https://github.com/OSC/ondemand/compare/v2.0.2...v2.0.3
[2.0.2]: https://github.com/OSC/ondemand/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/OSC/ondemand/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/OSC/ondemand/compare/v1.8.1...v2.0.0
[1.8.1]: https://github.com/OSC/ondemand/compare/v1.8.0...v1.8.1
