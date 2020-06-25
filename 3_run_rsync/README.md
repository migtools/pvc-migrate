# Stage 3: run_rsync

This playbook takes the input from [Stage 1](../1_pvc_data_gen) and [Stage 2](../2_pvc_destination_gen) and creates a Pod mounting each PVC. It also creates 
a LoadBalancer service through which we can run ssh/scp/rsync externally

## Usage:

1. Create your own copy of vars file 
```
cp vars/run-rsync.yml.example vars/run-rsync.yml
```

2. Run playbook while kubeconfig is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook run-rsync.yml -e mig_run_sync_phase=true  -e mig_dest_ssh_key=~/.ssh/libra.pem
```

3. Refer to  [Step 7 - Run CAM in "no PV" mode](https://github.com/konveyor/pvc-migrate#7-run-cam-in-no-pvc-migration-mode) to complete the migration.
