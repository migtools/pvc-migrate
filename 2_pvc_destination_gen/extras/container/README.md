# Rsync + SSH Container for OpenShift

The Rsync and SSH container allows running rsync in an OpenShift pod exposed via SSH tunnel & LoadBalancer Service.

# Build container

Create a SSH key to be registered with the container 

```sh
ssh-keygen -f <SSH_KEY_FILE_NAME>
```

Note that the key will be _baked in_ the container.

To build the container :

```sh
export IMG=quay.io/<repository>/<container_name>:<tag>

docker build --build-arg sshkey=<SSH_KEY_FILE_NAME> -t $IMG -f Dockerfile .
```

Note that 
# Deploy container

To deploy pod with the SSH container image on OpenShift cluster :

```sh
cp pod.yaml.sample pod.yaml

# Replace image with the IMG you built in the previous step
oc apply -f pod.yaml

# Create service
oc apply -f svc.yaml
```

Note that the resources will be created in your current namespace

# Rsync to pod

To rsync files to the destination pod :

```sh
# get the URL to the Service
URL=`oc get svc ssh -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'`

rsync -aPv <DIR> root@${URL}:<DESTINATION_DIR> 
```
