# Storage Class Selection

`Stage-2` of `pvc-migrate` is responsible for migrating PVCs to destination. 

While migrating PVCs, `pvc-migrate` cannot automatically choose the correct StorageClass (SC) for migrated PVCs on the destination side. For instance, an RWO mode PV using `glusterfs-storage` on an OpenShift 3.x cluster typically corresponds to `cephrbd` SC on destination. On the other hand, an RWX mode PV on `glusterfs-storage` corresponds to `cephfs` SC on the destination side. 

`pvc-migrate` ___cannot___ automatically determine the desired conversion between Storage Classes. You must provide a static mapping of StorageClass names between the source and the destination cluster.

See an example mapping below :

```yml
mig_storage_class_mappings:
  glusterfs-storage_RWO: ocs-storagecluster-ceph-rbd
  glusterfs-storage_RWX: ocs-storagecluster-cephfs
  glusterfs-storage-block_RWO: ocs_storagecluster-ceph-rbd
``` 

Each key-value pair in the above map follows the following format :

```yml
mig_storage_class_mappings:
  <SC-NAME-ON-SOURCE>_<MODE>: <SC-NAME-ON-DESTINATION> 
```

If a valid mapping is not found, `pvc-migrate` will simply retain the original StorageClass in the migrated PVC, which may result in a failure. 

If a PVC doesn't have any StorageClass assigned, migrated PVC will use the `default` StorageClass on the destination. 

## Usage

- Users are required to create their mapping before running [Stage 2](../2_pvc_destination_gen) of `pvc-migrate`. 
- The mapping can be given as a StorageClass mapping variable file [pvc-destination-gen.yml](../2_pvc_destination_gen/vars/pvc-destination-gen.yml)
- We have also provided a sample mapping [pvc-destination-gen.yml.sample](../2_pvc_destination_gen/vars/pvc-destination-gen.yml.example) showing the format of the mapping file

