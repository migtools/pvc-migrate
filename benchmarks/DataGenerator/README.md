# Data Generator

This is a sample shell app that generates data files of arbitrary sizes.

It creates one file of specified size per PV.

## Container

### Building the container

To build the app : 

```
docker build -f Dockerfile -t <IMG> .
```

### Container Usage 

The container creates files upon startup and sleeps infinitely. 

The container exposes different configuration options as environment variables :

| Variable               	| Default Value 	| Description                                                                                                                         	|
|------------------------	|---------------	|-------------------------------------------------------------------------------------------------------------------------------------	|
| `GENERATE_SAMPLE_DATA` 	| N             	| Whether to generate sample files or not?                                                                                            	|
| `NO_FILES`             	| 3             	| How many sample files to create? Each file  is created in its own directory under  `/opt/mounts/`e.g. `/opt/mounts/mnt1/SampleData` 	|
| `FILE_SIZE`            	| 1024          	| Size of the sample files in M                                                                                                        	|

## Deploying on OpenShift 

The Ansible playbook `playbook.yml` helps create / delete the benchmark pod on OpenShift cluster using Konveyor's image.

`default.yml` contains default configuration used for the pod. 

To deploy the pod on cluster, login to your OpenShift cluster using `oc login`

Once logged in, deploy the pod :

```sh
ansible-playbook playbook.yml
```

To delete the pod : 

```sh
ansible-playbook playbook.yml -e destroy=true
```

Note that the environment variables exposed by the container are passed to the playbook as variables.

## Alternative sample data generator

An additional generate_sample.sh script is supplied within the image if more advanced data samples are needed, it can create new samples or randomize existing data. See options and sample usage below: 
```
$ ./generate_sample.sh -h

Valid options are : 
	-c : How much data to create in megabytes
	-d : Target directory to create data, default is PWD
	-m : Max number of files to create, default is 128
	-r : Number of files of existing data to be randomized

```

Create some data : 

```
$ ./generate_sample.sh -c 4096 -d /opt/mounts/mnt1 -m 1024
```

Randomize existing data : 

```
$ ./generate_sample.sh -d /opt/mounts/mnt1 -r 128
```
