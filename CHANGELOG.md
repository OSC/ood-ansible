# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

View the [README](README#version-compatibility) for more on version compatibility.

## [Unreleased]

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

[Unreleased]: https://github.com/OSC/ood-ansible/compare/v2.0.2...HEAD
[2.0.2]: https://github.com/OSC/ondemand/compare/v2.0.1...v2.0.2
[2.0.1]: https://github.com/OSC/ondemand/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/OSC/ondemand/compare/v1.8.1...v2.0.0
[1.8.1]: https://github.com/OSC/ondemand/compare/v1.8.0...v1.8.1
