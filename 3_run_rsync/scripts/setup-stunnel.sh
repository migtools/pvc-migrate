#!/bin/bash

_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
umask 77
PEM1=`mktemp /tmp/openssh.XXXXXX`
PEM2=`mktemp /tmp/openssh.XXXXXX`
/usr/bin/openssl req -utf8 -newkey rsa:2048 -keyout $PEM1 -nodes -x509 -days 365 -out $PEM2 -subj "/C=US/ST=NC/L=RDU/O=migration/CN=openshift.io"
cat $PEM1 >  $_dir/tls.key
cat $PEM2 > $_dir/tls.crt
rm -f $PEM1 $PEM2
