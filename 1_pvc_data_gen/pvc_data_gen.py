import json
import yaml
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from kubernetes import client, config
from openshift.dynamic import DynamicClient

try:
    k8s_client = config.new_client_from_config()
    dyn_client = DynamicClient(k8s_client)
except: 
    print("\n[!] Failed while setting up OpenShift client. Ensure KUBECONFIG is set. ")
    exit(1)

script_dir = os.path.dirname(os.path.realpath(__file__))

# Using this as a workaround to handle empty results
class EmptyK8sResult:
    __dict__ = {}
emptyDict = EmptyK8sResult()

if not os.path.exists(script_dir+'/output'):
    os.makedirs(script_dir+'/output')


with open(script_dir+'/vars/pvc-data-gen.yml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

node_list = []
output = []

print("Running stage 1 data processing on namespaces: {}".format(data['namespaces_to_migrate']))

# Generate data for namespace-data.json
for namespace in data['namespaces_to_migrate']:
    print("Processing namespace: [{}]".format(namespace))
    v1_namespaces = dyn_client.resources.get(api_version='v1', kind='Namespace')
    try:
        ns = v1_namespaces.get(name=namespace)
        ns_out = {'namespace': namespace, 'annotations': ns.metadata.get("annotations", emptyDict).__dict__}
        output.append(ns_out)
    except:
        print("\n[!] v1/namespace not found: " + namespace)
    

with open(script_dir+'/output/namespace-data.json', 'w') as f:
    ns_data = json.dump(output, f, indent=4)

output = []

# Generate data for pvc-data.json and node-list.json
for namespace in data['namespaces_to_migrate']:
    print("Processing PVCs for namespace: [{}]".format(namespace))

    v1_pods = dyn_client.resources.get(api_version='v1', kind='Pod')
    pod_list = v1_pods.get(namespace=namespace)

    v1_pvcs = dyn_client.resources.get(api_version='v1', kind='PersistentVolumeClaim')
    pvc_list = v1_pvcs.get(namespace=namespace)
    for pvc in pvc_list.items:
        
        # Map pod binding and uid onto PVC data
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
            boundPodUid = pod.metadata.get("uid", "")
            nodeName = pod.spec.get("nodeName", "")
        if nodeName != "":
            node_list.append({'name': nodeName})

        # Build pvc-data.json data structure
        pvc_out = {
                'pvc_name': pvc.metadata.name,
                'pvc_namespace': pvc.metadata.namespace,
                'capacity': pvc.spec.get("resources",{}).get("requests",{}).get("storage",""),
                'labels': pvc.metadata.get("labels",emptyDict).__dict__,
                'annotations': pvc.metadata.get("annotations",emptyDict).__dict__,
                'pvc_uid': pvc.metadata.get("uid",""),
                'storage_class': pvc.spec.get("storageClassName",""),
                'bound': pvc.status.get("phase",""),
                'access_modes': pvc.spec.get("accessModes", ""),
                'node_name': nodeName,
                'volume_name': pvc.spec.get("volumeName",""),
                'bound_pod_name': boundPodName,
                'bound_pod_uid': boundPodUid
        }
        output.append(pvc_out)
    

# Write out results to pvc-data.json, node-list.json
with open(script_dir+'/output/pvc-data.json', 'w') as f:
    ns_data = json.dump(output, f, indent=4)

with open(script_dir+'/output/node-list.json', 'w') as f:
    ns_data = json.dump(node_list, f, indent=4)
