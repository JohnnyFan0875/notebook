# Vertual Machine

## Free up space in a `vdi` (VirtualBox Disk Image) file

1. Zero out free space inside the VM

- Run this **inside** Linux VM to fill the free space with zeroes. Deleted files are replaced with zeroes, making them compressible.

  ```bash
  sudo dd if=/dev/zero of=/EMPTY bs=1M
  sudo rm -f /EMPTY
  ```

2. Shut down VM (powered off)

3. Compact the VDI from host machine

    ```bash
    VBoxManage modifymedium disk /path/to/your-disk.vdi --compact
    ```