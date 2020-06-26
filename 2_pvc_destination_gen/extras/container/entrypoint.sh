#!/bin/bash
mkdir -p ${HOME}/.ssh && chmod 700 ${HOME}/.ssh
cp /authorized_keys ${HOME}/.ssh/authorized_keys && chmod 600 ${HOME}/.ssh/authorized_keys

USER_ID=$(id -u)

if [ x"$USER_ID" != x"0" -a x"$USER_ID" != x"1001" ]; then
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

ssh-keygen -A
cp /etc/ssh/ssh_host_* /opt/ssh/
cp /etc/ssh/sshd_config /opt/ssh
cp /etc/ssh/moduli /opt/ssh
sed -i "s/UsePAM yes/UsePAM no/" /opt/ssh/sshd_config
chown -R ssh:ssh /opt/ssh

exec /usr/sbin/sshd -De -f /opt/ssh/sshd_config
