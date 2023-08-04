# -*- coding: utf-8 -*-
"""

@author: kishibutt

Zone 1 = WC1- volume 3m^3 
Zone 2 = Bedroom 3- volume 41m^3 
Zone 3 = Bedroom 4  -  Volume= 44m^3 
Zone 4 = bedroom 4  -  Volume=   82m^3
Zone 5 = WC2- volume 4m^3 
Zone 6 = bedroom 6  -  Volume= 75m^3   
Zone 7 = WC3- volume 3m^3 
Zone 8 = store- volume 14m^3 
Zone 9 = corridor  -  Volume= 128m^3 
Zone 10 = bathroom  -  Volume= 17m^3  
Zone 11 = store  -  Volume= 14m^3  
Zone 12 = WC4- volume 3m^3 
Zone 13 = stairs - Volume= 53m^3  
Zone 14 = bedroom 8  -  Volume= 72m^3 
Zone 15 = office  -  Volume= 29m^3  
Zone 16 = bedroom 7 Volume= 59m^3 
Zone 17 = stairs1 Volume= 19m^3 
 
total volume= 652

This code is designed to be imported into code which solves the governing equations.

This file is set up to deal with imported boundary flows from the results of a contam simulation.
This function is called the ventilation matrix function.

Created 03/03/2023 AJE 

"""
import numpy as np
import scipy as sp
from boundary_flow_Contam_12zone_AJE import boundary_flow_contam #imports boundary flow function which uses cintam results to define them 


##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################
##############################################################################
#number of zones n
n=17

##############################################################################
############################## geometry matrix SETUP #########################
##############################################################################
""" the aim of this nxn matrix, geometry(nxn), is to characterise the geometry
of the zonal set-up and so if zone i is connected to zone j then entry 
geometry[i,j]=1, if zone i is not connected to zone j then geometry[1,j]=0."""

#@CH-block...................................................
#defined in such away that input should be [i,j] where i<j
geometry=np.zeros((n,n))
geometry[5,8]=1
geometry[3,8]=1
geometry[2,8]=1
geometry[1,8]=1
geometry[7,8]=1
geometry[8,9]=1
geometry[8,15]=1
geometry[8,13]=1
geometry[8,12]=1
geometry[12,14]=1
geometry[8,16]=1
geometry[8,10]=1
geometry[0,1]=1
geometry[3,4]=1
geometry[11,15]=1
geometry[5,6]=1 #negative flow




for i in range(n):
    for j in range(n):    
        geometry[j,i] = geometry[i,j]

print("geometry matric geometry" +str(geometry))

##############################################################################
#Zonal volumes little v
v_zonal = np.zeros(n)
#for when volume is the same in each room
#for i in range(n):
#    v_zonal[i] = V

#kish
v_zonal[0]=3
v_zonal[1]=44
v_zonal[2]=44
v_zonal[3]=75
v_zonal[4]=4
v_zonal[5]=75
v_zonal[6]=3
v_zonal[7]=5
v_zonal[8]=128
v_zonal[9]=17
v_zonal[10]=12
v_zonal[11]=3
v_zonal[12]=53
v_zonal[13]=72
v_zonal[14]=27
v_zonal[15]=59
v_zonal[16]=19
#   .
#   .
#   .
#v_zonal[n]= 
print("volume v_zonal = " + str(v_zonal))
##########################################################################

#number of people in each zone is not the same due to scenario

K_zonal = np.zeros(n)
K_zonal[0]=0
K_zonal[1]=2
K_zonal[2]=1
K_zonal[3]=2
K_zonal[4]=0
K_zonal[5]=2
K_zonal[6]=0
K_zonal[7]=0
K_zonal[8]=0
K_zonal[9]=0
K_zonal[10]=0
K_zonal[11]=0
K_zonal[12]=0
K_zonal[13]=1
K_zonal[14]=0
K_zonal[15]=2
K_zonal[16]=0
##############################################################################
###########################################################################

#zonal ventialtion rate m^3/min
Q_zonal = np.zeros(n)

#NOTE: Q_zonal[i] here has been calculated as a proportion of the volume size
#in order to lead to specific ACH rates - the ones used in this study have been
#pre-calculated and including in  the commenting for each zone below.

#........................................................
Q_zonal[0]=0.16#0.15 #for 3ach= 4.91 #for1.5ach = 2.45 for 0.5ach = 0.81 #for 6ACH=9.82
Q_zonal[1]=0.47#2.2 #for 3ach=4.91 #for1.5ach = 2.45 for 0.5ach = 0.81 #for 6ACH=9.82
Q_zonal[2]=0.47#2.2 #for 3ach=1.42 #for1.5ach = 0.71 for 0.5ach = 0.23 #for 6ACH=2.84
Q_zonal[3]=0.47#3.75 #for 3ach=1.42 #for1.5ach = 0.71 for 0.5ach = 0.23 #for 6ACH=2.84
Q_zonal[4]=0.16#0.2 #for 3ach=1.81 #for1.5ach = 0.9 for 0.5ach = 0.3 #for 6ACH=3.62
Q_zonal[5]=0.47#3.75 #for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
Q_zonal[6]=1.5#0.15 #for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
Q_zonal[7]=0.46#0.7#for 3ach=1.59 #for1.5ach = 0.795 for 0.5ach =0.265  #for 6ACH=3.18
Q_zonal[8]=4.13#6.4 #for 3ach=2.36 #for1.5ach = 1.18 for 0.5ach = 0.4 #for 6ACH=4.72
Q_zonal[9]=0.48#0.85 #for 3ach=2.52 #for1.5ach = 1.26 for 0.5ach = 0.42 #for 6ACH=5.04
Q_zonal[10]=0.46#0.6 #for 3ach=2.17 #for1.5ach = 1.08 for 0.5ach = 0.36 #for 6ACH=4.34
Q_zonal[11]=1.5#0.15 #for 3ach=2.32 #for1.5ach = 1.16 for 0.5ach = 0.39 #for 6ACH=4.64
Q_zonal[12]=0.48#2.65 #for 3ach=2.52 #for1.5ach = 1.26 for 0.5ach = 0.42 #for 6ACH=5.04
Q_zonal[13]=0.48#3.6 #for 3ach=2.17 #for1.5ach = 1.08 for 0.5ach = 0.36 #for 6ACH=4.34
Q_zonal[14]=0.48#1.35 #for 3ach=2.32 #for1.5ach = 1.16 for 0.5ach = 0.39 #for 6ACH=4.64
Q_zonal[15]=0.48#2.95 #for 3ach=2.52 #for1.5ach = 1.26 for 0.5ach = 0.42 #for 6ACH=5.04
Q_zonal[16]=0.48#0.95 #for 3ach=2.17 #for1.5ach = 1.08 for 0.5ach = 0.36 #for 6ACH=4.34


#add more for more zones, currently for 3 zones
print("ventilation Q_zonal =" + str(Q_zonal))
###########################################################################
#The function below uses the above set-up, alongside imported boundary flow values
#to define and calculate the ventilation matrix, required to solve the governing equations
#The inverse ventilation matrix is also calculated below

def VentilationMatrix(n, t, Q_zonal, geometry, filepath):
    
    
    #define boundary flow matrix from boundary flow contam func (uses contam flows)
    boundary_flow = boundary_flow_contam(filepath, n, t, geometry)
    
    
    #VENTILATION MATRIX
    V_zonal = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i==j:
                V_zonal[i,i] = Q_zonal[i]
            
                for k in range(n):
                    if geometry[i,k] > 0:
                        
                        V_zonal[i,i] = V_zonal[i,i] + boundary_flow[i,k]
                    else:
                        V_zonal[i,i] = V_zonal[i,i]
                    
                    
            else:
                if geometry[i,j]>0:
                        
                    V_zonal[i,j] = - boundary_flow[j,i]
                else:
                    V_zonal[i,j] = 0
                
    print("Ventilation Matrix V = " + str(V_zonal))   
    
    
    return V_zonal

def InvVentilationMatrix(V_zonal):
        
    #calculate the inverse of the ventilation matrix for steady-state calculation
    V_zonal_inv = sp.linalg.inv(V_zonal)
    print("Inverse Ventilation Matrix V = " + str(V_zonal_inv))
    
    return V_zonal_inv
###########################################################################
