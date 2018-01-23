# Haste-Space

### Motivation
  - University project at the FH Technikum Wien
  - Familiarisation with a uC
  - Sensor <-> uC <-> Computer Communication

### Dependencies
  - HW:
    - XMC4500 - Infineon
    - LIS3DH - 3-axis acceleration sensor (https://www.adafruit.com/product/2809)
    - UART TTL Serial Cable (https://www.adafruit.com/product/954)

  - SW:
    - python3  
    - SEGGER J-Link
    - gcc-arm-none-eabi-5_4-2016q3  

### How to Play
  - The goal is to capture the star as fast as you can
  - You should avoid shooting meteors and other spaceships as it increases the timer at the end
  - **Navigation**:
    - Button 1: Shooting in game
    - Button 2: Pause in game
    - Button 2 followed by button 1: finish game and go to menu
    - Button 2: Transition of scenes (e.g. from Menu to About and vice-versa)

### Troubleshooting
  - If you're having problem building the code, maybe this can help:
```bash
$ mkdir -p $HOME/Bin; cd $HOME/Bin  
$ curl -LO https://launchpad.net/gcc-arm-embedded/5.0/5-2016-q3-update/+download/gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
$ tar xjf gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
$ echo 'export PATH=$HOME/Bin/gcc-arm-none-eabi-5_4-2016q3/bin:$PATH' >> $HOME/.bashrc  
$ rm -rf gcc-arm-none-eabi-5_4-2016q3-20160926-linux.tar.bz2  
```
