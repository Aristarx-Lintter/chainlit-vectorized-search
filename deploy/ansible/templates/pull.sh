#!/bin/bash

set -ue

docker pull {{ docker_image }}:{{ docker_tag }}
