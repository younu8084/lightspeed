FROM docker-enterprise-prod.artifactrepository.citigroup.net/developersvcs-python-ai/redhat-python3.6/rhel7/redhat-python-rhel7:latest
COPY *.repo /etc/yum.repos.d/
RUN yum -y install postgresql-server postgresql postgresql-contrib postgis supervisor pwgen; yum clean all
COPY entrypoint.sh /tmp/
RUN mkdir /usr/local/pgsql
RUN chown postgres /usr/local/pgsql
RUN userdel -r postgres
RUN useradd -u 1001 -r -g 0 -d /usr/local/pgsql -s /sbin/nologin \
      -c "Postgress Admin" postgres && \
  chown -R 1001:0 /usr/local/pgsql
RUN chgrp -R 0 /var/run/postgresql/ && \
    chmod -R g+rwX /var/run/postgresql/
USER 1001
ENTRYPOINT ["/tmp/entrypoint.sh"]
EXPOSE 5432
CMD ["postgres"]