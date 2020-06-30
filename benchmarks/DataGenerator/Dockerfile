from centos:latest

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN mkdir -p /opt/mounts && chmod -R 777 /opt/mounts

RUN chmod +x /usr/local/bin/entrypoint.sh

CMD /usr/local/bin/entrypoint.sh
