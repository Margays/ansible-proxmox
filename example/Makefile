MKFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ANSIBLE_INVENTORY_DIR := $(MKFILE_DIR)/inventory
ANSIBLE_USER := root

.ONESHELL:

.PHONY: install-requirements
install-requirements:
	cd $(MKFILE_DIR)
	test -d $(MKFILE_DIR)/.venv || python3 -m virtualenv $(MKFILE_DIR)/.venv
	. $(MKFILE_DIR)/.venv/bin/activate
	pip install -r $(MKFILE_DIR)/requirements.txt
	ansible-galaxy collection install --force-with-deps --force -r $(MKFILE_DIR)/requirements.yml

.PHONY: provision
provision: install-requirements
	cd $(MKFILE_DIR)
	. $(MKFILE_DIR)/.venv/bin/activate
	ansible-playbook -i $(ANSIBLE_INVENTORY_DIR)/main.yaml $(MKFILE_DIR)/playbooks/provision.yaml -u $(ANSIBLE_USER)
