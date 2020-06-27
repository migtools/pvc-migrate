from centos:latest

ENV USER_NAME=ssh \
    USER_UID=1001 \
    HOME=/opt/ssh

RUN dnf -y install openssh-server nss_wrapper rsync && dnf clean all
RUN chmod -R 777 /etc/ssh /opt

EXPOSE 2222
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
CMD /usr/local/bin/entrypoint.sh
