FROM alpine:3.7
RUN yum update && yum install -y install postgresql-server postgresql postgresql-contrib; yum clean all
RUN userdel -r postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER postgreserver WITH SUPERUSER PASSWORD 'admin@123';" &&\
    createdb -O postgresdb postgreserver
EXPOSE 5432
CMD ["postgres"]
