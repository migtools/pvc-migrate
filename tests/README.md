# pvc-migrate Tests

This is a collection of tests for pvc-migrate.

## Pre-Requisites

### Prepare Kubeconfigs for Source and Destination clusters

Create source and destination kubeconfigs in the `tests` directory.

Login to your Source (3.x) cluster and save the kubeconfig in `src.config` file:

```sh
touch src.config && export KUBECONFIG=src.config

oc login -u <username> -p <password> <src_cluster_api_url>
```

Login to your Destination (4.x) cluster and save the kubeconfig in `dest.config` file:

```sh
touch dest.config && export KUBECONFIG=dest.config

oc login -u <username> -p <password> <destination_cluster_api_url>
```

### Prepare test configuration file

Copy `test-config.yml.sample` to `test-config.yml`:

```sh
cp test-config.yml.sample test-config.yml
```

This file contains configuration for different stages. Follow the comments in the file to configure your tests.


## Stage 1 tests

To run Stage 1 tests:

```sh
ansible-playbook 1_pvc_data_gen.yml
```

## Stage 2 tests

Prior to running Stage 2 tests, ensure:
* Stage 1 tests are run
* Valid Storage Class mappings are provided in `test-config.yml` 

To run Stage 2 tests:

```sh
ansible-playbook 2_pvc_destination_gen.yml
```

## Stage 3 tests

Prior to running Stage 3 tests, ensure:
* Stage 2 tests are run
* Valid SSH public and private key paths are provided in `test-config.yml` 

To run Stage 3 tests:

```sh
ansible-playbook 3_run_rsync.yml
```
