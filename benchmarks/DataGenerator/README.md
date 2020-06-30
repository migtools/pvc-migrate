# Data Generator

This is a sample shell app that generates data files of arbitrary sizes.

The data is generated in `/opt/mounts`. 

# Build

To build the app : 

```
docker build -f Dockerfile -t <IMG> .
```

# Usage

The container creates files upon startup and sleeps infinitely. 

The container exposes different configuration options as environment variables :

| Variable               	| Default Value 	| Description                                                                                                                         	|
|------------------------	|---------------	|-------------------------------------------------------------------------------------------------------------------------------------	|
| `GENERATE_SAMPLE_DATA` 	| N             	| Whether to generate sample files or not?                                                                                            	|
| `NO_FILES`             	| 3             	| How many sample files to create? Each file  is created in its own directory under  `/opt/mounts/`e.g. `/opt/mounts/mnt1/SampleData` 	|
| `FILE_SIZE`            	| 1024M         	| Size of the sample files                                                                                                            	|


