# Rsync + SSH Container for OpenShift

The Rsync and SSH container allows running rsync in an OpenShift pod exposed via SSH tunnel & LoadBalancer Service.

# Build container

To build the container :

```sh
export IMG=quay.io/<repository>/<container_name>:<tag>

docker build --build-arg sshpass=<SSH_PASS> -t $IMG -f Dockerfile .
```

# Deploy container

To deploy pod with the SSH container image on OpenShift cluster :

```sh
cp pod.yaml.sample pod.yaml

# Replace image with the IMG you built in the previous step
oc apply -f pod.yaml

# Create service
oc apply -f svc.yaml
```
