# Development and release

The default branch is `master`. This repository contains the Python package and PyO3 bindings; the Rust core is maintained in [aliyun-log-rust-sdk](https://github.com/aliyun/aliyun-log-rust-sdk).

## Build and test

From the repository root, with Python 3.8+ and a Rust toolchain:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install 'maturin>=1.14,<2'
maturin develop --extras test
python -m pytest tests
```

CI helper tests use Python 3.12+ and Node.js:

```sh
python -m unittest discover -s ci -p 'test_*.py'
node --test ci/test_build_status.cjs
```

## Rust dependencies

`Cargo.toml` pins the published Rust Producer and client versions. Commit `Cargo.lock` and update these dependencies explicitly when upgrading the Rust core. Run the Python tests and wheel checks before releasing an upgrade. Python and Rust package versions are independent.

For local development against unpublished Rust changes, use a local Cargo patch override. Do not include local paths in release configuration.

## CI and release

`python.yml` runs the Python build and test matrix on pull requests and pushes to `master`. Documentation-only changes run the CI helper checks and skip wheel builds. The `Python CI` summary job always runs and can be required by branch protection. Rust-only changes in the Rust repository do not trigger this workflow. `python-release.yml` builds the complete wheel matrix and sdist; `python-build-status.yml` publishes release build badges in this repository.

Before publishing, configure the GitHub environment `release-python` and its `PYPI_PASSWORD` secret with a token permitted to upload `aliyun-log-producer`. Allow deployment from branch `master` and tags matching `v*`. Preserve any required environment approval rules. This configuration is specific to the new repository.

Update the package version in `Cargo.toml`, then push a matching `v<VERSION>` tag to build and publish. For example, Cargo version `0.1.2` uses tag `v0.1.2`. Published PyPI versions cannot be replaced; use a new version if that version already exists.

A manual release dispatch with an empty `draft_version` builds artifacts only. A matching `draft_version` creates a draft GitHub release without uploading to PyPI.

## Related documents

- [Platform support](platforms.md)
