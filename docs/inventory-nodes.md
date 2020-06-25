# Configuring SSH and Inventory

`Stage 3` of `pvc-migrate` tooling is responsible for the synchronization of data between the source and the destination cluster.

On the destination cluster, for each PVC to be migrated, `pvc-migrate` creates a dummy pod that has `ssh` and `rsync` installed. It mounts the PVC we created in `Stage 2` onto these pods to be able to `rsync` from the source cluster. 

On the source side, for each PVC to be migrated, `pvc-migrate` finds out the physical node on which data is present. It then SSHs into the node and runs `rsync` keeping the destination cluster as the target. Therefore, `pvc-migrate` needs to be able to connect with every node on the source side. 

Here are absolute requirements for `pvc-migrate` to work :

* Ansible Host machine needs access to _all_ the OpenShift nodes on source cluster
 * If nodes are not accessible from the internet, `pvc-migrate` relies on a bastion host to connect with the nodes. 
* Ansible Host machine needs access to stage SSH pods created on the destination cluster. 
 * Users need to build their own Docker image to use as dummy pods, the Dockerfile and the instructions to build new docker image can be found [here](../2_pvc_destination_gen/extras/container/Dockerfile)

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

