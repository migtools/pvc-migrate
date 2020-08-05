FROM centos:latest

COPY generate_sample.sh /usr/local/bin/generate_sample.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN mkdir -p /opt/mounts && chmod -R 777 /opt/mounts

RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/generate_sample.sh

CMD /usr/local/bin/entrypoint.sh
