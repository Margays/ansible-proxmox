#!/bin/bash

bump_version() {
    if [ -z "$1" ]; then
        echo "No version type provided"
        exit 1
    fi
    echo "Bumping version"
    pip install -r .github/scripts/release/requirements.txt
    python .github/scripts/release/update_version.py $1
}

release() {
    rm -rf build
    collection="$1"
    echo "Releasing collection margays.${collection}"
    ansible-galaxy collection build --output-path build
    ansible-galaxy collection publish build/margays-${collection}-*.tar.gz \
        --api-key $GALAXY_API_KEY \
        --server="https://galaxy.ansible.com/"
}

commit_changes() {
    git config --global user.email "github-actions[bot]@users.noreply.github.com"
    git config --global user.name "github-actions[bot]"
    git add .
    local current_version=$(grep -oP 'version: \K[0-9]+\.[0-9]+\.[0-9]+' galaxy.yml)
    git commit -m "Release version $current_version"
    git tag $current_version
    git push
    git push origin tag $current_version
}

main() {
    if [ -z "$1" ]; then
        echo "No version type provided"
        exit 1
    fi
    bump_version $1
    release "proxmox"
}

main $1
