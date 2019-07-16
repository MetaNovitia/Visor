sudo apt-get install qemu-kvm libvirt-bin bridge-utils virtinst ovmf qemu-utils

sudo vi /etc/default/grub
# Make this line look like this
# GRUB_CMDLINE_LINUX="intel_iommu=on iommu=pt rd.driver.pre=vfio-pci video=efifb:off"
sudo update-grub
sudo vi /etc/initramfs-tools/modules
#vfio
#vfio_iommu_type1
#vfio_pci
#vfio_virqfd
sudo update-initramfs -u

lspci -nnk | grep -i nvidia
#02:00.0 VGA compatible controller [0300]: NVIDIA Corporation GM204 [GeForce GTX 980] [10de:13c0] (rev a1)
#02:00.1 Audio device [0403]: NVIDIA Corporation GM204 High Definition Audio Controller [10de:0fbb] (rev a1)

sudo vi /etc/modprobe.d/local.conf
#options vfio-pci ids=10de:13c0,10de:0fbb
#options vfio-pci disable_vga=1
sudo vi /etc/modprobe.d/vfio.conf
sudo echo 'vfio-pci' > /etc/modules-load.d/vfio-pci.conf


sudo find /sys/kernel/iommu_groups/ -type l
sudo vi /etc/modprobe.d/blacklist-nouveau.conf
#blacklist nouveau
#options nouveau modeset=0

