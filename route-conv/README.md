This is an example for configuring a Kubernetes deployment to provide SSH
access to an OpenShift cluster.  The deployment runs OpenSSH and stunnel.
SSH clients connect through an OpenShift passthrough route using stunnel.

Example usage:

Create a host key-pair for sshd:

```
    /bin/ssh-keygen -q -t rsa -f ssh_host_rsa_key -C '' -N ''
```

Create a TLS key and certificate for stunnel:

```
    make -f /etc/pki/tls/certs/Makefile ./stunnel.pem
    openssl x509 -in stunnel.pem -out stunnel-crt.pem
    openssl pkey -in stunnel.pem -out stunnel-key.pem
```

Create secrets with the host key-pair and the stunnel key and certificate:

```
    oc -n default create secret generic sshd-host-keys --from-file=ssh_host_rsa_key --from-file=ssh_host_rsa_key.pub
    oc -n default create secret tls stunnel-certs --cert=stunnel-crt.pem --key=stunnel-key.pem
```

Create a configmap with an authorized SSH public key or keys:

```
    oc -n default create configmap ssh-authorized-keys --from-file=authorized_keys=$HOME/.ssh/id_rsa.pub
```

Create the deployment and related resources for sshd and stunnel:

```
    oc -n default apply -f stunnel.yaml
```

Write the stunnel client configuration file (note: replace the host name in
the connect setting with the host name from the "ssh" route created in the
previous step):

```
    cat > ./stunnel-client.conf <<'EOF'
    client=yes
    foreground = yes
    pid = 
    sslVersion = TLSv1.2
    syslog = no
    
    [ssh]
    CAfile = ./stunnel-crt.pem
    accept = 2222
    cert = ./stunnel-crt.pem
    connect = ssh-default.apps.ci-ln-pw141ct-d5d6b.origin-ci-int-aws.dev.rhcloud.com:443
    key = ./stunnel-key.pem
    verify = 2
    EOF
```

Start the stunnel client:

```
    stunnel ./stunnel-client.conf
```

Connect to the local stunnel endpoint using ssh:

```
    ssh root@127.0.0.1 -p 2222 -i ~/.ssh/id_rsa
```

