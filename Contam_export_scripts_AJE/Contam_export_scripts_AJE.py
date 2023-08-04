# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:58:09 2022

@author: scaje
"""
from read_csv_AJE import ReadCSV
import numpy as np



def boundary_flow_contam(filepath,n,t,geometry):
    flows = ReadCSV(filepath)
    print(flows)
    
    
    # boundary_flow defines flow from zone i to j
    boundary_flow = np.zeros((n,n))
    #Diagonal terms are zero
    for i in range(n):
        boundary_flow[i,i] = 0
       
     
    # t is a vector of vectors e.g t[i][0] calls the first entry of the ith vector in t
    # then since the format of the excel data includes 2 entries for each flow value we take steps in 2 rather than 1
    #the second index then selects the colum which refers to the boundary
   #boundary_flow[0,5] = flows[int((t[0])*2),6] + flows[int((t[0])*2+1),6]#example1
   #boundary_flow[zone1,zone6] = flows[int((t[firstDefinedTime])*2),CSVFileColoum (8-2) where results of zone1toZone6] + Samething for flow2 flows[int((t[0])*2+1),6]#reading method
       #
    #@kish- CH model geometry for reference
    # geometry[5,8]=1
    # geometry[3,8]=1
    # geometry[2,8]=1
    # geometry[1,8]=1
    # geometry[7,8]=1
    # geometry[8,9]=1
    # geometry[8,15]=1
    # geometry[8,13]=1
    # geometry[8,12]=1
    # geometry[12,14]=1
    # geometry[8,10]=1
    # geometry[0,1]=1
    # geometry[3,4]=1
    # geometry[11,15]=1
    # geometry[5,6]=1 #negative flow
    
    boundary_flow[5,8] = flows[int((t[0])*2),10] + flows[int((t[0])*2+1),10]#zone6 to zone 9
    boundary_flow[3,8] = flows[int((t[0])*2),11] + flows[int((t[0])*2+1),11]#zone 4 to zone 9
    boundary_flow[2,8] = flows[int((t[0])*2),12] + flows[int((t[0])*2+1),12]# zone 3 to zone 9
    boundary_flow[1,8] = flows[int((t[0])*2),13] + flows[int((t[0])*2+1),13]#zone2 to zone 9
    boundary_flow[7,8] = flows[int((t[0])*2),14] + flows[int((t[0])*2+1),14]#zone8 to 9
    boundary_flow[8,9] = -flows[int((t[0])*2),15] + flows[int((t[0])*2+1),15]#zone 10 to 9
    boundary_flow[8,15] = -flows[int((t[0])*2),16] + flows[int((t[0])*2+1),16]#zone 16 to 9
    boundary_flow[8,13] = -(flows[int((t[0])*2+1),17] +flows[int((t[0])*2),17])#zone14 to 9
    boundary_flow[8,12] = -(flows[int((t[0])*2+1),18] + flows[int((t[0])*2),18])#zone 13 to 9
    boundary_flow[12,14] = -(flows[int((t[0])*2+1),19] +flows[int((t[0])*2),19])#zone 15 to 13
    boundary_flow[8,16] = -(flows[int((t[0])*2+1),20] +flows[int((t[0])*2),20])#zone 17 to 9
    boundary_flow[8,10] = -(flows[int((t[0])*2+1),21] +flows[int((t[0])*2),21])#zone 11 to 9
    boundary_flow[0,1] = (flows[int((t[0])*2+1),24] +flows[int((t[0])*2),24])#zone 1 to 2
    boundary_flow[3,4] = (flows[int((t[0])*2+1),25] +flows[int((t[0])*2),25])#zone 3 to 4
    boundary_flow[11,15] = (flows[int((t[0])*2+1),26] +flows[int((t[0])*2),26])#zone 12 to 16
    boundary_flow[5,6] = -(flows[int((t[0])*2+1),27] +flows[int((t[0])*2),27])#zone 7 to 6
    
    #The following loop adjusts for the positive flow direction which is set in...
    #...contam to avoid negative flows i.e if the boundary flow value, i to j is...
    #... negative, then this flow should be for flow j to i
    for i in range(n):
        for j in range(n):
            if geometry[i,j] > 0:
                if boundary_flow[i,j] < 0:
                    boundary_flow[j,i] = - boundary_flow[i,j]
                    boundary_flow[i,j] = 0
                

    
    print("flow from zone i to zone k boundary_flow =" + str(boundary_flow))
    ###########################################################################
    
    
    return boundary_flow
