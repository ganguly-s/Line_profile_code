'''
This is a duplicate code of line_profile_test_02.py. The aim of this code
is to be able to compare and optimize LP calc.
Once this has been finalized, we will name it LP_calc1D.py.

Stores tau and flux corresponding to each Model and Line at Output/Model/Line
'''

# importing necessary libraries and scripts
import os
import numpy as np
from opacity_table_v3 import *           # reads XSTAR lookup table
from my_athena_reader import *           # reads Athena++ output file
import pickle
import get_inp as gi			 # contains location of all input files for running LP code
#import fig_setup as fig			 # figure setup needs to be imported here although not required
from time import time
from matplotlib import pyplot as plt
from fnmatch import filter
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
# function for opacity calcualtion
def calc_opacity(opacity_file,fn,lines,xis,temp):
	op = {}
	optable = opacity_table(opacity_file)
	#of = opacity_file.replace('XSTARtab/','')
	#pickled_ion = of.split('.')[0]+'.p'
	#pickle.dump(optable,open(pickled_ion,"wb"))
	#f = pickle.load(open(pickled_ion,"rb"))
	
	for i,snap in enumerate(lines):
		val = np.zeros(len(xis))
		for k in range(len(xis)):
			val[k] = optable.get_opacity(np.log10(xis[k]),np.log10(temp[k]),i)
			val[k] 
		op[snap] = val
	pickle.dump(op,open(fn,"wb"))

# define function for LP calculation in v-space. For all lines including doublets

def LP_calc_1D(Model,sn,Line):
    
	# hydro file from Athena "...out1.tab", "...out2.tab" not required,
	# can be computed here using xiu = 1.37045e19
	# opacity_file is the opacity table from XSTAR
	# Model and Line names as strings, sn the snapshot number
	
	Doublets = ['Si_XIV_6','Si_XIV_5','Mg_XII','C_II','S_IV','C_IV','C_VI','Fe_XXVI','O_VI','He_II','N_V','O_VIII_19','Si_IV']
	
	flux = {}
	tau = {}
	
	# reading data from XSTAR lookup table and Athena++ results
	#lst = filter(os.listdir(gi.get_Model(Model)),'*.out1.*')
	#lst.sort()
	hydro_file = gi.get_Model(Model)+sn
	opacity_file, lines, matom = gi.get_Line(Line)
	hydroData = read_tab(hydro_file)
	
	# starting line profile calculations
	if(Model=='Ax8'):
        	sns = sn.split('.')[2]
	if(Model=='Bx8'):
        	sns = sn.split('.')[3]
	
    	####################################################################
	
    	# setting the basic parameters, velocity distribution space
	
	nu_lab0 = []
	for i in range(len(lines)):
		nu_lab0.append(C*1e8/lines[i])      # rest frequency of line
        
	# setting velocity domain for LP calculation

	ymin = -7e7/C
	ymax = 2e7/C
	Nv=1000
	nu_dist = np.array(np.linspace(ymin,ymax,Nv))
	v = nu_dist*C/1e5         # velocity from Doppler shift from assumed distribution in km/s

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
	xis = xiu/rho/r/r
   	
    	####################################################################
    
    	# calculating temperature and number density

	temp = press*mu*mp/kb/rho
	n_den = rho/mu/mp
	vth = np.sqrt(2*kb*temp/matom)
	vth /= C
	
	####################################################################

	# obtaining pickled opacity results
	start = time()
	fn_op = 'opacities/'+Line+'/'+sns+'.p'
	recalc = 1
	if recalc:
		print("\nBuilding opacity file using table\n{}".format(opacity_file))
		calc_opacity(opacity_file,fn_op,lines,xis,temp)
		op = pickle.load(open(fn_op,"rb"))
	else:
		try:    
			print("\n Attempting to open {}".format(fn_op))
			op = pickle.load(open(fn_op, "rb"))
			print("\nSuccess!")
		except:
			print("\nBuilding opacity file using table\n{}".format(opacity_file))
			calc_opacity(opacity_file,fn_op,lines,xis,temp)
			op = pickle.load(open(fn_op,"rb"))
	stop = time()
	print(stop-start)
	# starting line profile calculations
	
	print("Begin LP calculations for Model "+Model+','+sns)
	for i,snap in enumerate(lines):
		print ("Line "+Line, snap)
    
        	# val = sigma*nXSTAR, f0_array = nu_D (Doppler shifted frequency)
        	# vth is thermal velocity, vi is thermal velocity normalized to c
        	# k0 is the correctly normalized alpha obtained from XSTAR
    
		alpha_array = op[snap]*n_den/nx
		k0 = alpha_array/np.sqrt(pi)

		ta = np.zeros(len(nu_dist))
		fl = np.zeros(len(nu_dist))
    
		for k in range(len(nu_dist)):
			tmp = np.zeros(len(dr))
			for j in range(len(dr)):
				y = nu_dist[k]
				y -= vel[j]/C
				y *= 1/vth[j]
				phi = np.exp(-y*y)
				k1 = k0[j]*phi
				tmp[j] = k1
			ta[k] = np.sum(0.5*(tmp[1:] - tmp[:-1])*dr[:-1])
			fl[k] = np.exp(-ta[k])
		tau[str(snap)] = ta
		flux[str(snap)] = fl
	#plt,plot(v,ta)
	#plt.show()	        
	tau['v'] = v
	flux['v'] = v

	path1 = "Output/"+Model+"/Optical_depth/"+Line+"/"
	path2 = "Output/"+Model+"/Flux/"+Line+"/"

	# printing result in output files
        
	if not os.path.exists(path1):
		os.mkdir(path1)
	if not os.path.exists(path2):
		os.mkdir(path2)
	pickle.dump(tau, open(path1+sns+".p", "wb"))
	pickle.dump(flux, open(path2+sns+".p", "wb"))
	# define function block to calculate LP against nu-space for Doublets

	if Line not in Doublets:
		flux = {}
		tau = {}
    		
		y_dist = np.array(np.linspace(ymin,ymax,Nv))  # y~v/c
		ylos = -y_dist
		vel_dist = y_dist*C
		v = vel_dist/1e5
		nu1 = (1-y_dist)*nu_lab0[0]
		nu2 = (1-y_dist)*nu_lab0[1]
		
		nuc = np.array(np.linspace(min(min(nu1),min(nu2)),max(max(nu1),max(nu2)),Nv))
		lc = C*1e8/nuc
		vc = np.zeros(len(nuc))
		sg = 6.652e-25 #cm^-2

		# starting line profile calculations

		# storing the flux and optical depth of first of the doublet lines
		tau_init = np.zeros(len(v))
		v_init = np.zeros(len(v))
		print("Begin LP calculations for Model "+Model+','+sns)
		for i,snap in enumerate(lines):
			nu_lab = nu_lab0[i]
			print ("Line "+Line, snap)
    
			# val = sigma*nXSTAR, f0_array = nu_D (Doppler shifted frequency)
			# vth is thermal velocity, vi is thermal velocity normalized to c
			# k0 is the correctly normalized alpha obtained from XSTAR
    
			alpha_array = op[snap]*n_den/nx
			f0_array = 1+vel/C
			k0 = alpha_array/np.sqrt(pi)
			vth = np.sqrt(2*kb*temp/matom)
			vi = vth/C
			 
			fl = np.zeros(len(nuc))
			ta = np.zeros(len(nuc))
    
			for k in range(len(nuc)):
				tmp = np.zeros(len(dr))
				for j in range(len(dr)):
					y = -(nuc[k]-nu_lab0[i])/nu_lab0[i]
					vc[k] = y*C/1e5
					y -= vel[j]/C
					y *= 1/vi[j]
					phi = np.exp(-y*y)
					k1 = k0[j]*phi
					tmp[j] = k1
				ta[k] = np.sum(0.5*(tmp[1:]+tmp[:-1])*dr[:-1])
				fl[k] = np.exp(-ta[k])
				if(i==0):
					tau_init[k] = ta[k]
					v_init[k] = vc[k]
		comp_t = tau_init + ta#[i+j for i,j in zip(tau_init,ta)]
		comp_f = np.exp(-comp_t)#[np.exp(-i) for i in comp_t]
		tau[Line] = comp_t
		flux[Line] = comp_f
		tau['v'] = v_init
		tau['lambda'] = lc
		tau['nu'] = nuc
		flux['v'] = v_init
		flux['lambda'] = lc
		flux['nu'] = nuc
    		
		path1 = "Output/"+Model+"/Optical_depth/Doublets/"+Line+"/"
		path2 = "Output/"+Model+"/Flux/Doublets/"+Line+"/"
		if not os.path.exists(path1):
			os.mkdir(path1)
		if not os.path.exists(path2):
			os.mkdir(path2)
		pickle.dump( tau, open( path1+sns+".p", "wb" ) )
		pickle.dump( flux, open( path2+sns+".p", "wb" ) )


#LP_calc_1D('Bx8','02000','C_IV')
