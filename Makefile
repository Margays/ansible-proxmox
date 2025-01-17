MKFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ANSIBLE_INVENTORY_DIR := $(MKFILE_DIR)/example/inventory
ANSIBLE_USER := root

.ONESHELL:

.PHONY: release
release:
	echo "Releasing role to Ansible Galaxy"
	bash $(MKFILE_DIR)/.github/scripts/release.sh $(GALAXY_API_KEY) proxmox
