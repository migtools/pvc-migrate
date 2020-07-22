#!/bin/bash

# Defaults
# Max number of files to create per directory
MAX_FILES="128"
# Total data size for all files in megabytes
DATA_SIZE="1024"
# PWD if -d not used
DIR="$(pwd)"
# Randomize existing data
RANDOMIZE="false"

function usage () {
echo
echo "Valid options are : "
echo -e "\t-c : How much data to create in megabytes: i.e $0 -c 1024"
echo -e "\t-d : Target directory to create data, default is PWD"
echo -e "\t-m : Max number of files to create, default is 128"
echo -e "\t-r : Number of files of existing data to be randomized"
echo
exit 1
}

while getopts c:d:r:m:h opt
do
    case $opt in

        c)
            DATA_SIZE=${OPTARG}
            ;;
        d)
            DIR=${OPTARG}
            ;;
        m)
            MAX_FILES=${OPTARG}
            ;;
        r)
            RANDOMIZE="true"
            R_FILES=${OPTARG}
            ;;
        h)
            usage
            ;;
        *)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            ;;
    esac
done

# Check target dir
[ ! -d ${DIR} ] && echo "${DIR} directory does not exist, unable to continue, exiting.." && exit 1

if [ ${RANDOMIZE} == "true" ]; then
	for file in `seq 1 ${R_FILES}`; do
		[ ! -f ${DIR}/file${file} ] && echo "${DIR}/file${file} does not exist, unable to randomize, exiting.." && exit 1
		echo "Randomizing ${DIR}/file${file}.."
		dd conv=notrunc if=/dev/urandom of="${DIR}/file${file}" bs=1M count=1
	done
	echo
	echo "Randomized ${R_FILES} files at ${DIR}"
	echo
else
	FILE_SIZE=$((DATA_SIZE/MAX_FILES))
	for file in `seq 1 ${MAX_FILES}`; do
		echo "Creating ${DIR}/file${file}.."
		dd if=/dev/urandom of="${DIR}/file${file}" bs=1M count=${FILE_SIZE}
	done
	TOTAL_SIZE="$(du -sh ${DIR} | awk '{ print $1 }')"
	echo
	echo "Created ${MAX_FILES} files at ${DIR}, total size is ${TOTAL_SIZE}"
	echo
fi
