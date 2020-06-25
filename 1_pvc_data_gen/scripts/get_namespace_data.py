import json
import yaml
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from kubernetes import client, config
from openshift.dynamic import DynamicClient

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)

with open('vars/pvc-data-gen.yml') as f:
    data = yaml.load(f)

output = []

for namespace in data['namespaces_to_migrate']:
    print(namespace)
    v1_namespaces = dyn_client.resources.get(api_version='v1', kind='Namespace')
    ns = v1_namespaces.get(name=namespace)
    print(ns.metadata.annotations)
    ns_out = {'namespace': namespace, 'annotations': ns.metadata.annotations.__dict__}
    output.append(ns_out)
    #ns_out = json.dumps(ns_out)
    

# Write the result back out to pvc-data.json
with open('output/namespace-data.json', 'w') as f:
    ns_data = json.dump(output, f, indent=4)


            

        
