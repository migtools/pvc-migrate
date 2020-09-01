# pvc-migrate Tests

This is a collection of tests for pvc-migrate.

## Pre-Requisites

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

## Stage 1 tests


## Stage 2 tests


## Stage 3 tests
