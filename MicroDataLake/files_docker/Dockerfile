FROM puckel/docker-airflow:latest

USER root

# Instalar vim-tiny, una versión más ligera de vim
RUN apt-get update && apt-get install -y vim-tiny

USER airflow

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]

