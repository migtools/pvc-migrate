from centos:latest

RUN dnf -y install openssh-server rsync
RUN dnf clean all
RUN mkdir -p /root/.ssh/ && chmod 600 /root/.ssh/
RUN mkdir /var/run/sshd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

EXPOSE 22

CMD ssh-keygen -A && \
    exec /usr/sbin/sshd -De


