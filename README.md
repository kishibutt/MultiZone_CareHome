# MultiZone_CareHome
This repository contains the code and data to reproduce the research contained in the manuscript "Environmental Data Monitoring and Infection Risks in UK Care-homes in the Context of COVID-19"; Kishwer Abdul Khaliq, Sara Mohamad, Alexander J. Edwards, Catherine J. Noakes, Andrew H. Kemp, Carl Thompson, Grainne McGill, Tim Sharpe.
The original code is taken from the research "A Mathematical Model for Assessing Transient Airborne Infection Risk in Hospital Ward"; Alexander J. Edwards, Lee Benson, Zeyu Guo, Martin Lopez-Garcia, Catherine J. Noakes, Daniel Peckham, Marco-Felipe King. 

# Software
This code is written using Python in Spyder 4.1.4. Users will also require CONTAM 3.4.0.3 to reproduce the airflow simulations. The original code can be found at https://github.com/scaje/Multi-zone_Hospital_conc_AJE.

# Description
1. To reproduce the concentration of pathogen solution and predicted exposure solution, use the script 'InfHCW_12zone_Conc_AJE.py'. To run this script you must define the file path for the .csv file containing the exported CONTAM results at the beginning of the code. This script uses the following to run:
* 'Function_scripts_AJE/Contam_flows_12zone_AJE.py' defines the ventilation matrix set-up.
* 'Contam_export_scripts_AJE/Contam_export_scripts_AJE.py' defines the inter-zonal flow values using exported CONTAM airflow simulations.
* 'Contam_export_scripts_AJE/results3.csv' contains the exported CONTAM simulation results which are used to define the inter-zonal flows and associated airflow. 
* 'Contam_export_scripts_AJE/read_csv_AJE.py' is used to read the exported CONTAM results from the .csv file.
* 'Function_scripts_AJE/SE_Conc_Eqn_AJE.py' contains the functions which solve the associated ODE equations for this study, including the Susceptible-Exposed model, and the concentration of pathogen model.
* 'Function_scripts_AJE/output_AJE.py' produces multiple general outputs for the script, including those used in the study analysis.
Please note that all of the above scripts and files must be in the working directory in order to run the main script, 'InfHCW_12zone_Conc_AJE.py'.

