# Storage Class Selection

**Stage 2** of `pvc-migrate` is responsible for migrating PVCs to destination. 

While migrating PVCs, `pvc-migrate` cannot automatically choose the correct StorageClass (SC) for migrated PVCs on the destination side. As examples of such mappings:

- **RWO mode PV** on OCP 3.x with SC `glusterfs-storage` typically maps to `cephrbd` SC on OCP 4.x destination.
- **RWX mode PV** on OCP 3.x with SC `glusterfs-storage` typically maps to `cephfs` SC on OCP 4.x destination. 

Since `pvc-migrate` ___cannot___ automatically determine the desired conversion between Storage Classes. You must provide a static mapping of StorageClass names between the source and the destination cluster.

### Example mapping from `storage-class-mappings.yml`:

```yml
mig_storage_class_mappings:
  glusterfs-storage_RWO: ocs-storagecluster-ceph-rbd
  glusterfs-storage_RWX: ocs-storagecluster-cephfs
  glusterfs-storage-block_RWO: ocs_storagecluster-ceph-rbd
``` 

The sample above follows this general format:
```yml
mig_storage_class_mappings:
  <SC-NAME-ON-SOURCE>_<MODE>: <SC-NAME-ON-DESTINATION> 
```

### Mapping Behavior

- If an applicable mapping is not found, `pvc-migrate` will retain the original StorageClass in the migrated PVC, which may result in a failure. 
- If a PVC doesn't have any StorageClass assigned, the migrated PVC will use the `default` StorageClass on the destination. 

## Required Steps for Stage 2

- Before running [Stage 2](../2_pvc_destination_gen), the StorageClass mapping must be provided in [storage-class-mappings.yml](../2_pvc_destination_gen/vars/storage-class-mappings.yml)

