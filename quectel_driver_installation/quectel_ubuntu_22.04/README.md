[TOC]
# ***KERNEL CONFIGURATION FOR USB DRIVERS***
`$ cd /usr/src/linux-headers-$(uname -r)`

`$ export ARCH=arm`

`$ export CROSS_COMPILE=arm-none-linux-gnueabi-`

`$ sudo apt-get install make gcc flex bison net-tools pkg-config libncurses-dev`

`$ sudo make bcmrpi_defconfig`
~~~
  - **ERROR**: couldn't find bcmrpi_defconfig 
  - GETTING THIS ERROR IS OK, PLEASE PROCEED. (There is an appendix at the end, you can check if errors are the same)
~~~
`$ sudo make menuconfig`
-**IT WILL SHOW A MENU, SELECT THESE BELOW TO COMPILE KERNEL:**
~~~
  - Device Drivers
    - USB support
	    - USB Serial Converter Support (default value <M>, press Y to make it <*> , then press Enter)
	    - USB Driver for GSM and CDMA modems (default value <M>, press Y to make it <*> , then press Enter)

    - Device Drivers
      - Network device support
        - USB Network Adapters (default value {M}, press Y to make it {*} , then press Enter
          - Multi-purpose USB Networking Framework (default value {M}, press Y to make it {*})
          - QMI WWAN driver for Qualcomm MSM based 3G and LTE Modems (default value <M>, press Y to make it <*>)
~~~
-**THEN FIRST SAVE, OVERWRITE .config FILE, THEN EXIT THE MENU**

# **QMI_WWAN AND OPTION DRIVERS INSTALLATION**

- Extract Quectel_Linux&Android_QMI_WWAN_Driver_V1.2.1.zip into a folder
- Change the name of the folder qmi_wwan (can be any name, but & symbol is not supported)
- Go inside this folder, where the makefile is located, then run:

`$ sudo make install`
- There will be some errors and warnings saying something similar to this:
  "The kernel was built by: x86_64-linux-gnu-gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0   
  You are using: gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0"
**GETTING THIS ERROR IS ALSO OK.**

- Extract Quectel_Linux_USB_Serial_Option_Driver_20200720.tgz into a folder
- Then inside this folder there are folders of kernel versions, for ubuntu 22.04.2 
- with kernel version 5.19.0, go inside the v5.19.1 folder and then run

  `$ sudo make install`
**There should be no errors present in this installment.**

# **CHECKING IF THE DRIVERS ARE INSTALLED**

**Now to see if the drivers are installed, run this:**
  `$ ls /sys/bus/usb/drivers`
  - The output should include "option" and "qmi_wwan" drivers
  - if they are not visible (generally the case), plug QUECTEL
  - module into a USB3 port and run this command again, they should be visible



# **PDU SESSION ESTABLISHMENT MANAGER**


- Now install QconnectManager for PDU session establishment

- Extract QconnectManager_Linux_V1.6.1.zip into a folder

- Go inside the folder and run:

  `$ sudo make`

- Now after starting CN and gNB, and be sure that Quectel Module is open, then inside QconnectManager folder
  
  `$ sudo ./quectel-CM`
  **You should see the wwan0 interface is set up in ifconfig, and you should be also able to ping anywhere.**


# **TESTING IF THE DRIVERS ARE PROPERLY WORKING**


- After connecting the module to the PC via USB3 port, run this command to see if the drivers are working properly 
- and the device is seen by PC: (if they are not listed, then something is wrong, maybe try PLUGGING quectel again)
  
  `$ ls /dev/ttyUSB*`
  - The output should list these devices: /dev/ttyUSB0 /dev/ttyUSB1 /dev/ttyUSB2 /dev/ttyUSB3
  - /dev/ttyUSB2 is for sending the AT directives

- if you want to send AT directives, run:
  
  `$ sudo busybox microcom /dev/ttyUSB2`
  - After this command, you’ll see no output, but the terminal will be expecting for an input, therefore 
  - you can directly copy the following for starting the quectel module (blue LED means it is started already)


## **APPENDIX OF ERRORS AND OUTPUTS**

### **ERROR MESSAGE WHEN TRYING TO MAKE bcmrpi_defconfig**
~~~
  ***
  *** Can't find default configuration "arch/x86/configs/bcmrpi_defconfig"!
  ***
  scripts/kconfig/Makefile:90: recipe for target 'bcmrpi_defconfig' failed
  make[1]: *** [bcmrpi_defconfig] Error 1
  Makefile:617: recipe for target 'bcmrpi_defconfig' failed
  make: *** [bcmrpi_defconfig] Error 2
~~~

### **ERROR MESSAGE WHEN INSTALLING qmi_wwan driver**
~~~
  qq22@qq22:~/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan$ sudo make install
  make ARCH=x86_64 CROSS_COMPILE= -C /lib/modules/5.19.0-42-generic/build M=/home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan modules
  make[1]: Entering directory '/usr/src/linux-headers-5.19.0-42-generic'
  warning: the compiler differs from the one used to build the kernel
    The kernel was built by: x86_64-linux-gnu-gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0
    You are using:           gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.o
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c: In function ‘bridge_arp_reply’:
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:322:13: error: implicit declaration of function ‘netif_rx_ni’; did you mean ‘netif_rx’? [-Werror=implicit-function-declaration]
    322 |             netif_rx_ni(reply);
        |             ^~~~~~~~~~~
        |             netif_rx
  In file included from ./include/linux/string.h:253,
                  from ./include/linux/bitmap.h:11,
                  from ./include/linux/cpumask.h:12,
                  from ./arch/x86/include/asm/cpumask.h:5,
                  from ./arch/x86/include/asm/msr.h:11,
                  from ./arch/x86/include/asm/processor.h:22,
                  from ./arch/x86/include/asm/timex.h:5,
                  from ./include/linux/timex.h:67,
                  from ./include/linux/time32.h:13,
                  from ./include/linux/time.h:60,
                  from ./include/linux/stat.h:19,
                  from ./include/linux/module.h:13,
                  from /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:13:
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c: In function ‘qmap_register_device’:
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:1261:21: warning: passing argument 1 of ‘__builtin_memcpy’ discards ‘const’ qualifier from pointer target type [-Wdiscarded-qualifiers]
  1261 |     memcpy (qmap_net->dev_addr, real_dev->dev_addr, ETH_ALEN);
        |             ~~~~~~~~^~~~~~~~~~
  ./include/linux/fortify-string.h:379:27: note: in definition of macro ‘__fortify_memcpy_chk’
    379 |         __underlying_##op(p, q, __fortify_size);                        \
        |                           ^
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:1261:5: note: in expansion of macro ‘memcpy’
  1261 |     memcpy (qmap_net->dev_addr, real_dev->dev_addr, ETH_ALEN);
        |     ^~~~~~
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:1261:21: note: expected ‘void *’ but argument is of type ‘const unsigned char *’
  1261 |     memcpy (qmap_net->dev_addr, real_dev->dev_addr, ETH_ALEN);
        |             ~~~~~~~~^~~~~~~~~~
  ./include/linux/fortify-string.h:379:27: note: in definition of macro ‘__fortify_memcpy_chk’
    379 |         __underlying_##op(p, q, __fortify_size);                        \
        |                           ^
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:1261:5: note: in expansion of macro ‘memcpy’
  1261 |     memcpy (qmap_net->dev_addr, real_dev->dev_addr, ETH_ALEN);
        |     ^~~~~~
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c: In function ‘qmi_wwan_bind’:
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:2028:39: error: assignment of read-only location ‘*dev->net->dev_addr’
  2028 |                 dev->net->dev_addr[0] |= 0x02;  /* set local assignment bit */
        |                                       ^~
  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.c:2029:39: error: assignment of read-only location ‘*dev->net->dev_addr’
  2029 |                 dev->net->dev_addr[0] &= 0xbf;  /* clear "IP" bit */
        |                                       ^~
  cc1: some warnings being treated as errors
  make[2]: *** [scripts/Makefile.build:257: /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan/qmi_wwan_q.o] Error 1
  make[1]: *** [Makefile:1850: /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qmi_wwan] Error 2
  make[1]: Leaving directory '/usr/src/linux-headers-5.19.0-42-generic'
  make: *** [Makefile:28: default] Error 2
~~~
### **OUTPUT OF INSTALLATION OF USB_SERIAL_OPTION DRIVER**
~~~
  qq22@qq22:~/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1$ sudo make install
  [sudo] password for qq22: 
  make -C /lib/modules/5.19.0-42-generic/build M=/home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1 clean
  make[1]: Entering directory '/usr/src/linux-headers-5.19.0-42-generic'
  make[1]: Leaving directory '/usr/src/linux-headers-5.19.0-42-generic'
  make -C /lib/modules/5.19.0-42-generic/build M=/home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1 modules
  make[1]: Entering directory '/usr/src/linux-headers-5.19.0-42-generic'
  warning: the compiler differs from the one used to build the kernel
    The kernel was built by: x86_64-linux-gnu-gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0
    You are using:           gcc (Ubuntu 11.3.0-1ubuntu1~22.04.1) 11.3.0
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/option.o
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/usb_wwan.o
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/qcserial.o
    MODPOST /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/Module.symvers
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/option.mod.o
    LD [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/option.ko
    BTF [M] /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/option.ko
  Skipping BTF generation for /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/option.ko due to unavailability of vmlinux
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/qcserial.mod.o
    LD [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/qcserial.ko
    BTF [M] /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/qcserial.ko
  Skipping BTF generation for /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/qcserial.ko due to unavailability of vmlinux
    CC [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/usb_wwan.mod.o
    LD [M]  /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/usb_wwan.ko
    BTF [M] /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/usb_wwan.ko
  Skipping BTF generation for /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/./drivers/usb/serial/usb_wwan.ko due to unavailability of vmlinux
  make[1]: Leaving directory '/usr/src/linux-headers-5.19.0-42-generic'
  cp /home/qq22/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/usb_serial_option/20220902/v5.19.1/drivers/usb/serial/*.ko /lib/modules/5.19.0-42-generic/kernel/drivers/usb/serial/
  depmod
~~~
### **QCONNECTMANAGER OUTPUT THAT PROVIDES THE SUCCESFUL PDU SESSION**
~~~
  qq22@qq22:~/5G_LTE_Linux_Tools_Drivers_20230227/Linux/serden/qconnect$ sudo ./quectel-CM 
  [05-26_14:08:42:394] QConnectManager_Linux_V1.6.4
  [05-26_14:08:42:394] Find /sys/bus/usb/devices/2-1 idVendor=0x2c7c idProduct=0x800, bus=0x002, dev=0x003
  [05-26_14:08:42:394] Auto find qmichannel = /dev/cdc-wdm0
  [05-26_14:08:42:394] Auto find usbnet_adapter = wwan0
  [05-26_14:08:42:394] netcard driver = qmi_wwan, driver version = 5.19.0-42-generic
  [05-26_14:08:42:394] Modem works in QMI mode
  [05-26_14:08:42:400] /proc/8638/fd/7 -> /dev/cdc-wdm0
  [05-26_14:08:42:400] /proc/8638/exe -> /usr/libexec/qmi-proxy
  [05-26_14:08:44:411] cdc_wdm_fd = 7
  [05-26_14:08:44:509] Get clientWDS = 2
  [05-26_14:08:44:541] Get clientDMS = 1
  [05-26_14:08:44:573] Get clientNAS = 4
  [05-26_14:08:44:605] Get clientUIM = 1
  [05-26_14:08:44:637] Get clientWDA = 1
  [05-26_14:08:44:669] requestBaseBandVersion RM500QGLABR11A04M4G
  [05-26_14:08:44:797] requestGetSIMStatus SIMStatus: SIM_READY
  [05-26_14:08:44:829] requestGetProfile[1] internet///0/IPV4V6
  [05-26_14:08:44:860] requestRegistrationState2 MCC: 999, MNC: 70, PS: Detached, DataCap: UNKNOW
  [05-26_14:08:44:893] requestRegistrationState2 MCC: 999, MNC: 70, PS: Detached, DataCap: UNKNOW
  [05-26_14:08:44:925] requestQueryDataCall IPv4ConnectionStatus: DISCONNECTED
  [05-26_14:08:44:925] ifconfig wwan0 0.0.0.0
  [05-26_14:08:44:928] ifconfig wwan0 down
  [05-26_14:08:47:358] requestRegistrationState2 MCC: 999, MNC: 70, PS: Attached, DataCap: 5G_SA
  [05-26_14:08:47:582] requestSetupDataCall WdsConnectionIPv4Handle: 0xe34cfac0
  [05-26_14:08:47:710] change mtu 1500 -> 1400
  [05-26_14:08:47:710] ifconfig wwan0 up
  [05-26_14:08:47:714] No default.script found, it should be in '/usr/share/udhcpc/' or '/etc//udhcpc' depend on your udhcpc version!
  [05-26_14:08:47:714] busybox udhcpc -f -n -q -t 5 -i wwan0
  udhcpc: started, v1.30.1
  udhcpc: sending discover
  udhcpc: sending select for 10.60.0.5
  udhcpc: lease of 10.60.0.5 obtained, lease time 7200
  [05-26_14:08:47:904] ip -4 address flush dev wwan0
  [05-26_14:08:47:905] ip -4 address add 10.60.0.5/30 dev wwan0
  [05-26_14:08:47:907] ip -4 route add default via 10.60.0.6 dev wwan0
~~~


### **AFTER QCONNECTMANAGER, THE INTERFACE THAT IS SET UP:**
~~~
wwan0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1400
  inet 10.60.0.5  netmask 255.255.255.252  destination 10.60.0.5
  inet6 fe80::4d30:1d0b:90a8:eca4  prefixlen 64  scopeid 0x20<link>
  unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 1000  (UNSPEC)
  RX packets 2  bytes 604 (604.0 B)
  RX errors 0  dropped 0  overruns 0  frame 0
  TX packets 3  bytes 704 (704.0 B)
  TX errors 1  dropped 0 overruns 0  carrier 0  collisions 0
~~~
























