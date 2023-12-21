#!/bin/bash

set -ue

docker login -u {{ docker_registry_user }} -p {{ docker_registry_password }} {{ docker_registry }}

docker push {{ docker_image }}:{{ docker_tag }}