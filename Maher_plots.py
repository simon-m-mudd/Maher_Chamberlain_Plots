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

# a class for holding some parameters. See Maher and Chamberlain 2014
# Supplementary materials
class MaherParams:
    m = 270
    m_units = 'g/mol'
    R_nmax = 1085
    R_nmax_units = 'micromol/L/yr SiO2'
    k_eff = 8.7e-6
    k_eff_units = 'mol/m^2/yr'
    phi = 0.175
    phi_units = 'dimensionless'
    C_eq = 380
    C_eq_units = 'micromol/L SiO2'
    
# This calculates the fraction of mass remaining as a function of weathering zone
# thickness (H, in metres), Erosion rate (E in m/yr) and specific surface area
# A in m^2/g
# This comes from equation (2) in the paper
def calculate_fw(H,E,A):
    T_s = H/E
    f_w = 1/(1+MaherParams.m*MaherParams.k_eff*A*T_s)
    return f_w

# This calculates the Dahmkoeler coefficient (units m/yr) 
# Comes from Maher and Chamberlain 2014 equation (1)
# Parameters are
# weathering zone thickness (H, in metres)
# Erosion rate (E in m/yr)
# specific surface area (A in m^2/g)
# Flow length (L in m)
def calculate_Dw(H,E,A,L):
    f_w = calculate_fw(H,E,A)
    Dw = L*MaherParams.phi*MaherParams.R_nmax*f_w/MaherParams.C_eq
    return Dw
 
# Thiscalculates concentration of SiO2 (in units micromols/L)
# as a function of
# Dw the Dahmkoeler coefficient in m/yr
# q the runoff in m/yr
# This comes from equation 3 in Maher and Chamberlain 2014
def calculate_C(Dw,q):
    C = MaherParams.C_eq*(np.e*np.e*Dw/q)/(1+np.e*np.e*Dw/q)
    return C

# this function calcualtes the flux of aqueous silicate, it multiplies eqution 3
# in Maher and Chamberlain with runoff and does a unit conversion to 
# get flux in tonnes per km^2 per year
# Dw the Dahmkoeler coefficient in m/yr
# q the runoff in m/yr     
def calcualte_Q(Dw,q):
    Q = 0.001*MaherParams.m*MaherParams.C_eq*(np.e*np.e*Dw/q)/(1+np.e*np.e*Dw/q)
    return Q
  
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
          fw[i][j]=calculate_fw(thisH,thisE,A)
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


  #pp.show() 



def MaherCPlots():

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
  C = np.zeros((nq,nDw))   

  i = 0
  for thisq in q:
      j = 0
      for thisDw in Dw:
          #print "H: " + str(thisH)+ " E: " + str(thisE)
          #print "i: "+str(i)+ " j: " +str(j)
          C[i][j]=calculate_C(thisDw,thisq)
          j = j+1
      i = i+1

  print C
  print C[:,0]
  print Dw[0]
  
  # now plot the results    
  fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
  ax1 = fig.add_subplot(1,1,1)  
  
  print "Shapes: "
  print C.shape[0]
  print q.shape[0]
  print C[:,0].shape[0]
  
  print "q: "
  print q
  print "C[:,0]: "
  print C[:,0]
  
  pp.plot(q,C[:,0],linewidth=3,label = ("Dw = "+str(Dw[0])))
  pp.plot(q,C[:,1],linewidth=3,label = ("Dw = "+str(Dw[1])))
  pp.plot(q,C[:,2],linewidth=3,label = ("Dw = "+str(Dw[2])))
  pp.plot(q,C[:,3],linewidth=3,label = ("Dw = "+str(Dw[3])))
  pp.plot(q,C[:,4],linewidth=3,label = ("Dw = "+str(Dw[4]))) 
  #pp.plot(H,fw[:,3],linewidth=3,label = ("E = "+str(E[3]*1000)+ "$mm/yr$"))
  pp.legend()

  pp.rcParams['xtick.direction'] = 'in'
  pp.rcParams['ytick.direction'] = 'in'
  ax1.set_xscale('log')
  #ax1.set_yscale('log')
  
  
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
  pp.ylabel('SiO2 (aq) (micromol/yr)',fontsize = axis_size) 
  #pp.title("$A$ is "+str(A)+ " $m^2/g$")
  #pp.ylim(0,1)


  figname = "Dw.svg"
  pp.savefig(figname, format='svg')      

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
  C = np.zeros((nq,nDw))   

  i = 0
  for thisq in q:
      j = 0
      for thisDw in Dw:
          #print "H: " + str(thisH)+ " E: " + str(thisE)
          #print "i: "+str(i)+ " j: " +str(j)
          C[i][j]=calculate_C(thisDw,thisq)
          j = j+1
      i = i+1

  print C
  print C[:,0]
  print Dw[0]
  
  # now plot the results    
  fig = pp.figure(1, facecolor='white',figsize=(10,7.5))
  ax1 = fig.add_subplot(1,1,1)  
  
  print "Shapes: "
  print C.shape[0]
  print q.shape[0]
  print C[:,0].shape[0]
  
  print "q: "
  print q
  print "C[:,0]: "
  print C[:,0]
  
  pp.plot(q,C[:,0],linewidth=3,label = ("Dw = "+str(Dw[0])))
  pp.plot(q,C[:,1],linewidth=3,label = ("Dw = "+str(Dw[1])))
  pp.plot(q,C[:,2],linewidth=3,label = ("Dw = "+str(Dw[2])))
  pp.plot(q,C[:,3],linewidth=3,label = ("Dw = "+str(Dw[3])))
  pp.plot(q,C[:,4],linewidth=3,label = ("Dw = "+str(Dw[4]))) 
  #pp.plot(H,fw[:,3],linewidth=3,label = ("E = "+str(E[3]*1000)+ "$mm/yr$"))
  pp.legend()

  pp.rcParams['xtick.direction'] = 'in'
  pp.rcParams['ytick.direction'] = 'in'
  ax1.set_xscale('log')
  #ax1.set_yscale('log')
  
  
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
  pp.ylabel('SiO2 (aq) (micromol/yr)',fontsize = axis_size) 
  #pp.title("$A$ is "+str(A)+ " $m^2/g$")
  #pp.ylim(0,1)


  figname = "Dw.svg"
  pp.savefig(figname, format='svg')   


def MaherPlots():
    #MaherFwPlots(0.1)
    MaherCPlots()

if __name__ == "__main__":
    MaherPlots() 