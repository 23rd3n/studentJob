[TOC]

**DE states the 3.74e9 n78 FR1 band for 5G NR**
**ogs states the config files used for Open5GS**
## Commands for running the config files
### gNB : 40MHz(106 PRB) || USRP version is selected in config ||
`sudo ./nr-softmodem --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.1x1.usrpb200_DE.conf --usrp-tx-thread-config 1 --continous-tx -E`
- the argument -E is for sample speed
- --continous-tx is for transmitting and receiving at the same time, if it gives a lot LLLLL on the stdout then remove this
### gNB : 20MHz(51 PRB) || USRP version is selected in config ||
`sudo ./nr-softmodem --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/name_of_the_config_file --usrp-tx-thread-config 1 --continous-tx`
- the argument -E is not used here

### UE : 20MHZ (51 PRB) || OAI UE || DE BAND (for gNB run with *_DEconf)
`sudo ./nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3739980000  --ssb 192 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf `
- -C states the center frequency, one can also find this frequency in the log of gNB which is stated as ul_CarrierFreq or dl_CarrierFreq
- --ssb 192 is required for OAI UE which doesn't do any blind decoding of SS/PBCH block

### UE : 40MHZ (106PRB) || OAI UE || DE BAND (*_DE.conf)
`sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3739980000  --ssb 192 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf  -E`

### UE : 20MHZ (51 PRB) || OAI UE || OTHER BAND 1 (*_serkut.conf)
`sudo ./nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3619200000 --ue-fo-compensation --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf` 
- For OTHER BAND 1, no --ssb parameter is required

### UE : 40MHZ (106PRB) || OAI UE || OTHER BAND 1 (*_serkut.conf)
`sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --ue-fo-compensation --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf  -E`
- For OTHER BAND 1, no --ssb parameter is required

### UE : 20MHZ (51 PRB) || OAI UE || OTHER BAND 2 (*_new.conf)
`sudo ./nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3309480000  --ssb 238 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf` 
- For OTHER BAND 2, --ssb = 238 parameter is required, as calculated below

### UE : 40MHZ (106PRB) || OAI UE || OTHER BAND 2 (*_new.conf)
`sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3309480000  --ssb 238 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf -E`
- For OTHER BAND 2, --ssb = 238 parameter is required, as calculated below

### UE (QUECTEL) UBUNTU
- After drivers are installed run the QconnectManager as explained in [here](../quectel_drivers/quectel_ubuntu_22.04/)
- as for my experience, `ssb_SubcarrierOffset = 12` should be present in the gNB config files for quectel to connect in DE band but in the others it was not required, explained another section below

### RFSIM
- For gNB only add the --rfsim argument to the same command:, also remove -E command
`sudo ./nr-softmodem --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.1x1.usrpb200_DE.conf --usrp-tx-thread-config 1 --continous-tx --rfsim`

- For UE add the rfsimulator server as:
`sudo RFSIMULATOR=10.162.148.140 ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3739980000  --ssb 192 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf --rfsim `

## Calculation of ssb value for OAI UEa
    From the gNB config for 51PRB, 20MHZ, fr1 band78:

    absoluteFrequencySSB       = 620736 (GSCN = 7715, 3311040000Hz) (center of SSB)
    dl_absoluteFrequencyPointA = 620020 (3300300000Hz)

    Using the difference between absoluteFrequencySSB and dl_absoluteFrequencyPointA

    3311040kHz − 3300300kHz = 10740kHz,

    I got the difference between pointA and 0th RE via

    10740kHz - 10RB*12(RE/RB)*30(kHz/RE) = 7140kHz
    (30kHz SCS, 20RB for SSB means 10RB I had to substract for initial RE)

    which led me the ssb start subcarrier:

    7140kHz / 30kHz = 238

    Therefore final terminal command for me to work nrUE is:
    sudo ./nr-uesoftmodem -r 51 --numerology 1 --band 78 -C 3309480000  --ssb 238 --ue-fo-compensation  --sa -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/ue.conf

## For Quectels to connect in DE band
- Add `ssb_SubcarrierOffset  = 12; ` which is the k_{SSB} value for the standard. Otherwise it cannot synchronize with gNB.
- This k_{SSB} value calculated using the information in the gNB config file and this [website](https://www.sqimway.com/nr_refA.php)
- Honestly, I don't know the exact calculation of k_SSB value, which is stated in the standard but above website with the help of `initialDLBWPcontrolResourceSetZero` in the gNB config value and `GSCN` , `ARFCN` values of the SSB carrier, one can learn which value should be chosen.
- In the normal commercial bands of n78, this command wasn't needed but for the open band of n78(3.7Ghz - 3.8 Ghz), this value is needed to be added.


## Some TDD configs
### From Mailing lists
**Generally, it has been required to change the sl_ahead variable inside RU structure of gNB config, but no info here**
**Maintaining a 5ms periodicity and numerology 1, the following configurations have been tested:**

    CONFIG 1: (5 dl_UL_TransmissionPeriodicity, 1 nrofDownlinkSlots, 6 nrofDownlinkSymbols, 3 nrofUplinkSlots, 6 nrofUplinkSymbols) UPLINK: 7 Mbps    /   DONWLINK: 27 Mbps

    CONFIG 2: (5 dl_UL_TransmissionPeriodicity, 2 nrofDownlinkSlots, 6 nrofDownlinkSymbols, 2 nrofUplinkSlots, 6 nrofUplinkSymbols) UPLINK: 7 Mbps    /   DONWLINK: 47 Mbps

    CONFIG 3: (6 dl_UL_TransmissionPeriodicity, 7 nrofDownlinkSlots, 6 nrofDownlinkSymbols, 2 nrofUplinkSlots, 6 nrofUplinkSymbols) UPLINK: 7 Mbps    /   DONWLINK: 55 Mbps

    CONFIG 4: (6 dl_UL_TransmissionPeriodicity, 6 nrofDownlinkSlots, 6 nrofDownlinkSymbols, 3 nrofUplinkSlots, 6 nrofUplinkSymbols) UPLINK: 10 Mbps    /   DONWLINK: 64 Mbps

    CONFIG 5: (6 dl_UL_TransmissionPeriodicity, 6 nrofDownlinkSlots, 5 nrofDownlinkSymbols, 3 nrofUplinkSlots, 5 nrofUplinkSymbols) UPLINK: 9,5 Mbps    /   DONWLINK: 63 Mbps

    CONFIG 6: (6 dl_UL_TransmissionPeriodicity, 6 nrofDownlinkSlots, 7 nrofDownlinkSymbols, 3 nrofUplinkSlots, 6 nrofUplinkSymbols) UPLINK: 10,5 Mbps    /   DONWLINK: 65 Mbps

    CONFIG 7: (6 dl_UL_TransmissionPeriodicity, 6 nrofDownlinkSlots, 3 nrofDownlinkSymbols, 3 nrofUplinkSlots, 10 nrofUplinkSymbols) UPLINK: 11 Mbps    /   DONWLINK: 55 Mbps

    CONFIG 8: (6 dl_UL_TransmissionPeriodicity, 2 nrofDownlinkSlots, 6 nrofDownlinkSymbols, 7 nrofUplinkSlots, 6 nrofUplinkSymbols) The gNB accept the TDD configuration but the UE didn’t register.

    CONFIG 9: (6 dl_UL_TransmissionPeriodicity, 5 nrofDownlinkSlots, 0 nrofDownlinkSymbols, 5 nrofUplinkSlots, 0 nrofUplinkSymbols) The gNB accept the TDD configuration but the UE didn’t register.

    CONFIG 10: (6 dl_UL_TransmissionPeriodicity, 7 nrofDownlinkSlots, 0 nrofDownlinkSymbols, 3 nrofUplinkSlots, 0 nrofUplinkSymbols) The gNB accept the TDD configuration but the UE didn’t register.

### We tested these
    You need to change the tdd section in the configuration file:

    for 2.5 ms TDD, with sl_ahead = 5

    #tdd-UL-DL-ConfigurationCommon
    # subcarrierSpacing
    # 0=kHz15, 1=kHz30, 2=kHz60, 3=kHz120
        referenceSubcarrierSpacing                                    = 1;
        # pattern1
        # dl_UL_TransmissionPeriodicity
        # 0=ms0p5, 1=ms0p625, 2=ms1, 3=ms1p25, 4=ms2, 5=ms2p5, 6=ms5, 7=ms10
        dl_UL_TransmissionPeriodicity                                 = 5;
        nrofDownlinkSlots                                             = 3;
        nrofDownlinkSymbols                                           = 6;
        nrofUplinkSlots                                               = 1;
        nrofUplinkSymbols                                             = 4;


    For 2ms TDD sl_ahead = 4

    #tdd-UL-DL-ConfigurationCommon
    # subcarrierSpacing
    # 0=kHz15, 1=kHz30, 2=kHz60, 3=kHz120
        referenceSubcarrierSpacing                                    = 1;
        # pattern1
        # dl_UL_TransmissionPeriodicity
        # 0=ms0p5, 1=ms0p625, 2=ms1, 3=ms1p25, 4=ms2, 5=ms2p5, 6=ms5, 7=ms10
        dl_UL_TransmissionPeriodicity                                 = 4;
        nrofDownlinkSlots                                             = 2;
        nrofDownlinkSymbols                                           = 6;
        nrofUplinkSlots                                               = 1;
        nrofUplinkSymbols                                             = 4;

    Also make sure you have this in the MACRLC section of the configuration file:

    ulsch_max_frame_inactivity=0;

    which guarantees the the UL is scheduled in every TDD period with the minimal UL allocation (5 PRBs by default, mcs 9). You might want to increase this minimal allocation to something like :

    min_grant_prb = 20;
    min_grant_mcs = 16;

    also in the MACRLC section of the configuration file. Basically for lowest latency the UL needs to be scheduled in every TDD period, otherwise the scheduler will wait for SR or BSR to schedule the UL and this clearly will not work for low-latency services.

    We will make a dynamic version of this, but for the moment we need to use the parameters above to ensure that the scheduler gives resources all the time to UE for UL. Also, the "min_grant_prb" should be compatible with the packet size of the service you're trying to use (i.e. each application packet should fit in the constant allocation given in the TDD period). This all has to be done differently. We will make a proper URLLC scheduler soon.

    The other thing that is not there yet is to configure the URLLC CSI reporting (i.e. using the low spectral-efficient MCS table). This will report the mcs for 10^-5 transport block error rate. That's the "UR" in URLLC. So to get the equivalent you might want to limit the DL mcs with

    "dl_max_mcs=XX"

    and look at the error rate in the first round of HARQ transmission on DL (also on UL). You see this in logs that come out from the gNB. If you really want URLLC, you need 10^-5. We have made this work in one project, but the machines and RF need to be setup properly to ensure there are not lost fronthaul packets and no jitter in the operating system scheduling which will result in lost transmission. Without proper tuning you will have 10^-3 or 10^-4 independently of the SNR.

    Also, we needed to deploy the UPF in a real-time container. Normaly Linux will not provide the require packet jitter for URLLC and this is completely independent of the radio.

    Raymond

