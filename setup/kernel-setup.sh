wget https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/snapshot/linux-e61dbe7992fa053ca64d33200a6c766e0538751e.tar.gz
tar -zxvf linux-e61dbe7992fa053ca64d33200a6c766e0538751e.tar.gz
mv linux-e61dbe7992fa053ca64d33200a6c766e0538751e linux-4.17.0
sudo apt-get install build-essential libncurses-dev bison flex libssl-dev gcc 
cd linux-4.17.0
make oldconfig
make -j $(nproc)
sudo make modules_install 
sudo make install 
sudo update-grub
