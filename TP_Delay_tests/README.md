[TOC]
- PLOT means plotting codes are active, stated in case if they cause some delay
- SCHED means non-standart Scheduling Request code (it always sends SR request)
- TDD means lowest (for me) possible TDD config
## ul_max_mcs = 9
### W11 || X410GNB || 51PRB || (PLOT+, SCHED+, TDD+) || VM CN Free5GC|| B210 UE
    UL PING 4.930/5.817/7.045
    DL PING 5.026/6.162/7.198
    IPERF3 UL 8.21mbps
    IPERF3 DL 2.54mbps (MCS 6)
### W11 || X410GNB || 51PRB || (PLOT+, SCHED+, TDD+) || REAL CN Free5GC|| B210 UE
    UL PING WITH REAL CN WITH B200 5.337/5.847/6.471
    DL PING WITH REAL CN WITH B200 4.843/6.139/7.189
    IPERF3 UL 51PRB 8.13mbps
    IPERF3 DL 51PRB 4.37 (MCS 9)
- **Having CN installed on VM has no effect on delay, so continue with REAL CN** 
- **if the type of CN isn’t specified, then it is REAL CN**
- **Also we tried with OAI CN, it didn’t contributed to the delay, ALBA's setup**
### W11 || X410GNB || 51PRB || (PLOT-, SCHED+, TDD+) ||  Free5GC||  B210 UE
    UL PING 5.218/5.865/6.552
    DL PING 5.087/6.329/7.145
    IPERF3 UL 51PRB 8.17mbps
    IPERF3 DL 51PRB 4.02mbps
### W11 || X410GNB || 51PRB || (PLOT-, SCHED+, TDD+) ||  Free5GC|| QUECTEL UE
    UL PING  Minimum = 9ms, Maximum = 18ms, Average = 11ms (UL BLER of 0.25, MCS6)
    DL PING  Minimum = 9.587ms    , Maximum =19.014ms     , Average = 12.630ms
### W15 || X410GNB || 51PRB || (PLOT-, SCHED-, TDD+) ||Free5GC||  B210 UE || CONTINUOUS TX
    UL PING  4.937/5.490/6.441/0.495 ms
    DL PING  5.286/6.272/7.061/0.572 ms
    IPERF3 UL 51PRB 8.19mbps
    IPERF3 DL 51PRB 4.12mbps
- **Before we weren’t adding the —continous-tx option to the gNB in command line while starting it since it were causing a lot of LLLLL to appear in the log of gNB and eventually causing it to be terminated. But with a new update coming with the w15, it has been solved. From now on, even if it is not stated in the log, —continous-tx is always used.** 

### W15 || X410GNB || 51PRB || (PLOT-, SCHED+, TDD+) || Free5GC||  B210 UE || CONTINUOUS TX
    UL PING 4.922/5.399/6.436/0.499 ms
    DL PING 5.522/6.186/7.125/0.472 ms
    IPERF3 UL 8.18mbps
    IPERF3 DL 4.07mbps
## ul_max_mcs = 28
### W15 || X410GNB || 51PRB || (PLOT+, SCHED+, TDD+) ||Free5GC||  B210 UE || CONTINUOUS TX
    IPERF3 UL 33mbps 
    IPERF3 DL 4.74mbps (MCS 9)
    DL PING 4.766/6.055/6.936/0.551 ms
    UL PING 4.909/5.372/6.402/0.488 ms
    IPERF3 DL 9.30mbps (MCS 16)
### W15 || RFSIM || X410GNB ||51PRB||(PLOT+, SCHED+, TDD+)||Free5GC||B210 UE || CONTINUOUS TX
    BOTH IPERF WITH UDP
    IPERF3 UL 21.2mbps 
    IPERF3 DL 31mbps 
    DL PING 4.766/6.055/6.936/0.551 ms
    UL PING 5.362/6.213/7.804/0.645 ms