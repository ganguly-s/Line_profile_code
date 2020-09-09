'''
Main script for line profile calculation
Prompts user to select the following:
Choose from hydro model: Option A and B or both
Choose from list of Lines: list of lines (enumerated)
(enter a number to select the line of choice or choose all) 
Choose range of snapshots: give choices based on Model selected
'''

# import necessary python library
import numpy as np
import os

# import other necessary python scripts
import get_inp as gi
import line_profile_op as lp

# arrays of Models and Lines
Models = np.array(['Ax1','Bx1','Ax8','Bx8'])
Line = np.array(['Mg_XII','Mg_II','C_II','Fe_XXV','Fe_XXVI','O_VII','Ne_VIII','S_IV','S_IV*','Si_III','C_IV','C_VI','O_VI','He_II','N_V','O_VIII_19','Si_IV','N_VII','O_VIII_15','O_VIII_16','Ne_X','S_XVI_4','Ar_XVIII','Si_XIV_5','Si_XIV_6'])
Doublets = np.array(['Si_XIV 6','Si_XIV 5','Mg_XII','C_II','S_IV','C_IV','C_VI','Fe_XXVI','O_VI','He_II','N_V','O_VIII_19','Si_IV'])

# prompt for user choice
print("Let's compute some line profiles....")
print("\nAvailable models:")
for i,mod in enumerate(Models):
	print(str(i+1)+". "+mod)
	if(i+1==len(Models)):
		print(str(i+2)+". All of the above") 
mod_ch = int(input("Choose a model (enter an integer):"))
print("\nAvailable choice of ions:")
for i,ln in enumerate(Line):
	print(str(i+1)+". "+ln)
	if(i+1==len(Line)):
		print(str(i+2)+". All of the above") 
line_ch = int(input("Choose an ion (enter an integer):"))
# selection of snapshots to compute LP of
start_ind = -1
stop_ind = -1
try:
	print(f"Initiating computation of line profile for model {Models[mod_ch-1]}, {Line[line_ch-1]}")
except:
	if mod_ch > len(Models) and line_ch > len(Line):
		print("Initiating computation of line profile for all models and ions....")
	elif mod_ch > len(Models) and line_ch <= len(Line):
		print(f"Initiating computation of line profile for all models for {Line[line_ch-1]}...")
	else:
		print(f"Initiating computation of line profile for model {Models[mod_ch-1]} for all ions...")
