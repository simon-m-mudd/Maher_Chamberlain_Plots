# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 14:02:47 2015

@author: smudd
"""

import numpy as np


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
def calculate_Q(Dw,q):
    molar_SiO2 = 2*15.9994+28.0855
    Q = q*0.001*molar_SiO2*MaherParams.C_eq*(np.e*np.e*Dw/q)/(1+np.e*np.e*Dw/q)
    return Q

# this calcuates the concentration relative to equilibrium concentration
# as a function of H, E and A
def calculate_ConcRatio(H,E,A,L,q):
    Dw = calculate_Dw(H,E,A,L)
    C = calculate_C(Dw,q)
    Cfrac = C/MaherParams.C_eq
    return Cfrac
    