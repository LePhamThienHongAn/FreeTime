# Intro
Thiết bị: dùng giả lập qemu (qemu-system-mips) <br>
Hệ điều hành hoàn chỉnh cần kernel và image ổ cứng chứa sẵn các file system.
- kernel: source https://mirrors.edge.kernel.org/pub/linux/kernel/
- file system (rootfs): busybox-base git.busybox.net/buildroot

# Prepare
## Chuẩn bị môi trường
```
apt install git
apt install make gcc g++
apt install libncursesw5-dev libssl-dev
apt install qemu-system-mips
apt install unzip
```
libncursesw5-dev libssl-dev cần cho lệnh make menuconfig <br>
qemu-system-mips giả lập thiết bị mips <br>
unzip cần cho build rootfs

## Chuẩn bị compiler
Tham khảo: https://www.mips.com/develop/linux/ <br>
Theo đề xuất trên website của mips thì họ sử dụng ver kernel 4.8 và kernel 4.8.1 được release vào 07-Oct-2016 nên sẽ sử dụng compiler codescape 2016.05-08 (codescape là compiler chính thức của mips.com) <br>

Binary: https://codescape.mips.com/components/toolchain/2016.05-08/downloads.html

```
mkdir compiler
cd compiler
wget https://codescape.mips.com/components/toolchain/2016.05-08/Codescape.GNU.Tools.Package.2016.05-08.for.MIPS.IMG.Linux.CentOS-5.x86_64.tar.gz
tar -xf Codescape.GNU.Tools.Package.2016.05-08.for.MIPS.IMG.Linux.CentOS-5.x86_64.tar.gz
cd ..
```

# Build
## Build kernel
Các version kernel: https://mirrors.edge.kernel.org/pub/linux/kernel/ <br>
Tải source kernel 4.8.1 và giải nén
```
mkdir linux_kernel
cd linux_kernel
wget https://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/linux-4.8.1.tar.gz
tar -xf linux-4.8.1.tar.gz
```
Build kernel 4.8.1
```
cd linux-4.8.1
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu- malta_defconfig 
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu- menuconfig 
make -j4 ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu-
```
`make malta_defconfig` chọn loại machine mặc định là malta <br>
`make menuconfig` lưu ý các cấu hình quan trọng như `endianness`, `CPU`. Khuyến nghị chọn `CPU mips32 Release 6` vì qemu hỗ trợ CPU này. Chạy lệnh `qemu-system-mips -cpu help` để biết qemu-system-mips hỗ trợ những CPU nào. <br>
`make -j4` bắt đầu build kernel

Copy vmlinux về thư mục riêng
```
mkdir ../../final_result
cp vmlinux ../../final_result/vmlinux-4.8.1-mips32r6
cd ../../
```

## Build rootfs
Tải source busybox buildroot
```
mkdir busybox_base
cd busybox_base
git clone git://git.busybox.net/buildroot buildroot
```
Build busybox buildroot
```
cd buildroot
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu- menuconfig
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu-
cp output/images/rootfs.tar ../
cd ../../
```
`make menuconfig` lưu ý chọn các option
```
Target options  --->
    Target Architecture  --->
        MIPS (big endian)
    Target Architecture Variant  --->
        Generic MIPS32R6
```
# Make img with busybox rootfs
```
cd final_result
qemu-img create vmlinux-4.8.1-mips32r6.ext2 512M
mkfs.ext2 vmlinux-4.8.1-mips32r6.ext2
mkdir tmp_mnt_rfs
mount vmlinux-4.8.1-mips32r6.ext2 tmp_mnt_rfs -t ext2
tar -C tmp_mnt_rfs -xvf ../busybox_base/rootfs.tar
umount tmp_mnt_rfs
```
# RUN!
```
qemu-system-mips \
-M malta \
-cpu mips32r6-generic \
-kernel vmlinux-4.8.1-mips32r6 \
-hda vmlinux-4.8.1-mips32r6.ext2 \
-append "root=/dev/sda init=/bin/sh" \
-nographic
```
# Just in case ... 404
https://drive.google.com/drive/u/3/folders/1wUMNLL79QGDqW3N4Sn2cROjHAIhcUVcG
