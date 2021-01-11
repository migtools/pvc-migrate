# Known Rsync Issues

This document lists some of the known issues with Rsync observed in our testing environments and proposes solutions to solve them. 

## Issue 1: Rsync fails with `Connection timed out` error

This error can be caused when any network entity between the source and the target cluster drops the connection. The Rsync client process exits with non-zero return code printing `Connection timed out` error in the log. The _Stunnel_ logs may show `Connection reset peer` message.

### Possible Cause 1

pvc-migrate uses OpenShift Route in _passthrough_ mode to expose Rsync Daemon process running in the target cluster. The traffic is secured using an end-to-end tunnel created by _Stunnel_. 

OpenShift Routes are behind an AWS ELB used by the `ingress-controller`. The AWS ELB resets the incoming connection from Rsync Client when the client overwhelms the Rsync Daemon on the target. This is observed when the total files to be transferred are in the order of _a few hundred gigabytes_ or more.

To solve this issue, following solutions can be used:

- [Using bandwidth limiting options in Rsync](#using-bandwidth-limiting-options-in-rsync)
- [Increasing resources in the target Rsync Pod](#increasing-resources-in-the-target-rsync-pod)
- [Using NodePort Service instead of OpenShift Route](#using-nodeport-service-instead-of-openshift-route)

### Possible Cause 2

The OpenShift Route itself may drop the connection when it's default timeout of 30 seconds exceeds. This can be simply solved by increasing the timeout on the OpenShift Route created in the target cluster:

- [Increasing timeout on target OpenShift Route](#increasing-timeout-on-target-openshift-route)

## General solutions and workarounds

### Using bandwidth limiting options in Rsync

`--bwlimit` option allows limiting average bandwidth consumed by Rsync. This option is helpful in making sure the source always sends data at a controlled rate. By using this option alone, it is possible to completely avoid the issue. However, there is no perfect value which will work for all environments. The value needs to be determined by choosing a high bandwidth value first, then gradually decreasing it until the issue disappears. In `pvc-migrate`, this can be simply done by overriding `rsync_opts` variable in Stage 3:

`./3_run_rsync/vars/defaults.yml`
```yml
# below will limit the bandwidth to 250000 KB/sec 
rsync_opts: "-aPvvHh --delete --bwlimit=250000"
```

### Increasing resources in the target Rsync Pod

To avoid source overwhelming the target Pod, the target Pod can simply use more resources. In `pvc-migrate`, this can be done by overriding default resource constraints used by Rsync Pod: 

`./3_run_rsync/vars/run-rsync.yml`
```yml
transfer_pod_cpu_limits: '1'
transfer_pod_cpu_requests: '100m'
transfer_pod_mem_limits: '1Gi'
transfer_pod_mem_requests: '1Gi'
```

### Increasing timeout on target OpenShift Route

The default timeout on OpenShift Route exposing the Rsync Daemon Pod can be increased by using the following variable in `pvc-migrate`:

`./3_run_rsync/vars/defaults.yml`
```yml
route_timeout_seconds: 300
```

### Using NodePort Service instead of OpenShift Route

_Note: This solution is only applicable when the source and the target clusters are in the same network_.

When the source and the target clusters are both in the same network, it is possible to use OpenShift Service of type _NodePort_ instead of using an OpenShift Route. This will eliminate the use of AWS ELB altogether as _NodePort_ services expose on a physical port on underlying node instead of exposing through OpenShift Router. The source Rsync client Pod can then simply transfer the data using the internal IP address and the exposed NodePort of the target node instead of relying on a Route. 

`pvc-migrate` supports this setup. It is available in [node-port](https://github.com/konveyor/pvc-migrate/tree/node-port) branch of the project. By default, in AWS environments, OpenShift blocks the connections coming on the node port with the help of AWS Security Groups. Before trying this approach, the security groups of target nodes need to be manually updated to allow traffic from the CIDR range of source nodes. _Stage 1_ and _Stage 2_ work exactly the same way. The only change in this branch is in _Stage 3_. Apart from updating security groups, there is no extra configuration needed for this to work. You can simply follow the instructions in [readme here](https://github.com/konveyor/pvc-migrate/blob/node-port/3_run_rsync/README.md) to use the _NodePort_ solution.
