#!/bin/bash

# Create files? 
[[ -z "${GENERATE_SAMPLE_DATA}" ]] && GenerateSampleData="N" || GenerateSampleData="${GENERATE_SAMPLE_DATA}"

# How many volume mounts at location /opt/mounts
[[ -z "${NO_FILES}" ]] && NumberOfMounts="3" || NumberOfMounts="${NO_MOUNTS}"

# File size created upon startup
[[ -z "${FILE_SIZE}" ]] && FileSize="1024M" || FileSize="${FILE_SIZE}"

if [[ "${GENERATE_SAMPLE_DATA}" == "Y" ]]
then
    echo "Generating sample data..."
    for i in $( seq 0 $NumberOfMounts )
    do
        /usr/bin/mkdir -p "/opt/mounts/mnt${i}"
    	/usr/bin/truncate -s ${FileSize} "/opt/mounts/mnt${i}/SampleData"
        echo "Generated sample data at /opt/mounts/mnt${i}"
    done
else 
    echo "Skipping sample data generation..."
    echo "Please set GENERATE_SAMPLE_DATA to Y to generate data"
fi

/usr/bin/sleep infinity


