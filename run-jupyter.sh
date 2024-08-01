#!/bin/bash
#docker run -d -p 8888:8888 -v //c/Users/cgsilveriot/Engineer/work:/home/jovyan/work jupyter/all-spark-notebook start-notebook.sh --NotebookApp.token=''
docker run -d -p 8888:8888 -v /mnt/c/Users/cgsilveriot/Engineer/work:/home/jovyan/work jupyter/all-spark-notebook start-notebook.sh --NotebookApp.token=''
