# Storage Class Selection

`Stage-2` of `pvc-migrate` is responsible for migrating PVCs to destination. While migrating PVCs it cannot automatically choose the right Storage Class for migrated PVCs on the destination side. For instance, an RWO mode PV using `glusterfs-storage` on an OpenShift 3.x cluster typically corresponds to `cephrbd` SC on destination. On the other hand, an RWX mode PV on `glusterfs-storage` corresponds to `cephfs` SC on the destination side. `pvc-migrate` ___cannot___ automatically convert Storage Classes. However, it provides users with a way to input a static mapping of storage class names between the source and the destination cluster.

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

If a valid mapping is not found, `pvc-migrate` will simply retain the original Storage Class in the migrated PVC, which may result in a failure. 

If a PVC doesn't have any Storage Class assigned, migrated PVC will use the `default` Storage Class on the destination. 

## Usage

Users are required to create their mapping before running `Stage-2` of `pvc-migrate`. 

The mapping can be given as a variable file located at [Stage-2 SC Mapping](../2_pvc_destination_gen/vars/pvc-destination-gen.yml)

We have also provided a [Sample Mapping](../2_pvc_destination_gen/vars/pvc-destination-gen.yml.sample) to help you create your own mapping.

