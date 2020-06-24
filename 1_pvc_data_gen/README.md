# pvc-data-gen

## Usage:

1. Create your own copy of vars file 
```
cp vars/pvc-data-gen.yml.example vars/pvc-data-gen.yml
```

2. Edit `vars/pvc-data-gen.yml` adding a list of namespaces
```
namespaces_to_migrate:
- rocket-chat
- mssql-persistent
```

3. Run playbook while kubeconfig is set for connection to source cluster
```
export KUBECONFIG="/path/to/src_cluster_kubeconfig"
ansible-playbook pvc-data-gen.yml
```

4. Examine generated output
```
cat output/pvc-data.json  
```
