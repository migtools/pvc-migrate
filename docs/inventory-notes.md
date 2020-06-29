# Configuring SSH and Inventory

**Stage 3** of `pvc-migrate` runs `rsync` to synchronize data between the source and the destination cluster PVCs.

---

**On the destination cluster**, for each PVC to be migrated, `pvc-migrate` will: 
1. Create a *dummy sync Pod* that has `ssh` and `rsync` installed.
2. Mount the PVCs created in `Stage 2` onto these *dummy sync Pod* to make `rsync` possible from the source cluster.

**On the source cluster**, for each PVC to be migrated, `pvc-migrate` will:
1. Determine the source cluster OpenShift Node on which data is present.
2. SSH into the OpenShift Node and run `rsync` with the destination cluster *dummy sync Pod* as the `rsync` target.

Therefore, `pvc-migrate` needs to be able to connect with every node on the source side. 

---

## Stage 3: Network Connectivity requirements:

1. *Ansible Control Node* host needs access to _all_ the OpenShift Nodes on source cluster
   1. If OpenShift Nodes are not accessible from the internet, `pvc-migrate` can connect through a bastion host. 
   
   
1. *Ansible Control Node* host needs access to *dummy sync Pods* created on the destination cluster. 
   1. Users need to build their own container image for *dummy sync Pods*, the Dockerfile and the instructions to build new docker image can be found [here](../2_pvc_destination_gen/extras/container/Dockerfile)

## Stage 3: Required SSH Configuration:

Before running *Stage 3*, configure the SSH Daemon on the Ansible Control Node host to allow jump over bastion into OpenShift nodes.

### Bastion Host - `~/.ssh/config`

See following example configuration in `~/.ssh/config` :

```sh
Host *.${INTERNAL_DOMAIN}
    User ec2-user
    ProxyCommand ssh -W %h:%p ${BASTION_HOST}
    IdentityFile ${PRIVATE_KEY_FROM_BASTION_TO_NODES}

Host ${BASTION_HOST}
    User ec2-user
    IdentityFile ${PRIVATE_KEY_TO_BASTION}
    ControlMaster auto
    ControlPath ${HOME}/.ssh/ansible-%r:%h:%p
    ControlPersist 5m
```

### Ansible Control Node - `ansible.cfg`

See the following example configuration of `ansible.cfg`

```sh
[ssh_connection]
ssh_args = -F ${HOME}/.ssh/config -o ControlMaster=auto -o ControlPersist=5m
control_path = ${HOME}/.ssh/ansible-%%r@%%h:%%p
```
