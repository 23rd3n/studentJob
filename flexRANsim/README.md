[TOC]
- Running and installation of OAIsim is well explained inside the README.md file of oaisim itself. These are the modifications that I've attempted.
## PLOTTING OF DL
- Here, inside the /openair1/PHY/LTE_ESTIMATION/lte_dl_channel_estimation.c/lte_dl_channel_estimation,the plotting for DL channel estimates are given.
- This is just an attempted code, the correctness of the code couldn't be tested. I was not sure if FlexRANsim runs local PHY layer functionalities. Appearently, it seems it doesn't.
- However, inside the function there are compiler directed if statements like:
```C
#if (PLOT == 1)
  int sayac = 0;
  FILE *gnuplot = NULL;
#endif
```
- These parts are the codes that I've added, if it isn't wanted to run the changes that are made by me, just change the line `#define PLOT 1` to `#define PLOT 0`, basically make PLOT false.
- This code attemps to plot DL channel estimates created by OAI, for exact location, the file is uploaded to gitlab.
```C
    #if (PLOT == 1)
      //*********************************MY_PART FOR PLOTTING INSIDE ANTENNA LOOP*****************************************//
      dl_ch = (int16_t *)&dl_ch_estimates[(p<<1)+aarx][ch_offset];
      if(sayac == INT_MAX) sayac = 1;
      sayac++;
      const int fixed2real = 8192;
      double sqrt_mag;
      int nb_rb_pdsch = ue->frame_parms.N_RB_DL;

      printf("Plotting \n");
      if (gnuplot == NULL) gnuplot = popen("gnuplot", "w");
      else {
        fprintf(gnuplot, "set style data lines\n");
        fprintf(gnuplot, "set xrange [0:%d]\n",nb_rb_pdsch*12);
        fprintf(gnuplot, "set yrange [0:1]\n");
      } 


      fprintf(gnuplot, "plot '-' with lines title 'OAIest' \n");
      for (uint16_t re = 0; re< nb_rb_pdsch*12*2; re+=2){
        sqrt_mag = sqrt(dl_ch[re]*dl_ch[re] + dl_ch[re+1]*dl_ch[re+1])/fixed2real;
        fprintf(gnuplot, "%.4f\n",sqrt_mag);
      }
      fprintf(gnuplot,"e\n");


      fflush(gnuplot); 
      //*********************************MY_PART FOR PLOTTING INSIDE ANTENNA LOOP*****************************************// 
  #endif
```
- In the case of succesfully plotting, the plotting for 5G case may well be adapted here because for plotting it is pretty the same with 5G codes.
- Just make sure that gnuplot is installed in the host as explained [here](../README.md)

## Change of PDSCH values
- Here, the same approach is exactly followed with the name of `#define PDSCH_OKU 1`
- Since the code is quite case-specific defined, I attempt to change the table of modulation symbols so that the final sent symbol is in the shape that we want.
- Since the code parts are distributed over the whole file, you can find all the modifications by searching the PDSCH_OKU directive.
