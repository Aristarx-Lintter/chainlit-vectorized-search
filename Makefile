IMAGE_NAME := akkadeeemikk/chainlit
CONTAINER_NAME := chainlit-app
DOCKER_TAG := latest
CI_REGISTRY := docker.io
ANSIBLE_FLAGS := -e docker_image=$(IMAGE_NAME) -e docker_tag=$(DOCKER_TAG) \
 -e playbook_dest=$(PWD)/deploy/ansible/playbook -e source_dir=$(PWD)/deploy/ansible/templates -e root=$(PWD)

build:
	docker build -f docker/app/Dockerfile -t $(IMAGE_NAME) .

run_docker_app:
	echo "Starting chainlit app container" && \
	docker run -it --rm \
		--ipc=host \
  		--network=host \
  		-v ./:/app/ \
  		--name $(CONTAINER_NAME) \
  		$(IMAGE_NAME) chainlit run src/app.py

stop:
	docker stop $(CONTAINER_NAME)


ansible_external_deploy_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml \
		--skip-tags "destroy"$(ANSIBLE_FLAGS)

ansible_deploy_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml \
		--skip-tags "pull","destroy","prepare_external" $(ANSIBLE_FLAGS)

ansible_stop_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml --tags 'destroy' $(ANSIBLE_FLAGS)

create_env:
	cp .env_template .env
