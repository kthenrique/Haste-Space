# BEL3: ESS Project - Haste-Space

### Requested Devices
XMC4500 - Infinion
LIS3DH - 3-axis acceleration sensor

### Requested Software
python3
gcc-arm-none-eabi-5_4-2016q3


```bash
$ mkdir -p $HOME/Bin; cd $HOME/Bin  
$ curl -LO https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q3-update/+download/gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
$ tar xjf gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
$ echo 'export PATH=$HOME/Bin/gcc-arm-none-eabi-5_4-2016q3/bin:$PATH' >> $HOME/.bashrc  
$ rm -rf gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
```
