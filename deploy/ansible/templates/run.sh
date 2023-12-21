#!/bin/bash

set -ue

IMAGE={{ docker_image }}:{{ docker_tag }}

docker run -it --rm -d \
    --ipc=host \
    --network=host \
  	-v {{ root }}/:/app/ \
    --name={{ container_name }} \
    ${IMAGE} chainlit run app.py