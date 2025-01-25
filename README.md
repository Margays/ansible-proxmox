# Ansible Collection - margays.proxmox

## Description

This collection provides modules and plugins for managing Proxmox VE environments using Ansible. It includes modules for managing virtual machines, storage, networks, and other Proxmox resources.

## Installation

To install this collection, use the following command:

```bash
ansible-galaxy collection install margays.proxmox
```

## Usage

Here are some examples of how to use the modules in this collection:

### Create a VM

```yaml
- name: Create VM
  margays.proxmox.node_qemu:
    node: "testprox"
    vmid: "101"
    name: "testvm"
    cores: 2
    memory: 4096
    tags: "test"
    pool: "test"
    net:
      - idx: 0
        model: virtio
        bridge: vmbr0
        tag: 102
      - idx: 1
        model: virtio
        bridge: vmbr0
        tag: 102
      - idx: 2
        model: virtio
        bridge: vmbr0
        tag: 103
    scsi:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    ide:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    sata:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    virtio:
      - idx: 0
        storage: local-lvm
        size: 1
        cache: writeback
    state: present
```

### Delete a VM

```yaml
- name: Delete VM
  margays.proxmox.node_qemu:
    node: "testprox"
    vmid: "101"
    destroy_unreferenced_disks: true
    state: absent
```

## Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This collection is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more details.
