#!/bin/bash

USER_ID=$(id -u)

if [ x"$USER_ID" == x"0" ]; then
  export HOME=/root
fi

mkdir -p ${HOME}/.ssh && chmod 700 ${HOME}/.ssh
echo ${SSH_PUBLIC_KEY} > ${HOME}/.ssh/authorized_keys
chmod 600 ${HOME}/.ssh/authorized_keys

if [ x"$USER_ID" != x"0" ]; then
    NSS_WRAPPER_PASSWD=/tmp/passwd.nss_wrapper
    NSS_WRAPPER_GROUP=/tmp/group.nss_wrapper

    cp /etc/passwd $NSS_WRAPPER_PASSWD
    cp /etc/group $NSS_WRAPPER_GROUP
    sed -i '$ d' $NSS_WRAPPER_PASSWD
    echo "${USER_NAME:-ssh}:x:$(id -u):0:${USER_NAME:-ssh} user:${HOME}:/bin/bash" >> $NSS_WRAPPER_PASSWD
    echo "${USER_NAME:-ssh}:x:$(id -u):${USER_NAME:-ssh}" >> $NSS_WRAPPER_GROUP
    export NSS_WRAPPER_PASSWD
    export NSS_WRAPPER_GROUP

    LD_PRELOAD=/usr/lib64/libnss_wrapper.so
    export LD_PRELOAD
fi

sed -i 's/#Port.*$/Port 2222/' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
ssh-keygen -A 

if [ x"$USER_ID" != x"0" ]; then
  cp /etc/ssh/ssh_host_* /opt/ssh/
  cp /etc/ssh/sshd_config /opt/ssh
  cp /etc/ssh/moduli /opt/ssh
  sed -i 's/etc/opt/' /opt/ssh/sshd_config
  sed -i "s/UsePAM yes/UsePAM no/" /opt/ssh/sshd_config
  sed -i 's|#PidFile.*$|PidFile /opt/ssh/sshd.pid|' /opt/ssh/sshd_config
  chown -R ssh:ssh /opt/ssh
  exec /usr/sbin/sshd -D -f /opt/ssh/sshd_config
else
  exec /usr/sbin/sshd -D
fi

