# pvc-migrate


## Overview

`pvc-migrate` automates migration of PersistentVolumeClaims (PVCs) and PersistentVolumes (PVs) from OCP 3.x to OCP 4.x.

## Usage
### 1. Clone this git repo

```
git clone https://github.com/konveyor/pvc-migrate && cd pvc-migrate
```

### 2. Install prerequisites

```
pip install ansible==2.9.7     # ansible 2.9
pip install kubernetes==11.0.0 # kubernetes module for ansible
pip install openshift=0.11.2   # openshift module for ansible
pip install PyYAML==5.1.1      # pyyaml module for python
pip install jmespath==0.10.0   # for json querying from ansible

sudo dnf install jq            # jq-1.6 for json processing
sudo install bind-utils
sudo install dnsutils
```

### 3. Set cluster authentication details
**Copy source and destination cluster KUBECONFIG files authenticated with  *cluster-admin* privileges to `auth` directory**
   1. Create `auth` directory inside of repository root:  `mkdir auth`
   1. Copy source cluster kubeconfig to `auth/KUBECONFIG_SRC`
   1. Copy destination cluster kubeconfig to `auth/KUBECONFIG_TARGET`
   
### 4. Set list of namespaces to migrate PVC data for
   1. Copy sample config file as starting point: `cp 1_pvc_data_gen/vars/pvc-data-gen.yml.example 1_pvc_data_gen/vars/pvc-data-gen.yml`
   1. Edit `1_pvc_data_gen/vars/pvc-data-gen.yml`, adding list of namespaces for which PV/PVC data should be migrated
   
```
namespaces_to_migrate:
 - rocket-chat
 - nginx-pv
```
 
### 5. Familiarize with PVC migration automation

The `pvc-migrate` tooling is designed to work in 3 stages :    

#### Stage 1 - Detect source cluster info (PVCs, Pods, Nodes) ([Stage 1 README](1_pvc_data_gen/README.md))
```
1_pvc_data_gen
````
This preliminary stage collects information about PVCs, PVs and Pods from the Source cluster. It creates a JSON report of collected data which will be consumed by subsequent stages. 

**Note**: changes to the source cluster after completion of Stage 1 will not be considered by next stages. You can re-run stage 1 to refresh data as needed before running Stages 2 and 3.

#### Stage 2 - Migrate PVC definitions to destination cluster ([Stage 2 README](2_pvc_destination_gen/README.md))
```
2_pvc_destination_gen
````
This stage translates and migrates PVC resource definitions from the source to the destination cluster. 

**Note**: after completion of this stage, you will have PVCs created on the destination cluster which _may_ or _may not_ be `Bound`. This is expected as some provisioners do not create PVs until PVCs are bound to pods. This stage __requires__ users to provide Storage Class selections for the destination cluster. Please see notes on [Storage Class Selection](./docs/sc-selection.md)

#### Stage 3 - RSync PVC data to destination cluster ([Stage 3 README](3_run_rsync/README.md))
```
3_run_rsync
```
This final stage launches pods to attach with the PVCs created in the previous stage. 
- Each PVC is attached to its own dummy pod. The pods have `rsync` and `ssh` installed. 
- The tooling then uses `rsync` from source side to sync files to the PVs mounted on Pods in the destination side. 

*Note*: This stage __requires__ users to provide node info on the source cluster. Please see notes on [Configuring SSH and Inventory for Stage 3](./docs/inventory-notes.md)


### 6. Running the PVC migration
1. Run steps in: [1_pvc_data_gen/README.md](1_pvc_data_gen/README.md)
1. Run steps in: [2_pvc_destination_gen/README.md](2_pvc_destination_gen/README.md)
1. Run steps in: [3_run_rsync/README.md](3_run_rsync/README.md)
   
   
### 7. Run CAM in "no PVC migration" mode
   1. Your PV/PVC data has been migrated. You can use CAM to migrate the remaining OpenShift resources, which will connect to the PV/PVC data created by this tool.
   2. To run CAM in "no PVC migration" mode, modify the `MigrationController` resource on the *destination cluster* by swapping out the mig-controller image, then execute a migration as usual. The PVC migration steps will be skipped, but all other resources will be migrated, and workloads will connect back to the newly provisioned PVCs..
   
```
oc edit MigrationController -n openshift-migration
```
```
apiVersion: migration.openshift.io/v1alpha1
kind: MigrationController
metadata:
  name: migration-controller
  namespace: openshift-migration
spec:
  [...]
  mig_controller_image_fqin: quay.io/konveyor/mig-controller:release-1.2.2-hotfix-nopvs
  [...]
 ```
 
  3. Create a MigPlan and MigMigration covering the same namespaces migrated with `pvc-migrate`.
 
 ## Troubleshooting
If any steps fail, you can edit the shell script `migrate_pvc_data.sh`, toggling steps on/off as needed to re-run desired steps. If some PVCs migrate successfully and some fail, you can remove the PVCs that already migrated successfully from `output/pvc-data.json`
   
