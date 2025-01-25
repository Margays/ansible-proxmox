MKFILE_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
ANSIBLE_INVENTORY_DIR := $(MKFILE_DIR)/example/inventory
ANSIBLE_USER := root

.ONESHELL:

.PHONY: release
release:
	echo "Releasing role to Ansible Galaxy"
	bash $(MKFILE_DIR)/.github/scripts/release.sh $(GALAXY_API_KEY) proxmox
	sed -i 's/^version: .*/version: $$(python -c "import semver; print(semver.VersionInfo.parse(open(\"galaxy.yml\").read().split(\"version: \")[1].split()[0]).bump_patch())")/' galaxy.yml
	git add galaxy.yml
	git commit -m "Bump version in galaxy.yml"
	git push

.PHONY: test
test:
	echo "Running tests"
	cd $(MKFILE_DIR)/plugins
	export PYTHONPATH=$(MKFILE_DIR)/plugins
	pytest test
