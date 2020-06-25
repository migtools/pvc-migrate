# Synchronization Phase

This allows us to synchronize files between source and destination clusters.

## Pre-requisites

* Ansible Host machine needs access to _all_ the OpenShift nodes on source cluster
  * A bastion host to help us jump to OpenShift nodes (Only applicable if nodes do not have public addresses)
  * An [inventory](./inventory) file to map node names with their internal DNS addresses
* Ansible Host machine needs access to stage SSH pods created on the destination cluster
  * We create an SSH key on Ansible Host and register it in SSH pods on destination cluster

## SSH Configuration

Before running the sync phase, we configure SSH Daemon on Ansible Host to allow jump over bastion into OpenShift nodes.

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

Additionally, we configure Ansible to use the the above configuration along with some additional options in `ansible.cfg` 

```sh
[ssh_connection]
ssh_args = -F ${HOME}/.ssh/config -o ControlMaster=auto -o ControlPersist=5m
control_path = ${HOME}/.ssh/ansible-%%r@%%h:%%p
```

## Running synchronization phase

In progress...
  
