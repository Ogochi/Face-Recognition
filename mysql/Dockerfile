FROM mysql:8.0.2
ENV MYSQL_ROOT_PASSWORD example
ENV MYSQL_DATABASE baza
ENV MYSQL_USER michal
ENV MYSQL_PASSWORD kichal
COPY init.sql /docker-entrypoint-initdb.d
