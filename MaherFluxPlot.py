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

# This plots concentrations and is used to reproduce figure 2b from the
# Maher and Chamberlain paper
def MaherFluxPlots():

  # These set the font size
  label_size = 20
  #title_size = 30
  axis_size = 28

  rcParams['font.size'] = label_size 
    
  #get the fw as a function of the erosion rate
  #log_Dw = np.linspace(-3,0,5)
  #Dw = np.power(10,log_Dw)  
  log_q = np.linspace(-2,1,51)
  q = np.power(10,log_q)
  Dw = np.zeros(5)
  Dw[0] = 0.003
  Dw[1] = 0.01
  Dw[2] = 0.03
  Dw[3] = 0.1
  Dw[4] = 0.3
  
  print Dw
  print q

  nDw = Dw.shape[0]
  nq = q.shape[0]
  #print "nH is: " + str(nH) + " and nE is: " + str(nE)
  Q = np.zeros((nq,nDw))   

  i = 0
  for thisq in q:
      j = 0
      for thisDw in Dw:
          #print "H: " + str(thisH)+ " E: " + str(thisE)
          #print "i: "+str(i)+ " j: " +str(j)
          Q[i][j]=MV.calculate_Q(thisDw,thisq)
          j = j+1
      i = i+1

  print Q
  print Q[:,0]
  print Dw[0]
  
  # now plot the results    
  fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
  ax1 = fig.add_subplot(1,1,1)  
  
  print "Shapes: "
  print Q.shape[0]
  print q.shape[0]
  print Q[:,0].shape[0]
  
  print "q: "
  print Q
  print "C[:,0]: "
  print Q[:,0]
  
  pp.plot(q,Q[:,0],linewidth=3,label = ("Dw = "+str(Dw[0])))
  pp.plot(q,Q[:,1],linewidth=3,label = ("Dw = "+str(Dw[1])))
  pp.plot(q,Q[:,2],linewidth=3,label = ("Dw = "+str(Dw[2])))
  pp.plot(q,Q[:,3],linewidth=3,label = ("Dw = "+str(Dw[3])))
  pp.plot(q,Q[:,4],linewidth=3,label = ("Dw = "+str(Dw[4]))) 
  #pp.plot(H,fw[:,3],linewidth=3,label = ("E = "+str(E[3]*1000)+ "$mm/yr$"))
  pp.legend()

  pp.rcParams['xtick.direction'] = 'in'
  pp.rcParams['ytick.direction'] = 'in'
  ax1.set_xscale('log')
  ax1.set_yscale('log')
  
  
  ax1.spines['top'].set_linewidth(2.5)
  ax1.spines['left'].set_linewidth(2.5)
  ax1.spines['right'].set_linewidth(2.5)
  ax1.spines['bottom'].set_linewidth(2.5) 
  ax1.tick_params(axis='both', width=2.5)    
  ax1.xaxis.set_major_formatter(FormatStrFormatter('%.03f'))

  for line in ax1.get_xticklines():
    line.set_marker(mpllines.TICKUP)

  for line in ax1.get_yticklines():
    line.set_marker(mpllines.TICKRIGHT)

  pp.xlabel('Flow rate ($m/yr$)',fontsize = axis_size)
  pp.ylabel('SiO2 (aq) flux ($tons/km^2/yr$)',fontsize = axis_size) 
  #pp.title("$A$ is "+str(A)+ " $m^2/g$")
  #pp.ylim(0,1)


  figname = "Flux_MCfig2b.svg"
  pp.savefig(figname, format='svg')   


def MaherPlots():
    MaherFluxPlots()

if __name__ == "__main__":
    MaherPlots() 