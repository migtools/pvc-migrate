# Stage 3: run_rsync

This playbook takes the input from [Stage 1](../1_pvc_data_gen) and [Stage 2](../2_pvc_destination_gen) and creates a Pod mounting each PVC. It also creates 
a LoadBalancer service through which we can run ssh/scp/rsync externally

## Usage:

1. Ensure you have followed steps in [inventory-notes.md](../docs/inventory-notes.md) 
   1. Complete SSH and Ansible Configuration 

2. Create your own copy of vars file 
```
cp vars/run-rsync.yml.example vars/run-rsync.yml
```

3. Set vars in `vars/run-rsync.yml`

```
# Destination cluster 'transfer pod' resource limits
transfer_pod_cpu_limits: '1'
transfer_pod_cpu_requests: '100m'
transfer_pod_mem_limits: '1Gi'
transfer_pod_mem_requests: '1Gi'

# Destination cluster 'transfer pod' SSH auth info
mig_dest_ssh_public_key: ""  # path to public key to install as authorized user in transfer pod
mig_dest_ssh_private_key: "" # path to private key used for SSH auth into transfer pod as 'root' user

# Wait for transfer pod service ELB deletion to complete before proceeding to next PVC
wait_for_finalizer: false
```

4. Run Stage 3 playbook while KUBECONFIG is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook run-rsync.yml 
```

By default, `rsync` accepts connections on port `2222` through `stunnel`. If the port is pre-occupied on your cluster, you can override it by using extra var `stunnel_port` : `ansible-playbook run-rsync.yml ... -e stunnel_port=<PORT> ...`.

For all the default variables used, please check the [defaults.yml](./vars/defaults.yml) file.

5. Refer to  [Step 7 - Run CAM in "no PV" mode](https://github.com/konveyor/pvc-migrate#7-run-cam-in-no-pvc-migration-mode) to complete the migration.
