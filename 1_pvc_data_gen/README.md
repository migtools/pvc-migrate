# pvc-data-gen

This playbook scans source cluster PVCs in a `namespaces_to_migrate` list provided by the user and generates info needed by stage 2 for destination cluster PVC creation and data sync.

## Usage:

1. Create your own copy of vars file 
```
cp vars/pvc-data-gen.yml.example vars/pvc-data-gen.yml
```

2. Edit `vars/pvc-data-gen.yml` adding a list of namespaces
```
namespaces_to_migrate:
- rocket-chat
- mssql-persistent
```

3. Run playbook while kubeconfig is set for connection to **source cluster**
```
export KUBECONFIG="/path/to/src_cluster_kubeconfig"
ansible-playbook pvc-data-gen.yml
```

4. Examine generated output
```
cat output/pvc-data.json  

[
{
  "pvc_name" : "rocketchat-data-claim",
  "pvc_namespace": "rocket-chat",
  "capacity": "10Gi",
  "labels" : {
    "velero.io/backup-name": "bd778570-b286-11ea-8b3d-298baab088b3-f9mrj",
    "velero.io/restore-name": "bd778570-b286-11ea-8b3d-298baab088b3-rhz9q"
},
  "annotations": {
    "openshift.io/backup-registry-hostname": "docker-registry.default.svc:5000",
    "openshift.io/backup-server-version": "1.11",
    "openshift.io/restore-registry-hostname": "image-registry.openshift-image-registry.svc:5000",
    "openshift.io/restore-server-version": "1.17",
    "pv.kubernetes.io/bind-completed": "yes",
    "pv.kubernetes.io/bound-by-controller": "yes",
    "volume.beta.kubernetes.io/storage-provisioner": "kubernetes.io/aws-ebs",
    "volume.kubernetes.io/selected-node": "ip-10-0-138-112.ec2.internal"
},
  "uid": "66b89c3e-c25b-4d11-8af4-a167aeaf9013",
  "storage_class": "gp2",
  "bound": "Bound",
  "access_modes": ["ReadWriteOnce"],
  "node_name":  "ip-10-0-138-112.ec2.internal"
}
,
{
  "pvc_name" : "mssql-pvc",
  "pvc_namespace": "mssql-persistent",
  "capacity": "10Gi",
  "labels" : {
    "app": "mssql"
},
  "annotations": {
    "pv.kubernetes.io/bind-completed": "yes",
    "pv.kubernetes.io/bound-by-controller": "yes",
    "volume.beta.kubernetes.io/storage-provisioner": "kubernetes.io/aws-ebs",
    "volume.kubernetes.io/selected-node": "ip-10-0-153-152.ec2.internal"
},
  "uid": "f9187fd8-feb2-4542-a18f-6f41f293a571",
  "storage_class": "gp2",
  "bound": "Bound",
  "access_modes": ["ReadWriteOnce"],
  "node_name":  "ip-10-0-153-152.ec2.internal"
}

]
```
