# Stage 3: Configuring SSH and Inventory

**Stage 3** of `pvc-migrate` runs `rsync` to synchronize data between the source and the destination cluster PVCs.

---

**On the destination cluster**, for each PVC to be migrated, `pvc-migrate` will: 
1. Create a *transfer Pod* that has `ssh` and `rsync` installed.
2. Mount the PVCs created in `Stage 2` onto these '*transfer Pods*' to make `rsync` possible from the source cluster.

**On the source cluster**, for each PVC to be migrated, `pvc-migrate` will:
1. Determine the source cluster OpenShift Node on which data is present.
2. SSH into the OpenShift Node and run `rsync` with the destination cluster *transfer Pod* as the `rsync` target.

Therefore, `pvc-migrate` needs to be able to connect with every node on the source side. 

---

## Network Connectivity requirements

1. *Ansible Control Node* host needs *SSH access* to _all_ the OpenShift Nodes on source cluster
   1. If OpenShift Nodes are not accessible from the internet, `pvc-migrate` can connect through a bastion host. 
   
1. *Ansible Control Node* host needs *SSH access* to '*transfer Pods*' created on the destination cluster. 

## Required SSH and Ansible Configuration 

- Set SSH config (~/.ssh/config) on the host where `ansible-playbook` will be invoked
- Set Ansible config (ansible.cfg) on the host where `ansible-playbook` will be invoked

### **Mode 1**: Running 'ansible-playbook' from Bastion Host

Set these configuration values on the Bastion host.

##### `~/.ssh/config`

```sh
Host *.${INTERNAL_DOMAIN}
    User ec2-user
    ProxyCommand ssh -W %h:%p ${BASTION_HOST}
    IdentityFile ${PRIVATE_KEY_FROM_BASTION_TO_NODES}
```

##### `ansible.cfg`

```sh
[ssh_connection]
ssh_args = -F ${HOME}/.ssh/config -o ControlMaster=auto -o ControlPersist=5m
control_path = ${HOME}/.ssh/ansible-%%r@%%h:%%p
```

### **Mode 2**: Running 'ansible-playbook' from External Host

Set these configuration values on the External host.

##### `~/.ssh/config`

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

##### `ansible.cfg`

```sh
[ssh_connection]
ssh_args = -F ${HOME}/.ssh/config -o ControlMaster=auto -o ControlPersist=5m
control_path = ${HOME}/.ssh/ansible-%%r@%%h:%%p
```

## Next steps

After completing the above configuration, return to [Stage 3 README.md](../3_run_rsync) for next steps.



