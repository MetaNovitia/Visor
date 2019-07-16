sudo apt-get install gparted
wget http://downloads.sourceforge.net/project/e2fsprogs/e2fsprogs/v1.43.1/e2fsprogs-1.43.1.tar.gz
tar xzf e2fsprogs-1.43.1.tar.gz
cd e2fsprogs-1.43.1
./configure # <== if this step fail, check the config.log file, it could just be that you are missing the "libc6-dev" package on your system
make
sudo cp e2fsck/e2fsck /sbin/e2fsck
#sudo cp resize/resize2fs /sbin/resize2fs
