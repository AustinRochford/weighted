#! /bin/bash

PORT=${PORT:-8888}
SRC_DIR=${SRC_DIR:-`pwd`}
NOTEBOOK_DIR=${NOTEBOOK_DIR:-$SRC_DIR/notebooks}

docker build -t weighted $SRC_DIR
docker run -d \
    -p $PORT:8888 \
    -v $SRC_DIR:/home/jovyan/weighted/ \
    -v $NOTEBOOK_DIR:/home/jovyan/work/ \
    --name weighted weighted \
    start-notebook.sh --NotebookApp.token=''
