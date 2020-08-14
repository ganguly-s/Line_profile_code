'''
This is a duplicate code of line_profile_test_02.py. The aim of this code
is to be able to compare and optimize LP calc.
Once this has been finalized, we will name it LP_calc1D.py.

Stores tau and flux corresponding to each Model and Line at Output/Model/Line
'''

# importing necessary libraries and scripts

import numpy as np
from opacity_table_v3 import *           # reads XSTAR lookup table
from matplotlib import pyplot as plt  
import matplotlib      
from my_athena_reader import *           # reads Athena++ output file
import pickle
import get_inp as gi			 # contains location of all input files for running LP code
#import fig_setup as fig			 # figure setup needs to be imported here although not required

####################################################################

# mention path of input (Athena) files. Imported from gi. Need to change path of 
# input files at gi.

####################################################################

# constants we'll need

mp  = 1.6726231e-24                      # 1.67262178e-24 g
pi  = np.pi
h   = 6.6262e-27                         # plank's constant in erg / s
C   = 3.0e10                             # 2.99792458e+10 cm / s
kb  = 1.380658e-16                       # 1.380658e-16 erg / K
mu  = 0.6
gamma = 1.6666667
nx = 1e8                                 # /cm^3

#####################################################################

# define function for LP calculation in v-space. For all lines including doublets

def LP_vel(Model,sn,Line):
    
	# hydro file from Athena "...out1.tab", "...out2.tab" not required,
	# can be computed here using xiu = 1.37045e19
	# opacity_file is the opacity table from XSTAR
	# Model and Line names as strings, sn the snapshot number
	
	Doublets = ['Si XIV 6','Si XIV 5','Mg XII','C II','S IV','C IV','C VI','Fe XXVI','O VI','He II','N V','O VIII','Si IV']
	
	flux = {}
	tau = {}
	
	# reading data from XSTAR lookup table and Athena++ results
	
	hydro_file = gi.get_Model(Model)+sn
	opacity_file, lines, matom = gi.get_Line(Line)
    	
    	####################################################################
	
    	# setting the basic parameters, velocity distribution space
	
	nu_lab0 = []
	for i in range(len(lines)):
		nu_lab0.append(C*1e8/lines[i])      # rest frequency of line
        
	hydroData = read_tab(hydro_file)
	optable   = opacity_table(opacity_file)
    	
	# setting velocity domain for LP calculation

	ymin = -7e7/C
	ymax = 2e7/C
	Nv=1000
	nu_dist = np.linspace(ymin,ymax,Nv)
	v = []
	for j in range(Nv):
		v.append(nu_dist[j]*C/1e5)         # velocity from Doppler shift from assumed distribution in km/s

    	####################################################################
    	
    	# extracting variables from Athena data
    	
	r = hydroData['x1v']
	dr = hydroData['x1v'][1:] - hydroData['x1v'][:-1] 
	rho = hydroData['rho']
	vel = hydroData['vel1']
	vel1 = vel
	vel = -vel1                             # sign of velocity needs to be inverted
	press = hydroData['press']
    	
	xiu = 1.37045e19
	xis = [xiu/(i*(j**2)) for i,j in zip (rho,r)]
   	
    	####################################################################
    
    	# calculating temperature and number density

	temp = []
	n_den = []
	for k in range(len(press)):
		temp.append(press[k]*mu*mp/kb/rho[k])
		n_den.append(rho[k]/mu/mp)

    	####################################################################

    	# starting line profile calculations
	if(Model=='Ax8'):
		sns = sn.split('.')[2]
	if(Model=='Bx8'):
		sns = sn.split('.')[3]
	print("Begin LP calculations for Model "+Model+','+sns)
	for i,snap in enumerate(lines):
		print ("Line "+Line, snap)
    
        	# val = sigma*nXSTAR, f0_array = nu_D (Doppler shifted frequency)
        	# vth is thermal velocity, vi is thermal velocity normalized to c
        	# k0 is the correctly normalized alpha obtained from XSTAR
    
		alpha_array = []
		f0_array = []
		k0 = []
		vth = []
		vi = []
		for k in range(len(dr)):
			val = optable.get_opacity(np.log10(xis[k]),np.log10(temp[k]),i)
			alpha_array.append(val*n_den[k]/nx)
			k0.append(alpha_array[k]/np.sqrt(pi))
			f0_array.append( (1. + vel[k]/C) )
			vth.append(np.sqrt(2*kb*temp[k]/matom))
			vi.append(vth[k]/C)
		   
		ta = []
		fl = []
    
		for k in range(len(nu_dist)):
			tmp = []
			for j in range(len(dr)):
				y = nu_dist[k]
				y -= vel[j]/C
				y *= 1/vi[j]
				phi = np.exp(-y*y)
				k1 = k0[j]*phi
				tmp.append(k1)
			tmp1 = []
			for j in range(len(tmp)-1):
				tmp1.append(0.5*(tmp[j]+tmp[j+1])*dr[j])
			ta.append(np.sum(tmp1))
			fl.append(np.exp(-ta[k]))
		tau[str(snap)] = ta
		flux[str(snap)] = fl
        	        
	tau['v'] = v
	flux['v'] = v

	path = Line+"/"+sns+".p"
	
    	# printing result in output files
	
	pickle.dump(tau, open("Output/"+Model+"/Optical_depth/"+path, "wb"))
	pickle.dump(flux, open("Output/"+Model+"/Flux/"+path, "wb"))
	
	# define function block to calculate LP against nu-space for Doublets

	if Line in Doublets:
		flux = {}
		tau = {}
    		
		y_dist = np.linspace(ymin,ymax,Nv)  # y~v/c
		ylos = [-i for i in y_dist]
		vel_dist = []

		v = []
        
		nu1 = []
		nu2 = []
		for j in range(Nv):
			vel_dist.append(y_dist[j]*C)       # velocity from Doppler shift from assumed distribution
			v.append(vel_dist[j]/1e5)           # velocity in units of km/s
			nu1.append((1-y_dist[j])*nu_lab0[0])
			nu2.append((1-y_dist[j])*nu_lab0[1])

		nuc = np.linspace(min(min(nu1),min(nu2)),max(max(nu1),max(nu2)),Nv)
		lc = [C*1e8/i for i in nuc]
		vc = [0 for i in nuc]
		sg = 6.652e-25 #cm^-2

		# starting line profile calculations

		# storing the optical depth of first of the doublet lines
		tau_init = [0 for i in range(len(v))]
		v_init = [0 for i in range(len(v))]
		print("Begin LP calculations for Model "+Model+','+sn)
		for i,snap in enumerate(lines):
			nu_lab = nu_lab0[i]
			print ("Line "+Line, snap)
    
			# val = sigma*nXSTAR, f0_array = nu_D (Doppler shifted frequency)
			# vth is thermal velocity, vi is thermal velocity normalized to c
			# k0 is the correctly normalized alpha obtained from XSTAR
    
			alpha_array = []
			f0_array = []
			k0 = []
			vth = []
			vi = []
			ln = []
			lxi = []
		
			for k in range(len(xis)):
				val = optable.get_opacity(np.log10(xis[k]),np.log10(temp[k]),i)
				alpha_array.append(val*n_den[k]/nx)
				k0.append(alpha_array[k]/np.sqrt(pi))
				f0_array.append( (1. + vel[k]/C) )
				vth.append(np.sqrt(2*kb*temp[k]/matom))
				vi.append(vth[k]/C)
    
			fl = []
			ta = []
			N = []
			ndr = []
			cs = 0
    
			for k in range(len(nuc)):
				s = 0
				tmp = []
				for j in range(len(dr)):
					y = -(nuc[k]-nu_lab0[i])/nu_lab0[i]
					vc[k] = y*C/1e5
					y -= vel[j]/C
					y *= 1/vi[j]
					phi = np.exp(-y*y)
					k1 = k0[j]*phi
					tmp.append(k1)
				tmp1 = []
				for j in range(len(tmp)-1):
					tmp1.append(0.5*(tmp[j]+tmp[j+1])*dr[j])
				ta.append(np.sum(tmp1))
				fl.append(np.exp(-ta[k]))
				if(i==0):
					tau_init[k] = ta[k]
					v_init[k] = vc[k]
		comp_t = [i+j for i,j in zip(tau_init,ta)]
		comp_f = [np.exp(-i) for i in comp_t]
		tau[Line] = comp_t
		flux[Line] = comp_f
		tau['v'] = v_init
		tau['lambda'] = lc
		tau['nu'] = nuc
		flux['v'] = v_init
		flux['lambda'] = lc
		flux['nu'] = nuc
    
		path = "/Doublets/"+Line+"/"+sns+".p"
		pickle.dump( tau, open( "Output/"+Model+"/Optical_depth/"+path, "wb" ) )
		pickle.dump( flux, open( "Output/"+Model+"/Flux/"+path, "wb" ) )    
