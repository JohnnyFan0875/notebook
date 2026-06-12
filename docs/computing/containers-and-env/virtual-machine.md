# Virtual Machine (VirtualBox)

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

## Fix VirtualBox unable to copy and paste bidirectionally

[Link](https://medium.com/%E8%8A%B1%E5%93%A5%E7%9A%84%E5%A5%87%E5%B9%BB%E6%97%85%E7%A8%8B/%E8%A7%A3%E6%B1%BAvirtualbox%E7%84%A1%E6%B3%95%E9%9B%99%E5%90%91%E8%A4%87%E8%A3%BD%E8%B2%BC%E4%B8%8A-1554d5a81da0)

## How can I make my own account a sudoers on VirtualBox

```bash
su -                           # login root # the same password as user account
sudo adduser [username] sudo
su [username]
```

[Link](https://superuser.com/questions/1623376/how-can-i-make-my-own-account-a-sudoers-on-virtualbox)

## How to fix if terminal can not open

```bash
CTRL + ALT + F3  # 进入命令行模式 (需要返回桌面的CTRL + ALT + F1)

$ sudo localectl set-locale LANG=en_US.UTF-8
$ sudo reboot
```

![Image](https://1.bp.blogspot.com/-SdNHPYYSiQo/YLMaDXTpOFI/AAAAAAAAc04/uID-1vB6EBsMPvf1jh5ajhC4UDr_xtwbwCNcBGAsYHQ/s0/J1049_01_virtualbox_shared_folders.png)

[Link](https://www.jinnsblog.com/2021/05/virtualbox-shared-folder-permission-setting.html)

```bash
sudo usermod -aG vboxsf $USER
sudo reboot
```

## Resize windows

[Link](https://aprilyang.home.blog/2020/12/25/tips-for-smoother-virtual-machine/)
