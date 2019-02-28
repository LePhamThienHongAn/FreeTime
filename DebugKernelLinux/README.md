<p>Get Debug Symbol Here:</p>
<ul>
<li>Thttps://wiki.ubuntu.com/Kernel/Systemtap</li>
<li>CACHE:
<ul>
<li>
<p>GPG key import</p>
<ul>
<li>
<blockquote>
<p>#16.04 and higher<br>
sudo apt-key adv --keyserver  <a href="http://keyserver.ubuntu.com/">keyserver.ubuntu.com</a>  --recv-keys C8CAB6595FDFF622<br>
#older distributions<br>
sudo apt-key adv --keyserver  <a href="http://keyserver.ubuntu.com/">keyserver.ubuntu.com</a>  --recv-keys ECDCAD72428D7C01</p>
</blockquote>
</li>
</ul>
</li>
<li>
<p>Add repository config</p>
<ul>
<li>
<blockquote>
<p>codename=$(lsb_release -c | awk ‘{print $2}’)<br>
sudo tee /etc/apt/sources.list.d/ddebs.list &lt;&lt; EOF<br>
deb  <a href="http://ddebs.ubuntu.com/">http://ddebs.ubuntu.com/</a>  ${codename} main restricted universe multiverse<br>
deb  <a href="http://ddebs.ubuntu.com/">http://ddebs.ubuntu.com/</a>  ${codename}-security main restricted universe multiverse<br>
deb  <a href="http://ddebs.ubuntu.com/">http://ddebs.ubuntu.com/</a>  ${codename}-updates main restricted universe multiverse<br>
deb  <a href="http://ddebs.ubuntu.com/">http://ddebs.ubuntu.com/</a>  ${codename}-proposed main restricted universe multiverse<br>
EOF</p>
</blockquote>
</li>
<li>
<blockquote>
<p>sudo apt-get update<br>
sudo apt-get install linux-image-$(uname -r)-dbgsym</p>
</blockquote>
</li>
</ul>
</li>
<li>
<p>Your symbol file will be here /usr/lib/debug/boot/</p>
</li>
</ul>
</li>
</ul>
<p>Setup VMWARE machine (DEBUG TARGET):</p>
<ul>
<li>Add this to vmx file
<ul>
<li>
<blockquote>
<p>#enable the gdb remote listener (so we can debug from another VM or machine)<br>
debugStub.listen.guest64.remote = “TRUE”<br>
#wait for debuger attacth to this machine<br>
monitor.debugOnStartGuest64 = “TRUE”</p>
</blockquote>
</li>
</ul>
</li>
</ul>
<p>Debug</p>
<ul>
<li>Turn on the DEBUG TARGET</li>
<li>run gdb (on other computer)</li>
<li>enter these command
<ul>
<li>
<blockquote>
<p>symbol-file [path-to-symbol-file]<br>
target remote [ip-of-machine-running-vmware]:8832</p>
</blockquote>
</li>
</ul>
</li>
</ul>
