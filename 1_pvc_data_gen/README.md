# Stage 1: pvc-data-gen

This playbook scans source cluster PVCs in a `namespaces_to_migrate` list provided by the user and generates info needed by stage 2 for destination cluster PVC creation and data sync.

## Usage:

1. Before running stage 1, ensure you have completed [prerequisite steps](https://github.com/konveyor/pvc-migrate#prerequisite-steps) and have installed required [automation prerequisites](https://github.com/konveyor/pvc-migrate#2-automation-prerequisites).

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

3. Run script while KUBECONFIG is set for connection to **source cluster**
```
export KUBECONFIG="/path/to/src_cluster_kubeconfig"
python3 pvc_data_gen.py 
```

4. Move on to [Stage 2](../2_pvc_destination_gen)

---

Sample generated output


**output/node-list.json**
```bash
cat output/node-list.json
[
    {
        "name": "ip-10-0-138-112.ec2.internal"
    }
]
```

**output/namespace-data.json**
```bash
cat output/namespace-data.json
[
    {
        "namespace": "rocket-chat",
        "annotations": {
            "openshift.io/backup-registry-hostname": "docker-registry.default.svc:5000",
            "openshift.io/backup-server-version": "1.11",
            "openshift.io/description": "",
            "openshift.io/display-name": "",
            "openshift.io/requester": "opentlc-mgr",
            "openshift.io/sa.scc.mcs": "s0:c9,c4",
            "openshift.io/sa.scc.supplemental-groups": "1000080000/10000",
            "openshift.io/sa.scc.uid-range": "1000080000/10000"
        }
    }
]
```

**output/pvc-data.json**
```bash
cat output/pvc-data.json  
[
    {
        "namespace": "rocket-chat",
        "pvcs": [
            {
                "pvc_name": "rocketchat-data-claim",
                "pvc_namespace": "rocket-chat",
                "capacity": "10Gi",
                "labels": {
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
                "pvc_uid": "66b89c3e-c25b-4d11-8af4-a167aeaf9013",
                "storage_class": "gp2",
                "bound": "Bound",
                "access_modes": [
                    "ReadWriteOnce"
                ],
                "node_name": "ip-10-0-138-112.ec2.internal",
                "volume_name": "pvc-66b89c3e-c25b-4d11-8af4-a167aeaf9013",
                "bound_pod_name": "rocketchat-db-1-2thf7",
                "bound_pod_uid": "fb246b11-f946-48f1-a6e2-3e2b92acbbb1",
                "bound_pod_mount_path": "/data/db",
                "bound_pod_mount_container_name": "rocketchat-db"
            }
        ]
    }
]
```
