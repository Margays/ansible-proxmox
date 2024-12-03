MKFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ANSIBLE_INVENTORY_DIR := $(MKFILE_DIR)/example/inventory
ANSIBLE_USER := root

.ONESHELL:

.PHONY: example-ansible-requirements
example-ansible-requirements:
	cd $(MKFILE_DIR)
	test -d $(MKFILE_DIR)/.venv || python3 -m virtualenv $(MKFILE_DIR)/.venv
	. $(MKFILE_DIR)/.venv/bin/activate
	pip install ansible

.PHONY: example-provision
example-provision: example-ansible-requirements
	cd $(MKFILE_DIR)
	. $(MKFILE_DIR)/.venv/bin/activate
	cd $(MKFILE_DIR)/plugins
	ansible-playbook -i $(ANSIBLE_INVENTORY_DIR)/main.yaml provision.yaml -u $(ANSIBLE_USER)

.PHONY: release
release:
	echo "Releasing role to Ansible Galaxy"
	bash $(MKFILE_DIR)/.github/scripts/release.sh $(GALAXY_API_KEY) $(COLLECTION_NAME)
