from centos:latest

ARG sshpass
RUN dnf -y install openssh-server rsync
RUN dnf clean all
RUN mkdir /var/run/sshd
RUN echo "root:${sshpass}" | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

EXPOSE 22

CMD ssh-keygen -A && \
    exec /usr/sbin/sshd -D


