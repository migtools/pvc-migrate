# pvc-migrate
Standalone PVC migration

## Overview
pvc-migrate automates migration of PersistentVolumeClaims and PersistentVolumes from OCP 3.x to OCP 4.x.

## Usage
1. **Clone this git repo**
```
git clone https://github.com/konveyor/pvc-migrate && cd pvc-migrate
```

2. **Install prerequisites**

```
pip install ansible    # ansible 2.9 
pip install kubernetes # kubernetes module for ansible
pip install openshift  # openshift module for ansible
sudo yum install jq    # jq for json processing
```

3. **Copy source and target cluster KUBECONFIG files authenticated with  *cluster-admin* privileges to `auth` directory**
   1. Create `auth` directory inside of repository root:  `mkdir auth`
   1. Copy source cluster kubeconfig to `auth/KUBECONFIG_SRC`
   1. Copy target cluster kubeconfig to `auth/KUBECONFIG_TARGET`
   
4. **Set list of namespaces to migrate PV/PVC data for**
   1. Copy sample config file as starting point: `cp 1_pvc_data_gen/vars/pvc-data-gen.yml.example pvc-data-gen.yml`
   1. Edit `1_pvc_data_gen/vars/pvc-data-gen.yml`, adding list of namespaces for which PV/PVC data should be migrated
   
```
namespaces_to_migrate:
 - rocket-chat
 - nginx-pv
```
 
5. **Run playbook automation**
   1. Run `./migrate_pv_data.sh` to kick off a series of Ansible Playbooks that will migrate PV/PVC data in selected namespaces
   2. Upon successful completion, selected namespaces will be created on the *target cluster* and PV/PVC data from the *source cluster* will have been copied with *rsync* into dynamically provisioned PV/PVC pairs 
