# Stage 2: pvc-destination-gen

This playbook takes the input from [Stage 1](../1_pvc_data_gen) and creates PVC OpenShift resources in destination cluster

## Usage:

1. Create your own copy of vars file 
```
cp vars/pvc-destination-gen.yml.example vars/pvc-destination-gen.yml
cp vars/storage-class-mappings.yml.example vars/storage-class-mappings.yml
```

2. Edit storage class mappings in `vars/storage-class-mappings.yml` as needed.

3. Run playbook while KUBECONFIG is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook pvc-destination-gen.yml
```
4. Verify that PVCs are created on destination

```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
oc get pvc -n sample-namespace
```

5. Move on to [Stage 3](../3_run_rsync)
