FROM mysql:8.0.2
ENV MYSQL_ROOT_PASSWORD example
ENV MYSQL_DATABASE images_db
ENV MYSQL_USER michal
ENV MYSQL_PASSWORD pass
COPY init.sql /docker-entrypoint-initdb.d
