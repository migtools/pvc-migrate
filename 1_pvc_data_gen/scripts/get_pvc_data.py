import json
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

with open('vars/pvc-data-gen.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

output = []

for namespace in data['namespaces_to_migrate']:
    v1_pods = dyn_client.resources.get(api_version='v1', kind='Pod')
    pod_list = v1_pods.get(namespace=namespace)

    v1_pvcs = dyn_client.resources.get(api_version='v1', kind='PersistentVolumeClaim')
    pvc_list = v1_pvcs.get(namespace=namespace)
    for pvc in pvc_list.items:
        pvc_pod = None
        boundPodName = ''
        boundPodUid = ''
        nodeName = ''
        for pod in pod_list.items:
            volumes = pod.spec.get('volumes', "")
            if volumes == "":
                continue
            for volume in volumes:
                if volume.get('persistentVolumeClaim', {}).get('claimName', '') == pvc.metadata.name:
                    pvc_pod = pod.__dict__
                    break
            if pvc_pod != None:
                break

        if pvc_pod != None:
            boundPodName = pod.metadata.name
            boundPodUid = pod.metadata.uid
            nodeName = pod.spec.nodeName
        pvc_out = {
                'pvc_name': pvc.metadata.name,
                'pvc_namespace': pvc.metadata.namespace,
                'capacity': pvc.spec.resources.requests.storage,
                'labels': pvc.metadata.labels.__dict__,
                'annotations': pvc.metadata.annotations.__dict__,
                'pvc_uid': pvc.metadata.uid,
                'storage_class': pvc.spec.storageClassName,
                'bound': pvc.status.phase,
                'access_modes': pvc.spec.accessModes,
                'node_name': nodeName,
                'volume_name': pvc.spec.volumeName,
                'bound_pod_name': boundPodName,
                'bound_pod_uid': boundPodUid
        }
        output.append(pvc_out)
    #ns_out = json.dumps(ns_out)
    

# Write the result back out to pvc-data.json
with open('output/pvc-data.json', 'w') as f:
    ns_data = json.dump(output, f, indent=4)


            

        
