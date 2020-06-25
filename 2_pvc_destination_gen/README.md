# pvc-destination-gen

This playbook takes the input from stage 1 and create the pvc's in destination cluster

## Usage:

1. Create your own copy of vars file 
```
cp vars/pvc-destination-gen.yml.example vars/pvc-destination-gen.yml
cp vars/storage-class-mappings.yml.example vars/storage-class-mappings.yml
```
2. copy the output directory from stage 1 to 2_pvc_destination_gen folder

```
mkdir 2_pvc_destination_gen/output
cp -r 1_pvc_data_gen/output 2_pvc_destination_gen/output
```


3. Run playbook while kubeconfig is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook pvc-destination-gen.yml
```
4. verify that pvc's are created on destination

```
# export KUBECONFIG=/path/to/destination/kubeconfig
oc get pvc -A
```