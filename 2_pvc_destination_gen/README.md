# Stage 2: pvc-destination-gen

This playbook takes the input from [Stage 1](../1_pvc_data_gen) and creates PVC OpenShift resources in destination cluster

## Usage:

1. Create your own copy of vars file 
```
cp vars/storage-class-mappings.yml.example vars/storage-class-mappings.yml
```

2. Set storage class mappings in `vars/storage-class-mappings.yml`, following directions in [sc-selection.md](../docs/sc-selection.md)

```
# Sample mappings for glusterfs -> cephfs migration
mig_storage_class_mappings:
  glusterfs-storage_RWO: ocs-storagecluster-ceph-rbd
  glusterfs-storage_RWX: ocs-storagecluster-cephfs
  glusterfs-storage-block_RWO: ocs-storagecluster-ceph-rbd
```

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
