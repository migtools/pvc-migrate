import json

with open('output/pods-and-pvcs.json') as f:
    data = json.load(f)


# keep track of Pod associations to PVCs
pvc_pod_mapping = []

# for each PVC, need to find the pod (if any) that mounts the data
for pvc in data.get("pvcs", {}):
    pvc_name = pvc.get("metadata", {}).get("name", "")
    pvc_ns = pvc.get("metadata", {}).get("namespace", "")

    # look through all pods for the one that mounts this PVC
    for pod in data.get("pods", {}):
        pod_name = pod.get("metadata", {}).get("name", "")
        pod_ns = pod.get("metadata", {}).get("namespace", "")
        pod_uid = pod.get("metadata", {}).get("uid", "")

        volumes = pod.get("spec", {}).get("volumes", "")
        # skip if no vols
        if volumes == "":
            continue
        for volume in volumes:
            claimed_pvc = volume.get("persistentVolumeClaim", {}).get("claimName", "")
            # skip if no pvcs
            if claimed_pvc == "":
                continue
            if claimed_pvc == pvc_name:
                pvc_pod_mapping.append(
                    {
                        "pod_uid": pod_uid,
                        "pod_ns": pod_ns,
                        "pod_name": pod_name,
                        "pvc_name": claimed_pvc,
                    }
                )

with open('output/pvc-data.json') as f:
    pvc_data = json.load(f)

for pvc in pvc_data:
    pvc_name = pvc.get("pvc_name", "")
    pvc_ns = pvc.get("pvc_namespace", "")
    # for each PVC in pvc-data.json, see if there is a matching Pod UID/NS/Name
    for pod_pvc_pair in pvc_pod_mapping:
        if pod_pvc_pair["pvc_name"] == pvc_name and pod_pvc_pair["pod_ns"] == pvc_ns:
            pvc["bound_pod_name"] = pod_pvc_pair["pod_name"]
            pvc["bound_pod_uid"] = pod_pvc_pair["pod_uid"]
            break

# Write the result back out to pvc-data.json
with open('output/pvc-data.json', 'w') as f:
    pvc_data = json.dump(pvc_data, f, indent=4)


            

        
