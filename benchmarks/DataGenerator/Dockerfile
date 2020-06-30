from centos:latest

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN mkdir -p /opt/mounts && chmod -R /opt/mounts

RUN chmod +x entrypoint.sh

CMD /usr/local/bin/entrypoint.sh
