#!/bin/bash
rm -rf build
collection="${2%*/}"
echo "Releasing collection $collection"
ansible-galaxy collection build --output-path build
ansible-galaxy collection publish build/margays-$collection-*.tar.gz \
    --api-key $GALAXY_API_KEY \
    --server="https://galaxy.ansible.com/"
