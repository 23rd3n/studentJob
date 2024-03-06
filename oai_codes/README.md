[TOC]

- **In the added code parts you can search the "SERDEN ADDED" keyword to see exact location**
- **sayac (counter in Turkish) is a variable to control the speed of plotting**
- **When iperf is utilized the function will be called more, and thus sayac increases faster**
- **Therefore, sayac=50 will plot very slow if there is no packet request, and will be faster if there is packets**
- **It is chosen heurastically but 50 is a good point for 20Mhz DL plotting and 200 is good point for UL plotting**

- **NOTE(1)** : When using the estimations from .txt file, its path should be modified in the source function
- **NOTE(2)** : When reading PDSCH estimations from .txt file, it only changes with the real one, when the channel is fully utilized(iperf) but there is also the part where no change of PDSCH estimations and full plotting (even in no full BW utilization)
- **NOTE(3)** : Please use 4 decimal points after the comma like 0.abcd, because all the code is written for 4 point precision.
- **NOTE(4)** : The variable fixed2real is chosen such that channel magnitude lies in the interval [0,1]. 
  - It is not completely random, the value is chosen as 512 in UL, because both it makes the normalization correct and it is suggested by OAI developers
  - The value is chosen as 8192 in DL to make normalization consistent with the UL plotting. This value itself is not confirmed and may be subject to changes.
- **NOTE(5)** : Basically two main difference between UL plotting and DL plotting are fixed2real values (UL 512, DL 8192) and the definition of the array of estimates.


## OAI DL Plotting (at UE)
- **For further reference, the modified nr_dl_channel_estimation.c file is uploaded**
### **at the beginning of the openair1/PHY/NR_UE_ESTIMATION/nr_dl_channel_estimation.c, add the followings:**
```C
// ## SERDEN ADDED
int sayac = 0;
FILE *gnuplot = NULL;
int node_index;
int node_prev = -1;
double float_numbers[612];
// ## SERDEN ADDED
```
### **at the end of the rx antenna for loop of the function nr_pdsch_channel_estimation(line number 1705 for tag w15.2023)**
```C
    // ## SERDEN ADDED
    dl_ch = (c16_t *)&dl_ch_estimates[p * ue->frame_parms.nb_antennas_rx + aarx][ch_offset];
    if(sayac == INT_MAX) sayac = 1;
    sayac++;
    const int fixed2real = 8192; //refer to NOTE(1)
    double sqrt_mag;
    if (sayac % 50 == 0 ){

      if (gnuplot == NULL) gnuplot = popen("gnuplot", "w");
      else {
        fprintf(gnuplot, "set style data lines\n");
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pdsch*12);
        fprintf(gnuplot, "set yrange [0:1]\n");
        fprintf(gnuplot, "set title '{/:Bold GNB(dlEst) RSSI %d dB (%d dBm/RE) WBandCQI %d dB NODE %d} sayac= %d' \n",
                          ue->measurements.rx_power_avg_dB[0],
                          ue->measurements.rx_rssi_dBm[0],
                          ue->measurements.wideband_cqi_avg[0],
                          node_prev,
                          sayac);
      } 

      if (nb_rb_pdsch == 51){
        FILE *fp = fopen("./bothCamEst.txt", "r");
        if(fscanf(fp, "%d", &node_index));
        if (node_prev != node_index){
          node_prev = node_index;
          fprintf(gnuplot, "plot '-' with lines title 'MLest', '-' with lines title 'OAIest'\n");
          for (int i = 0; i < nb_rb_pdsch*12; i++) {
            if(fscanf(fp, "%lf", &float_numbers[i]));
            fprintf(gnuplot, "%.4f\n",float_numbers[i]);
          }
          fprintf(gnuplot,"e\n");
          for (uint16_t re = 0; re< nb_rb_pdsch*12; re++){
            sqrt_mag = sqrt(dl_ch[re].r*dl_ch[re].r + dl_ch[re].i*dl_ch[re].i)/fixed2real;
            fprintf(gnuplot, "%.4f\n",sqrt_mag);
          }
          fprintf(gnuplot,"e\n");
        }
        fclose(fp);
      }else{
        fprintf(gnuplot, "plot '-' with lines title 'OAIest' \n");
        for (uint16_t re = 0; re< nb_rb_pdsch*12; re++){
          sqrt_mag = sqrt(dl_ch[re].r*dl_ch[re].r + dl_ch[re].i*dl_ch[re].i)/fixed2real;
          fprintf(gnuplot, "%.4f\n",sqrt_mag);
        }
        fprintf(gnuplot,"e\n");
      }
      
      fflush(gnuplot);  
    }
    // ## SERDEN ADDED
```

### **if you don't want to read from a txt file but only plot the OAI estimates then use:**

```C
//to the beginning of the file 
// ## SERDEN ADDED
int sayac = 0;
FILE *gnuplot = NULL;
// ## SERDEN ADDED
//to the beginning of the file 

//at the end of int nr_pdsch_channel_estimation() function ##
// ## SERDEN ADDED
dl_ch = (c16_t *)&dl_ch_estimates[p * ue->frame_parms.nb_antennas_rx + aarx][ch_offset];
sayac++;
double sqrt_mag;
if (sayac % 50 == 0 ){

    if (gnuplot == NULL) gnuplot = popen("gnuplot", "w");
    else {
        fprintf(gnuplot, "set style data lines\n");
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pdsch*12);
        fprintf(gnuplot, "set title 'sayac = %d and size = %d' \n",sayac,nb_rb_pdsch*12);
        //fprintf(gnuplot, "set yrange [0:1.5]\n");
    };
    fprintf(gnuplot, "plot '-' with lines\n");
    for (uint16_t re = 0; re< nb_rb_pdsch*12; re++){
        sqrt_mag = sqrt(dl_ch[re].r*dl_ch[re].r + dl_ch[re].i*dl_ch[re].i)/8192; //refer to NOTE(1)
        fprintf(gnuplot, "%.3f\n",sqrt_mag);
    }
    fprintf(gnuplot,"e\n");

    fflush(gnuplot);  
}
// ## SERDEN ADDED
//at the end of int nr_pdsch_channel_estimation() function 
```
## OAI DL Plotting OaiEst and MLest at same graph with replacement
### **at the beginning of the openair1/PHY/NR_UE_ESTIMATION/nr_dl_channel_estimation.c, add the followings:**
```C
// ## SERDEN ADDED
int sayac = 0;
FILE *gnuplot = NULL;
int node_index;
int node_prev = -1;
double float_numbers[612];
// ## SERDEN ADDED
```
### **at the end of the rx antenna for loop of the function nr_pdsch_channel_estimation(line number 1705 for tag w15.2023)**
```C
    // ## SERDEN ADDED
    dl_ch = (c16_t *)&dl_ch_estimates[p * ue->frame_parms.nb_antennas_rx + aarx][ch_offset];
    if(sayac == INT_MAX) sayac = 1; // to avoid overflow
    sayac++;
    const int fixed2real = 8192; //refer to NOTE(1)
    double sqrt_mag; //holder variable for magnitude of the channel
    if (sayac % 50 == 0 ){ //to limit the speed of plotting

      if (gnuplot == NULL) gnuplot = popen("gnuplot", "w"); //if not open, then open gnuplot
      else {
        fprintf(gnuplot, "set style data lines\n"); //line plot
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pdsch*12); 
        fprintf(gnuplot, "set yrange [0:1]\n");
        //plot the SISO measurements obtained from ue->measurements struct
        fprintf(gnuplot, "set title '{/:Bold GNB(dlEst) RSSI %d dB (%d dBm/RE) WBandCQI %d dB NODE %d} sayac= %d' \n",
                          ue->measurements.rx_power_avg_dB[0],
                          ue->measurements.rx_rssi_dBm[0],
                          ue->measurements.wideband_cqi_avg[0],
                          node_prev,
                          sayac);
      } 
      //if full BW, then read from txt and replace with real channel
      if (nb_rb_pdsch == 51){
        //just read the estimates written by ML model
        FILE *fp = fopen("./bothCamEst.txt", "r"); //open txt
        if(fscanf(fp, "%d", &node_index)); //get node id
        if (node_prev != node_index){ // if not the same channel, read it
          node_prev = node_index; //update the read node
          //create two line plots with names
          fprintf(gnuplot, "plot '-' with lines title 'MLest', '-' with lines title 'OAIest'\n");
          for (int i = 0; i < nb_rb_pdsch*12; i++) {
            if(fscanf(fp, "%lf", &float_numbers[i])); //read from fp to array
            int re = dl_ch[i].r; //hold the current channel
            int im = dl_ch[i].i; //hold the current channel
            dl_ch[i].r = (int)(float_numbers[i]*fixed2real*cos(atan2(im,re))); //replace estimates
            dl_ch[i].i = (int)(float_numbers[i]*fixed2real*sin(atan2(im,re))); //replace estimates
            fprintf(gnuplot, "%.4f\n",float_numbers[i]); //plot txt file
          }
          fprintf(gnuplot,"e\n"); //finish read estimates' plot
          for (uint16_t re = 0; re< nb_rb_pdsch*12; re++){
            sqrt_mag = sqrt(re*re + im*im)/fixed2real;
            fprintf(gnuplot, "%.4f\n",sqrt_mag); //plot the OAI channel
          }
          fprintf(gnuplot,"e\n");
        }
        fclose(fp);
      }else{ //if no full bandwidth, then just plot OAI estimates
        fprintf(gnuplot, "plot '-' with lines title 'OAIest' \n");
        for (uint16_t re = 0; re< nb_rb_pdsch*12; re++){
          sqrt_mag = sqrt(dl_ch[re].r*dl_ch[re].r + dl_ch[re].i*dl_ch[re].i)/fixed2real;
          fprintf(gnuplot, "%.4f\n",sqrt_mag);
        }
        fprintf(gnuplot,"e\n");
      }
      
      fflush(gnuplot);  
    }
    // ## SERDEN ADDED
```

## OAI UL Plotting (at gNB)
- **For further reference, the modified nr_ul_channel_estimation.c file is uploaded**
### **at the beginning of the openair1/PHY/NR_ESTIMATION/nr_ul_channel_estimation.c, add the followings:**
```C
// ## SERDEN ADDED
int sayac = 0;
FILE *gnuplot = NULL;
int node_index;
int node_prev = -1;
double float_numbers[612];
// ## SERDEN ADDED
```

### **at the end of the rx antenna for loop of the function nr_pusch_channel_estimation(line number 509 for tag w23.2023)**
```C
    // ## SERDEN ADDED
    ul_ch = &ul_ch_estimates[p * gNB->frame_parms.nb_antennas_rx + aarx][ch_offset];
    if(sayac == INT_MAX) sayac = 1;
    sayac++;
    const int fixed2real = 512; //refer to NOTE(1)
    double sqrt_mag;
    if (sayac % 200 == 0 ){

      if (gnuplot == NULL) gnuplot = popen("gnuplot", "w");
      else {
        fprintf(gnuplot, "set style data lines\n");
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pdsch*12);
        fprintf(gnuplot, "set yrange [0:1]\n");
        fprintf(gnuplot, "set title '{/:Bold (ulEst) NODE %d} sayac= %d' \n",
                          node_prev,
                          sayac);
      } 

      if (nb_rb_pusch == 51){
        FILE *fp = fopen("./PDSCH.txt", "r");
        if(fscanf(fp, "%d", &node_index));
        if (node_prev != node_index){
          node_prev = node_index;
          fprintf(gnuplot, "plot '-' with lines title 'MLest', '-' with lines title 'OAIest'\n");
          for (int i = 0; i < nb_rb_pusch*12; i++) {
            if(fscanf(fp, "%lf", &float_numbers[i]));
            fprintf(gnuplot, "%.4f\n",float_numbers[i]);
          }
          fprintf(gnuplot,"e\n");
          for (uint16_t re = 0; re< nb_rb_pusch*12; re++){
            sqrt_mag = sqrt(ul_ch[re].r*ul_ch[re].r + ul_ch[re].i*ul_ch[re].i)/fixed2real;
            fprintf(gnuplot, "%.4f\n",sqrt_mag);
          }
          fprintf(gnuplot,"e\n");
        }
        fclose(fp);
      }else{
        fprintf(gnuplot, "plot '-' with lines title 'OAIest' \n");
        for (uint16_t re = 0; re< nb_rb_pusch*12; re++){
          sqrt_mag = sqrt(ul_ch[re].r*ul_ch[re].r + ul_ch[re].i*ul_ch[re].i)/fixed2real;
          fprintf(gnuplot, "%.4f\n",sqrt_mag);
        }
        fprintf(gnuplot,"e\n");
      }
      
      fflush(gnuplot);  
    }
    // ## SERDEN ADDED
```

### **if you don't want to read from a txt file but only plot the OAI estimates then use:**

```C
//to the beginning of the file
// ## SERDEN ADDED 
int sayac = 0;
FILE *gnuplot = NULL;
// ## SERDEN ADDED
//to the beginning of the file 

//at the end of the rx antenna for loop of the function  nr_pusch_channel_estimation() function ##
// ## SERDEN ADDED
ul_ch = &ul_ch_estimates[p * gNB->frame_parms.nb_antennas_rx + aarx][ch_offset];
sayac++;
double sqrt_mag;
if (sayac % 200 == 0 ){

    if (gnuplot == NULL) gnuplot = popen("gnuplot", "w");
    else {
        fprintf(gnuplot, "set style data lines\n");
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pusch*12);
        fprintf(gnuplot, "set title 'sayac = %d and size = %d' \n",sayac,nb_rb_pusch*12);
        //fprintf(gnuplot, "set yrange [0:1.5]\n");
    };
    fprintf(gnuplot, "plot '-' with lines\n");
    for (uint16_t re = 0; re< nb_rb_pusch*12; re++){
        sqrt_mag = sqrt(ul_ch[re].r*ul_ch[re].r + ul_ch[re].i*ul_ch[re].i)/512; //refer to NOTE(1)
        fprintf(gnuplot, "%.3f\n",sqrt_mag);
    }
    fprintf(gnuplot,"e\n");

    fflush(gnuplot);  
}
// ## SERDEN ADDED
//at the end of the rx antenna for loop of the function nr_pusch_channel_estimation() function 
```

## OAI Changing PDSCH Values (at gNB)
- **For further reference, the modified nr_dlsch.c file is uploaded**
- **These are both inside nr_generate_pdsch function**
### **This part should be added right before `for (int ap=0; ap<frame_parms->nb_antennas_tx; ap++) {` loop**
```C
// ## SERDEN ADDED
    double *newPDSCH = (double*)malloc(612*12*sizeof(double));
    int OKU;
    if (rel15->rbSize*12 == 612){
      FILE* fd = fopen("/home/serkut/Desktop/serden/PDSCH.txt","r");
      if(fscanf(fd,"%d",&OKU));
      if (OKU) printf("PDSCH is being generated. WAIT... \n");
      else{
        printf("PDSCH is being read. WAIT... \n");
        for (int i = 0; i < 612; i++) {
          if(fscanf(fd, "%lf", newPDSCH+i));
        }
      }
      fclose(fd);
    }
// ## SERDEN ADDED
```

### **This part should be added at the end of the unitary precoding if, namely at the end of `if (pmi == 0) {//unitary Precoding`**
```C
//## SERDEN ADDED
            c16_t* pdsch_val = (c16_t*)malloc(NR_NB_SC_PER_RB*sizeof(c16_t));
            pdsch_val = &txdataF[ap][l*frame_parms->ofdm_symbol_size + txdataF_offset + k]; 

            if ((rel15->rbSize)*12 == 612 ){
              for (int rE = 0; rE < 12; rE++){
                pdsch_val[rE].r = pdsch_val[rE].r*newPDSCH[rb*12+rE];
                pdsch_val[rE].i = pdsch_val[rE].i*newPDSCH[rb*12+rE];
              }
            }
// ## SERDEN ADDED
```

### **FOR FAST BUILD**
- if you build the gNB and UE with `--ninja` option `./build_oai --gNB -w USRP --ninja -c` then after the
modifications of the code, the changed part can be effectively build with:
`cd cmake_targets/ran_build/build`
`ninja nr-softmodem nr-uesoftmodem params_libconfig coding telnetsrv rfsimulator ldpc`