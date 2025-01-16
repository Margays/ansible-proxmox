MKFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

.ONESHELL:

.PHONY: release
release:
	echo "Releasing role to Ansible Galaxy"
	bash $(MKFILE_DIR)/.github/scripts/release.sh $(GALAXY_API_KEY) proxmox
