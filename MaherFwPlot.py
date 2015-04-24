# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 13:28:11 2015

@author: smudd
"""

import matplotlib.pyplot as pp
import numpy as np
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib import rcParams
import matplotlib.lines as mpllines
from matplotlib.ticker import FormatStrFormatter
import MaherVariables as MV

 
# This plots the farction of weatherable minerals remianing as a function
# of the specific surface area, and over a range of H and E values 
def MaherFwPlots(A):
  
  # These set the font size
  label_size = 20
  #title_size = 30
  axis_size = 28

  rcParams['font.size'] = label_size 
  # set some variables for the fonts
  #rcParams['font.family'] = 'sans-serif'
  #rcParams['font.sans-serif'] = ['arial']
  
  #get the fw as a function of the erosion rate
  H = np.linspace(0.1,10,101)
  log_E = np.linspace(-5,-3,3)
  E = np.power(10,log_E)
  #print "Log e is: "
  #print log_E  
  #print "E is: "
  #print E
  #print "H is: "
  #print H
  
  nH = H.shape[0]
  nE = E.shape[0]
  #print "nH is: " + str(nH) + " and nE is: " + str(nE)
  fw = np.zeros((nH,nE))


  i = 0
  for thisH in H:
      j = 0
      for thisE in E:
          #print "H: " + str(thisH)+ " E: " + str(thisE)
          #print "i: "+str(i)+ " j: " +str(j)
          fw[i][j]=MV.calculate_fw(thisH,thisE,A)
          j = j+1
      i = i+1

  #print fw
    
  pp.clf
  pp.cla

  # now plot the results    
  fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
  ax1 = fig.add_subplot(1,1,1)  
  
  pp.plot(H,fw[:,0],linewidth=3,label = ("E = "+str(E[0]*1000)+"$mm/yr$"))
  pp.plot(H,fw[:,1],linewidth=3,label = ("E = "+str(E[1]*1000)+ "$mm/yr$"))
  pp.plot(H,fw[:,2],linewidth=3,label = ("E = "+str(E[2]*1000)+ "$mm/yr$"))
  #pp.plot(H,fw[:,3],linewidth=3,label = ("E = "+str(E[3]*1000)+ "$mm/yr$"))
  pp.legend()

  pp.rcParams['xtick.direction'] = 'out'
  pp.rcParams['ytick.direction'] = 'out'
  ax1.set_xscale('log')
  #ax1.set_yscale('log')
  
  
  ax1.spines['top'].set_linewidth(2.5)
  ax1.spines['left'].set_linewidth(2.5)
  ax1.spines['right'].set_linewidth(2.5)
  ax1.spines['bottom'].set_linewidth(2.5) 
  ax1.tick_params(axis='both', width=2.5)    
  ax1.xaxis.set_major_formatter(FormatStrFormatter('%.01f'))

  for line in ax1.get_xticklines():
    line.set_marker(mpllines.TICKDOWN)

  for line in ax1.get_yticklines():
    line.set_marker(mpllines.TICKLEFT)

  pp.xlabel('Weathering zone thickness ($m$)',fontsize = axis_size)
  pp.ylabel('$f_w$, dimensionless',fontsize = axis_size) 
  pp.title("$A$ is "+str(A)+ " $m^2/g$")
  pp.ylim(0,1)


  figname = "fw_for_A"+str(A)+".svg"
  pp.savefig(figname, format='svg') 


def MaherPlots():
    MaherFwPlots(0.1)


if __name__ == "__main__":
    MaherPlots() 