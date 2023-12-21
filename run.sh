#!/bin/bash

set -ue

IMAGE=akkadeeemikk/chainlit:latest

docker run -it --rm -d \
    --ipc=host \
    --network=host \
  	-v ./:/app/ \
    --name=chainlit-app \
    --restart always \
    ${IMAGE} bash