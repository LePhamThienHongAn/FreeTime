Get Debug Symbol Here:
- https://wiki.ubuntu.com/Kernel/Systemtap
- CACHE:
  - GPG key import
    - >#16.04 and higher
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C8CAB6595FDFF622 
#older distributions
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ECDCAD72428D7C01 

  - Add repository config
    - >codename=$(lsb_release -c | awk  '{print $2}')
sudo tee /etc/apt/sources.list.d/ddebs.list << EOF
deb http://ddebs.ubuntu.com/ ${codename}      main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-security main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-updates  main restricted universe multiverse
deb http://ddebs.ubuntu.com/ ${codename}-proposed main restricted universe multiverse
EOF

    - >sudo apt-get update
sudo apt-get install linux-image-$(uname -r)-dbgsym

Setup VMWARE machine (DEBUG TARGET):
- Add this to vmx file
  - >#enable the gdb remote listener (so we can debug from another VM or machine)
debugStub.listen.guest64.remote = "TRUE"
#wait for debuger attacth to this machine
monitor.debugOnStartGuest64 = "TRUE"

Debug
- Turn on the DEBUG TARGET
- run gdb (on other computer)
- enter these command
  - >symbol-file [path-to-symbol-file]
target remote [ip-of-machine-running-vmware]:8832
