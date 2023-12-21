IMAGE_NAME := akkadeeemikk/chainlit
CONTAINER_NAME := chainlit-app
DOCKER_TAG := latest
CI_REGISTRY := docker.io
ANSIBLE_FLAGS := -e docker_image=$(IMAGE_NAME) -e docker_tag=$(DOCKER_TAG) \
 -e playbook_dest=$(PWD)/deploy/ansible/playbook -e source_dir=$(PWD)/deploy/ansible/templates -e root=$(PWD)

build:
	docker build -f docker/app/Dockerfile -t $(IMAGE_NAME) .

# run the container
run_docker_app:
	echo "Starting docker container" && \
	docker run -it --rm \
		--ipc=host \
  		--network=host \
  		-v ./:/app/ \
  		--name $(CONTAINER_NAME) \
  		$(IMAGE_NAME) chainlit run app.py


full_deploy_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml \
		-e docker_image=$(IMAGE_NAME) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY) \
		-e playbook_dest=$(PWD)/deploy/ansible/playbook \
		-e source_dir=$(PWD)/deploy/ansible/templates \
		-e root=$(PWD)

deploy_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml \
		--skip-tags "pull","destroy","prepare_external" $(ANSIBLE_FLAGS)

stop_local:
	ansible-playbook -v -i deploy/ansible/inventory.ini  deploy/ansible/deploy_local.yml --tags 'destroy' $(ANSIBLE_FLAGS)