# Data Generator

This is a sample shell app that generates data files of arbitrary sizes.

## Container

### Building the container

To build the app : 

```
docker build -f Dockerfile -t <IMG> .
```

# Container Usage 

The container creates files upon startup and sleeps infinitely. 

The container exposes different configuration options as environment variables :

| Variable               	| Default Value 	| Description                                                                                                                         	|
|------------------------	|---------------	|-------------------------------------------------------------------------------------------------------------------------------------	|
| `GENERATE_SAMPLE_DATA` 	| N             	| Whether to generate sample files or not?                                                                                            	|
| `NO_FILES`             	| 3             	| How many sample files to create? Each file  is created in its own directory under  `/opt/mounts/`e.g. `/opt/mounts/mnt1/SampleData` 	|
| `FILE_SIZE`            	| 1024M         	| Size of the sample files                                                                                                            	|

## Deploying on OpenShift 

The Ansible playbook `playbook.yml` helps create / delete the benchmark pod on OpenShift cluster.

Before deploying the pod, make sure you have built a container image.

`default.yml` contains default configuration used for the pod. 

To deploy the pod on cluster, login to your OpenShift cluster using `oc login`

Once logged in, deploy the pod :

```sh
ansible-playbook playbook.yml -e image=<IMG>
```

To delete the pod : 

```sh
ansible-playbook playbook.yml -e image=<IMG> -e destroy=true
```


