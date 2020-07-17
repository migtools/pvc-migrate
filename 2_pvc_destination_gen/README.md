# Stage 2: pvc-destination-gen

This playbook takes the input from [Stage 1](../1_pvc_data_gen) and creates PVC OpenShift resources in destination cluster.

## Sub-Stages

`Stage 2` is divided into two sub-stages `Stage 2 (a)` and `Stage 2 (b)`. 

### Stage 2 (a)

`Stage 2 (a)` scans the volumes on the source cluster to ensure :

* The volumes on the source node are not full or close-to-full.
* The requested size in PVC matches the actual volume size on the source.

If any of the above conditions are met, `pvc-migrate` takes corrective actions to _adjust_ the PVC size on the destination cluster. 

* When the volume is found to be full :
  * The destination volume is grown by 5% of its original size on the source node. The value `5%` can be configured using variable `full_volume_grow_percentage`. The default value is set to `5.0`.
* When the size of the volume doesn't match its requested size in the PVC :
  * The size of the actual volume is used to create PVC on the destination.

Finally, `Stage 2 (a)` generates an intermediary report that contains information about the decisions `pvc-migrate` took regarding volume sizes along with the reasons behind them. The report can be found in the default output directory. The users are expected to read the report and confirm whether the corrective actions are accepteable. 

### Stage 2 (b)

This is the final sub-stage where `pvc-migrate` will read the output from `Stage 1` to create PVCs on the destination cluster. For every volume, it will also apply the corrective actions reported in `Stage 2 (a)` report, if applicable. 

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
  glusterfs-storage-block_RWO: ocs_storagecluster-ceph-rbd
```

3. Run `Stage 2 (a)` while KUBECONFIG is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook pvc-destination-gen.yml --tags stage_a
```
Check the report generated in the output directory in file `pvc-data-adjusted.json`. Make sure that the new PV sizes are accepteable. 

A sample output from `Stage 2 (a)` :

```json
[
    {
        "actual_pv_size": "1019M",
        "adjusted_pvc_capacity": "2Gi",
        "original_pvc_capacity": "1Gi",
        "original_volume_usage": "100%",
        "pvc_name": "pvc-2",
        "pvc_namespace": "pvc-migrate-bmark-0",
        "reason": "PV was identified to be almost full. pvc-migrate grew the original size by 5%."
    }
]
```

In the above example, the volume on the source was full. Therefore, `pvc-migrate` grew the volume and rounded the value to the nearest possible value maintaining the original size unit `Gi`. 

4. Run `Stage 2 (b)` while KUBECONFIG is set for connection to **destination cluster**
```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
ansible-playbook pvc-destination-gen.yml --tags stage_b
```

5. Verify that PVCs are created on destination

```
export KUBECONFIG="/path/to/destination_cluster_kubeconfig"
oc get pvc -n sample-namespace
```

6. Move on to [Stage 3](../3_run_rsync)
