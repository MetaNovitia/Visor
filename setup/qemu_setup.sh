sudo apt-get install git libsdl2-dev libpixman-1-dev
git clone git://git.qemu.org/qemu.git -b stable-2.12 qemu_src
cd qemu_src
git submodule init
git submodule update --recursive
sudo ./configure --prefix=/usr \
                --enable-kvm \
                --enable-sdl \
                --disable-werror \
                --target-list=x86_64-softmmu
sudo make -j64
cd roms/seabios
sudo git checkout master
sudo LC_ALL=C make -j64
cd -
sudo make install
sudo cp `pwd`/roms/seabios/out/bios.bin /usr/bin/bios.bin

