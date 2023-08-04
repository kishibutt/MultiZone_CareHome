# -*- coding: utf-8 -*-
"""
@author: scaje
@Adaptive Code by Kishwer
 This code aims to solve for concentration of pathogens in the air and 
the SE epidemic model for a care home floor 1 (layout defined in geometry matrix)
#.............................................. Care Home by kishwer
This code solves the setup for a 17 zone care home setting with zones defined as
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
 
Each room has at least one resident and a couple of rooms are shared between 2 residents. All rooms are attached to a corridor with a single door.
 One support worker takes care of each resident at different times of the day. 
 

User must define infected individuals and corresponding zone, and any time
periods or zones which the infectors move to, below.

Created 03/03/2023 Kishwer
"""


import matplotlib.pyplot as plt
import random, math
import numpy as np
np.float = float    
from scipy.integrate import odeint #for solving odes
import matplotlib.colors as mcolors #colour name package
from matplotlib.pyplot import cm #colour map package
from pywaffle import Waffle #visual package for visualising icons
import time #for live run time of code
import Contam_flows_12zone_AJE as VentMatrix #imports setup for 6 zone ward ventilation setting from another file where it is already defined
from Contam_flows_12zone_AJE import VentilationMatrix #import function which defines ventilation matrix
from Contam_flows_12zone_AJE import InvVentilationMatrix #imports function which defines inverse ventilation matrix
from SE_Conc_Eqn_AJE import odes #imports predefined SE ode functions for a transient concentration
from SE_Conc_Eqn_AJE import steadyodes ##imports predefined SE ode functions for a steady concentration
from output_AJE import output_SE_Ct #This imports the plotting ode for all possible outputs for the multizonal transient concentration SE model
from boundary_flow_Contam_12zone_AJE import boundary_flow_contam #this import is the function which changes the boundary flow values based on output from contam simulation


start_time = time.time() #time code started running
############################################################################
#Initial values from other simulations for reference
########################################################
###########################Initial values###################################


## DEFINE FILEPATH FOR EXPORTED CONTAM AIRFLOW SIMULATION RESULTS

filepath = r"fullfilepath..\Contam_export_scripts_AJE\results3.csv"

#outbreak parameters
#quanta rate = quanta/min . person (as 0.5 quanta per min)
q=0.5
#pulmonary rate = volume/min ( as 0.01volume/min)
p=0.01

##############################################################################
##############################################################################
############################## ZONAL SETUP ###################################
##############################################################################

######################Run ventilation setting############################ 
n=17
VentMatrix

###############################################################

#Pulmonary rate in each zone
p_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    p_zonal[i] = p

print("Pulmonary rate p_zonal = " + str(p_zonal))
############################################################################

#Zonal quanta
q_zonal = np.zeros(n)
#for when  is the same in each room
for i in range(n):
    q_zonal[i] = q
#If volumes are different
#q_zonal[0]=
#q_zonal[1]=
#q_zonal[2]=
#   .
#   .
#   .
#q_zonal[n]=
print("quanta q_zonal = " + str(q_zonal))
############################################################################
#Zonal infections
#Zonal volumes little v
I_zonal = np.zeros(n)
# for when is the same in each room
# for i in range(n):
#     I_zonal[i] = I0
# If volumes are different
#   .
I_zonal[1]=1 #bedroom3, zone 2
I_zonal[2]=0    #bedroom 4, zone3
I_zonal[5]=0    #bedroom6, zone 6
I_zonal[13]=0    #bedroom8, zone 14
I_zonal[15]=0   #bedroom7, zone16
#I_zonal[14]=0   #office, zone15
#
#
#
#I_zonal[n]= 
print("infections I_zonal = " + str(I_zonal))
##########################################################################

#############################################################################
#############################################################################
######################### DEFINE  Transient ODES #############################
#############################################################################


#################################################################
# declare the time vector in which to solve ODEs
#A grid of time points (in minutes)
#14400 time steps used, this is split up proportional to the length of each time period
#defined below - This is amount of seconds in a 4hr = 4x60x60 simulation
###########################################################################
################ transient infector #############################
##############################################################################
# #Thinking about a transient infector i.e only present for a certain amount of time

#NOTE: - time stepping for each second in a 4 hour simulation 
#that is 4 x 60 x 60 = 14,400 time steps, or 3600 time steps per hour
#..........................................................................@kishi
#t1 = np.linspace(0,30,1800) says time 1= np.linespace(startingTime,Duration,?)
#time periods of scenario
t1 = np.linspace(0,60,3600) # for infector present in bedroom3 - Zone 2---------------row 18 is for 8am, how can I change for a hour?

t2 = np.linspace(60,120,3600) # infector starts round in bedroom4 - zone 3------------20 is for 9am

t3 = np.linspace(120,180,3600) # infector continues round in bedroom5 - zone 4

t4 = np.linspace(180,240,3600) # infector continues round in bedroom6- zone 6

t5 = np.linspace(240,300,3600) # infector continues drug round bedroom7 - zone 16

t6 = np.linspace(300,360,3600) # for infector present in bedroom3 - Zone 2

t7 = np.linspace(360,420,3600) # infector starts bedroom6- zone 6

t8 = np.linspace(420,480,3600) # infector continues round bedroom8- zone 14

t9 = np.linspace(480,540,3600) # infector continues round in bedroom7- zone 16

t10 = np.linspace(540,600,3600) # infector come back to bedroom3 - zone 2

#NOTE: - time stepping for each second in a 4 hour simulation 
#that is 4 x 60 x 60 = 14,400 time steps, or 3600 time steps per hour

#...............................................................@kishi
#infection vectors to correspon with scenario
I_zonal_t1 = I_zonal # for infector present in bedroom3 - Zone 2

I_zonal_t2 = np.zeros(n)
I_zonal_t2[2] = 1    # infector starts bedroom4- zone 3

I_zonal_t3 = np.zeros(n)
I_zonal_t3[5] = 1    # bedroom5- zone 6

I_zonal_t4 = np.zeros(n)
I_zonal_t4[13] = 1    # continue visiting room6 - zone 14

I_zonal_t5 = np.zeros(n)
I_zonal_t5[15] = 1    #  bedroom 7- zone 16

I_zonal_t6 = np.zeros(n)
I_zonal_t6[1] = 1   # infector returns to bedroom4 - zone 2

I_zonal_t7 = np.zeros(n)
I_zonal_t7[2] = 1    # infector starts drug round bedroom4- zone 3

I_zonal_t8 = np.zeros(n)
I_zonal_t8[5] = 1    # carries out drug round bedroom5- zone 6

I_zonal_t9 = np.zeros(n)
I_zonal_t9[13] = 1    # carries out drug round bedroom8 - zone 14

I_zonal_t10 = np.zeros(n)
I_zonal_t10[15] = 1    #  bedroom7- zone 16

#combining for solution loop

t=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]
I_zonal_t=[I_zonal_t1,I_zonal_t2,I_zonal_t3,I_zonal_t4,I_zonal_t5,I_zonal_t6,I_zonal_t7,I_zonal_t8,I_zonal_t9,I_zonal_t10]
###########################################################################
############################################################################
##############################################################################
#################################################################

#Loops below calculate the solution for transient infector over any specified time periods

###########################################
##############  Transient #################
###########################################

#looping solutions over different time periods for transient model
C0 = np.zeros(n) #inital concentration
E0 = np.zeros(n) #inital exposed
S0 = VentMatrix.K_zonal - I_zonal_t1 - E0 #inital suceptibles
Ct = np.empty((0,n))
St = np.empty((0,n))
Et = np.empty((0,n))
#combining intial conditions
X0 = np.hstack( (C0, S0, E0) )
print(X0)

for i in range(len(t)):
    
    V_zonal = VentilationMatrix(n, t[0], VentMatrix.Q_zonal, VentMatrix.geometry, filepath)
    print("V_zonal = " + str(V_zonal)) #print bounday flow to check its updating each step
    
    #solving
    x = odeint(odes, X0, t[i], args=(n, V_zonal, I_zonal_t[i], q_zonal, p_zonal, VentMatrix.v_zonal)) #args=()
    
    #re-defining initial conditions
    C0 = x[:, 0:n]
    S0 = x[:, n:2*n]
    E0 = x[:, 2*n:3*n] 
    
    X0 = np.hstack( (C0[-1,:], S0[-1,:], E0[-1,:]) )
    print(X0)
    
    #storing results in a vector
    Ct = np.vstack((Ct, C0))
    St = np.vstack((St,S0))
    Et = np.vstack((Et,E0)) 

    #End
#########################################
############ Steady State ###############
#########################################

E0star = np.zeros(n)
S0star = VentMatrix.K_zonal - I_zonal_t1 - E0star

Cstar = np.empty((0,n))
Ststar = np.empty((0,n))
Etstar = np.empty((0,n))

#initial condition
X0star = np.hstack((S0star, E0star))
print(X0star)

for j in range(len(t)):

    V_zonal = VentilationMatrix(n, t[0], VentMatrix.Q_zonal, VentMatrix.geometry, filepath)
    print("V_zonal = " + str(V_zonal)) #print bounday flow to check its updating each step
    V_zonal_inv = InvVentilationMatrix(V_zonal)
    print( "V_zonal_inv = " + str(V_zonal_inv))
    

    #solving steady state system with steady concentration
    x = odeint(steadyodes, X0star, t[j], args=(n, V_zonal_inv, I_zonal_t[j], q_zonal, p_zonal, VentMatrix.v_zonal))
    
    #rdfining initial conditions with stored solution
    S0star = x[:, 0:n]
    E0star = x[:, n:]
    
    
    #redefine initial conditions
    X0star = np.hstack((S0star[-1,:], E0star[-1,:]))
    print(X0star)
    
    #store values in a vector
    Ststar = np.vstack((Ststar, S0star))
    Etstar = np.vstack((Etstar, E0star))


    #defining the concentration value for each zone at each time period (cols represent zones, rows represent time periods)
    Cstar_t = np.matmul(V_zonal_inv, I_zonal_t[j]) * q_zonal
    Cstar_t = np.tile(Cstar_t, (len(t[j]), 1))
    Cstar = np.vstack((Cstar,Cstar_t))
    

#end

###########################################################################
###########################################################################
####################### population values###################################


#transinet version
St_pop = np.sum(St, axis=1) #axis=1 does rows, axis=0 does columns
Et_pop = np.sum(Et, axis=1)
S0_pop = np.sum(S0)
E0_pop = np.sum(E0)
I0_pop = np.sum(I_zonal)

#steady state
Ststar_pop = np.sum(Ststar, axis=1) #axis=1 does rows, axis=0 does columns
Etstar_pop = np.sum(Etstar, axis=1)
S0star_pop = np.sum(S0star)
E0star_pop = np.sum(E0star)

############################################################################
############################################################################
######################### Plotting #########################################
############################################################################
############################################################################

#define t for plotting 
#plotting in hours 
#t_hours = t/60

t_hours=np.empty((0,0))
for i in range(10):#note range runs for number of time periods defined
    t_hours = np.append(t_hours,t[i]/60) #to make all times plottable in hours not minutes
    
############################################################################
############################################################################

#uses a predefined function to plot all of the required outputs for this model
output_SE_Ct(n, t_hours, Ct, Cstar, St, Et, Ststar, Etstar, St_pop, Et_pop, Ststar_pop, Etstar_pop, I0_pop, start_time)
