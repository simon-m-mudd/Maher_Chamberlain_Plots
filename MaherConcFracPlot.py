# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:10:10 2015

@author: smudd
"""

import matplotlib.pyplot as pp
import numpy as np
from matplotlib import rcParams
import matplotlib.lines as mpllines
from matplotlib.ticker import FormatStrFormatter
import MaherVariables as MV

# this function makes a series of plots of the concentration relative to the
# equilibrium concentration for a variety of weathering zone thicknesses and
# erosion rates
def ConcFracErosionHPlot(A,L,q):

  # These set the font size
  label_size = 20
  #title_size = 30
  axis_size = 28

  rcParams['font.size'] = label_size 
    
  #get the fw as a function of the erosion rate
  H = np.linspace(0.1,10,101)
  log_E = np.linspace(-5,-3,3)
  E = np.power(10,log_E)

  
  nH = H.shape[0]
  nE = E.shape[0]
  #print "nH is: " + str(nH) + " and nE is: " + str(nE)
  ConcRatio = np.zeros((nH,nE))


  i = 0
  for thisH in H:
      j = 0
      for thisE in E:
          #print "H: " + str(thisH)+ " E: " + str(thisE)
          #print "i: "+str(i)+ " j: " +str(j)
          ConcRatio[i][j]=MV.calculate_ConcRatio(thisH,thisE,A,L,q)
          j = j+1
      i = i+1    

    
  pp.clf
  pp.cla

  # now plot the results    
  fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
  ax1 = fig.add_subplot(1,1,1)  
  
  pp.plot(H,ConcRatio[:,0],linewidth=3,label = ("E = "+str(E[0]*1000)+"$mm/yr$"))
  pp.plot(H,ConcRatio[:,1],linewidth=3,label = ("E = "+str(E[1]*1000)+ "$mm/yr$"))
  pp.plot(H,ConcRatio[:,2],linewidth=3,label = ("E = "+str(E[2]*1000)+ "$mm/yr$"))
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
    line.set_marker(mpllines.TICKRIGHT)

  pp.xlabel('Weathering zone thickness ($m$)',fontsize = axis_size)
  pp.ylabel('Concentration ratio, dimensionless',fontsize = axis_size) 
  pp.title("$A$ is "+str(A)+" $m^2/g$, L is "+str(L)+"m and q is: "+str(q)+" m/yr" )
  pp.ylim(0,1)


  figname = "ConcRatio_for_A"+str(A)+"_q"+str(q)+"_L"+str(L)+".svg"
  pp.savefig(figname, format='svg') 


def MaherPlots():
    A = 0.1
    L = 50
    q = 5
    ConcFracErosionHPlot(A,L,q)

if __name__ == "__main__":
    MaherPlots() 