#!/bin/bash
_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
umask 77
PEM1=`/bin/mktemp /tmp/openssh.XXXXXX`
PEM2=`/bin/mktemp /tmp/openssh.XXXXXX`
/usr/bin/openssl req -utf8 -newkey rsa:2048 -keyout $PEM1 -nodes -x509 -days 365 -out $PEM2
cat $PEM1 >  $_dir/stunnel.pem
echo "" >> $_dir/stunnel.pem
cat $PEM2 >> $_dir/stunnel.pem
rm -f $PEM1 $PEM2
