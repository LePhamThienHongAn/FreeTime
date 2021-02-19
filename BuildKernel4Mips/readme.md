# Intro
Thiết bị: dùng giả lập qemu (qemu-system-mips) <br>
Hệ điều hành hoàn chỉnh cần kernel và image ổ cứng chứa sẵn các file system.
- kernel: source https://mirrors.edge.kernel.org/pub/linux/kernel/
- file system (rootfs): busybox-base git.busybox.net/buildroot

# Prepare
## Chuẩn bị môi trường
```
apt install git
apt install make
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

## Build
### Build kernel
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
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu menuconfig 
make -j4 ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu
```
`make malta_defconfig` chọn loại machine mặc định là malta <br>
`make menuconfig` lưu ý các cấu hình quan trọng như endianness, CPU. Khuyến nghị chọn CPU mips32 Release 6 vì qemu hỗ trợ CPU này. Chạy lệnh `qemu-system-mips -cpu help` để biết qemu-system-mips hỗ trợ những CPU nào <br>
`make -j4` bắt đầu build kernel

Copy vmlinux về thư mục riêng
```
mkdir ../../final_result
cp vmlinux ../../final_result/vmlinux-4.8.1
cd ../../
```


### Build rootfs
Tải source busybox buildroot
```
mkdir busybox_base
cd busybox_base
git clone git://git.busybox.net/buildroot buildroot
```
Build busybox buildroot
```
cd buildroot
make ARCH=mips CROSS_COMPILE=../../compiler/mips-img-linux-gnu/2016.05-08/bin/mips-img-linux-gnu menuconfig 
```
`make menuconfig` lưu ý chọn các option
```
Target options  --->
    Target Architecture  --->
        MIPS (big endian)
    Target Architecture Variant  --->
        Generic MIPS32R6
```
