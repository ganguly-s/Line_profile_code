'''
Sythetic line profile generation for multiple files with the aim of 
generating avaeraged LP. Calculates optical depth and 
realtive flux or intensity for a particular line, such as CIV,
OVIII and Fe XXV. Plots a two panel figure showing tau and flux. 
'''

# importing necessary libraries and scripts

import numpy as np
from opacity_table_v3 import *           # reads XSTAR lookup table
from matplotlib import pyplot as plt  
import matplotlib      
from my_athena_reader import *           # reads Athena++ output file
import pickle
import get_inp as gi

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

####################################################################

fs = 12
fig, axs = plt.subplots(nrows=2,ncols=1,figsize=(8,4))
#fig, axs = plt.subplots(nrows=2,ncols=2)#,figsize=(10,6))
colr = ['blue','red']
plt.subplots_adjust(left=0.12, bottom=0.08, right=0.88, top=0.93, wspace=0.0, hspace=0.)
plt.rcParams['font.family'] = 'serif' #'STIXGeneral' #'serif'
matplotlib.rcParams['font.size'] = '16'
matplotlib.rcParams['ps.fonttype'] = 42 #note: fontype 42 compatible with MNRAS style file when saving figs
matplotlib.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['axes.linewidth'] = 1.
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.numpoints'] = 1  # uses 1 symbol instead of 2
plt.rcParams['legend.frameon'] = False 
plt.rcParams['legend.handletextpad'] = 0.3

def LP_vel(f1,f2,fop,lines,matom,Model,Line,sn):
    flux = {}
    tau = {}

    # reading data from XSTAR lookup table and Athena++ results
    if(Model!='Bx8'):
        hydro_file   = f1
        hydro_file1 =  f2
    else:
        hydro_file = f1
    
    opacity_file = fop
    
    ####################################################################

    # setting the basic parameters, velocity distribution space

    nu_lab0 = []
    for i in range(len(lines)):
        nu_lab0.append(C*1e8/lines[i])      # rest frequency of line
        
    optable   = opacity_table(opacity_file)
    hydroData = read_tab(hydro_file)
    if(Model!='Bx8'):
        hydroData1 = read_tab(hydro_file1)
    
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
    #if(Model=='Bx8'):
    xiu = 1.37045e19
    xis = [xiu/(i*(j**2)) for i,j in zip (rho,r)]
    #else:
    #xis = hydroData1['user_out_var0']
    #xis = xis.tolist()

    ####################################################################
    
    # calculating temperature and number density

    temp = []
    n_den = []
    for k in range(len(press)):
        temp.append(press[k]*mu*mp/kb/rho[k])
        n_den.append(rho[k]/mu/mp)

    ####################################################################

    # starting line profile calculations
    
    print("Begin LP calculations for Model "+Model+','+sn)
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
        for k in range(len(k0)):
            if(k0[k]==max(k0)):
                print(k0[k],r[k],vel[k]/1e5,temp[k],vth[k]/1e5)
                break   
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
        #axs[0].plot(v,ta,lw=2,label=Model[i])
        #axs[1].plot(v,fl,lw=2,label=Model[i])
        '''
        for k in range(len(ta)):
            if(ta[k]==max(ta)):
                print(ta[k],v[k])
                break
        '''
        
    tau['v'] = v
    flux['v'] = v
    '''
    axs[0].set_xlim(ymin*C/1e5,ymax*C/1e5)
    axs[1].set_xlim(ymin*C/1e5,ymax*C/1e5)
    axs[1].set_xlabel('v[km/s]',fontsize=fs)
    axs[0].set_ylabel(r"$\tau_\nu$", fontsize=fs,rotation=0,labelpad=14)
    axs[1].set_ylabel(r"$I_\nu$", fontsize=fs,rotation=0,labelpad=14)
    vh = np.linspace(ymin*C/1e5,ymax*C/1e5,10)
    th = [1 for i in range(10)]
    axs[0].plot(vh,th,'k--')
    axs[0].set_yscale('log') 
    axs[0].set_ylim(1e-3,5e3)
    axs[1].set_ylim(0,1.2)
    axs[1].legend(frameon=False,fontsize=10,loc='best')#, bbox_to_anchor=(1, 0.5))   
    plt.setp(axs[1].get_yticklabels()[-1],visible=False)

    
    axs[0].tick_params(which='major',axis='both',direction='in',width=1.)
    axs[1].tick_params(which='major',axis='both',direction='in',width=1.)

    #plt.setp(axs[0].get_xticklabels(), visible=False)
    plt.suptitle(Line+', '+str(snap),fontsize=fs)
    #plt.savefig("FeXXV.png", bbox_inches='tight',dpi=300)
    '''
    # printing result in output files
    if(Model=='Ax8'):
        pickle.dump( tau, open( "Output/tauA_hires/"+Line+"/"+sn+".p", "wb" ) )
        pickle.dump( flux, open( "Output/fluxA_hires/"+Line+"/"+sn+".p", "wb" ) )
    if(Model=='Bx8'):
        pickle.dump( tau, open( "Output/tauB_hires/"+Line+"/"+sn+".p", "wb" ) )
        pickle.dump( flux, open( "Output/fluxB_hires/"+Line+"/"+sn+".p", "wb" ) )
    
        
def LP_freq(f1,f2,fop,lines,matom,Model,Line,sn):
    flux = {}
    tau = {}
    
    # reading data from XSTAR lookup table and Athena++ results
    if(Model!='Bx8'):
        hydro_file   = f1
        hydro_file1 =  f2
    else:
        hydro_file = f1
    
    opacity_file = fop

    ####################################################################

    # setting the basic parameters, velocity distribution space

    nu0 = []
    for i in range(len(lines)):
        nu0.append(C*1e8/lines[i])      # rest frequency of line

    optable   = opacity_table(opacity_file)
    hydroData = read_tab(hydro_file)
    if(Model!='Bx8'):
        hydroData1 = read_tab(hydro_file1)

    ymin = -7e7/C
    ymax = 10e6/C
    Nv=1000
    y_dist = np.linspace(ymin,ymax,Nv)  # y~v/c
    ylos = [-i for i in y_dist]
    vel_dist = []

    v = []

    nu1 = []
    nu2 = []
    for j in range(Nv):
        vel_dist.append(y_dist[j]*C)       # velocity from Doppler shift from assumed distribution
        v.append(vel_dist[j]/1e5)           # velocity in units of km/s
        nu1.append((1-y_dist[j])*nu0[0])
        nu2.append((1-y_dist[j])*nu0[1])

    nuc = np.linspace(min(min(nu1),min(nu2)),max(max(nu1),max(nu2)),Nv)
    lc = [C*1e8/i for i in nuc]
    vc = [0 for i in nuc]
    sg = 6.652e-25 #cm^-2
    ####################################################################
    
    # extracting variables from Athena data
    
    r = hydroData['x1v']
    r = r.tolist()
    dr = hydroData['x1v'][1:] - hydroData['x1v'][:-1] 
    dr = dr.tolist()
    nur = C*1e8/lines[0]
    rho = hydroData['rho']
    rho = rho.tolist()
    vel = hydroData['vel1']
    vel = vel.tolist()
    vel1 = vel
    vel = [-j for j in vel]                # sign of velocity needs to be inverted
    press = hydroData['press']
    press = press.tolist()
    #if(Model=='Bx8'):
    xiu = 1.37045e19
    xis = [xiu/(i*(j**2)) for i,j in zip (rho,r)]
    #else:
    #    xis = hydroData1['user_out_var0']
    #    xis = xis.tolist()
    if(Model=='B'):
        xis = xis[1:]
    
    ####################################################################

    # calculating temperature and number density

    temp = []
    n_den = []
    dn = []
    dxi = []
    for k in range(len(press)):
        temp.append(press[k]*mu*mp/kb/rho[k])
        n_den.append(rho[k]/mu/mp)
    for k in range(len(n_den)-1):
        dn.append(abs((n_den[k+1]-n_den[k])/(r[k+1]-r[k])))
        dxi.append(abs((xis[k+1]-xis[k])/(r[k+1]-r[k])))

    # starting line profile calculations

    # storing the optical depth of first of the doublet lines
    tau_init = [0 for i in range(len(v))]
    v_init = [0 for i in range(len(v))]
    print("Begin LP calculations for Model "+Model+','+sn)
    for i,snap in enumerate(lines):
        nu_lab = nu0[i]
        print ("Line "+Line, snap)
    
        # val = sigma*nXSTAR, f0_array = nu_D (Doppler shifted frequency)
        # vth is thermal velocity, vi is thermal velocity normalized to c
        # k0 is the correctly normalized alpha obtained from XSTAR
    
        alpha_array = []
        alpha_array1 = []
        f0_array = []
        k0 = []
        k01 = []
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
        for k in range(len(k0)):
            if(k0[k]==max(k0)):
                print(k0[k],r[k],vel[k]/1e5,temp[k],vth[k]/1e5)
                break
    
        flux = []
        tau = []
        N = []
        ndr = []
        cs = 0
    
        for k in range(len(nuc)):
            s = 0
            tmp = []
            for j in range(len(dr)):
                '''
                if(k==0):
                    ln.append(n_den[j]*n_den[j]*sg/dn[j])
                    lxi.append(n_den[j]*sg*xis[j]/dxi[j])
                    cs += n_den[j]*dr[j]
                    N.append(sg*cs)
                    ndr.append(sg*n_den[j]*dr[j])
                '''
                y = -(nuc[k]-nu0[i])/nu0[i]
                vc[k] = y*C/1e5
                y -= vel[j]/C
                y *= 1/vi[j]
                phi = np.exp(-y*y)
                k1 = k0[j]*phi
                tmp.append(k1)
            tmp1 = []
            for j in range(len(tmp)-1):
                tmp1.append(0.5*(tmp[j]+tmp[j+1])*dr[j])
            tau.append(np.sum(tmp1))
            flux.append(np.exp(-tau[k]))
            if(i==0):
                tau_init[k] = tau[k]
                v_init[k] = vc[k]
    
    comp_t = [i+j for i,j in zip(tau_init,tau)]
    comp_f = [np.exp(-i) for i in comp_t]
    flux = {}
    tau = {}
    tau[Line] = comp_t
    flux[Line] = comp_f
    tau['v'] = v_init
    tau['lambda'] = lc
    tau['nu'] = nuc
    flux['v'] = v_init
    flux['lambda'] = lc
    flux['nu'] = nuc
    
    if(Model=='Ax8'):
        pickle.dump( tau, open( "Output/tauA_hires/Doublets/"+Line+"/"+sn+".p", "wb" ) )
        pickle.dump( flux, open( "Output/fluxA_hires/Doublets/"+Line+"/"+sn+".p", "wb" ) )
    if(Model=='Bx8'):
        pickle.dump( tau, open( "Output/tauB_hires/Doublets/"+Line+"/"+sn+".p", "wb" ) )
        pickle.dump( flux, open( "Output/fluxB_hires/Doublets/"+Line+"/"+sn+".p", "wb" ) )
    
    