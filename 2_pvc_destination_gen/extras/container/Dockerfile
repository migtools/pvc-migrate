from centos:latest

ENV USER_NAME=ssh \
    USER_UID=1001 \
    HOME=/opt/ssh

ARG sshkey=""
RUN dnf -y install openssh-server nss_wrapper rsync && dnf clean all
RUN sed -i 's|#PidFile.*$|PidFile /opt/ssh/sshd.pid|' /etc/ssh/sshd_config
RUN sed -i 's/#Port.*$/Port 2222/' /etc/ssh/sshd_config
RUN sed -i 's/etc/opt/' /etc/ssh/sshd_config
RUN chmod -R 777 /etc/ssh /opt
RUN echo "${sshkey}" > /authorized_keys && chmod 444 /authorized_keys 
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

EXPOSE 2222
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
CMD /usr/local/bin/entrypoint.sh
