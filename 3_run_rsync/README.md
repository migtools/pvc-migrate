# run_rsync

This playbook takes the input from stage 1 and creates a pod for each pvc and mounts it on the pvc. It also creates 
a LoadBalancer service through which we can run ssh/scp/rsync externally

## Usage:

1. Create your own copy of vars file 
```
cp vars/run-sync.yml.example vars/run-sync.yml
```
2. copy the output directory from stage 1 to 2_pvc_destination_gen folder

```
mkdir 3_run_rsync/output
cp -r 1_pvc_data_gen/output 3_run_rsync/output
```


3. Run playbook while kubeconfig is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook rsync.yml
```