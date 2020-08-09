import numpy as np
import pylab as plt
import matplotlib.animation as anim
import matplotlib
from matplotlib.pylab import *
import matplotlib.animation as animation
import os, fnmatch
from opacity_table_v3 import *           # reads XSTAR lookup table
from my_athena_reader import *           # reads Athena++ output file

# constants we'll need
mp  = 1.6726231e-24                      # 1.67262178e-24 g
C   = 3.0e10                             # 2.99792458e+10 cm / s
kb  = 1.380658e-16                       # 1.380658e-16 erg / K
mu  = 0.6

# for A
#path = 'model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/'
#Model = 'Ax8'
# for B
path = 'model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/'
Model = 'Bx8'
lst = fnmatch.filter(os.listdir(path),'*.out1.*')
lst.sort()

# figure setup
fs = 12
fig, axs = plt.subplots(nrows=1,ncols=3,figsize=(13,5))  
fig.suptitle("Flow properties, Model "+Model, fontsize=fs)
plt.subplots_adjust(left=0.05, bottom=0.08, right=0.92, top=0.93, wspace=0.3, hspace=0.)
plt.rcParams['font.family'] = 'serif' #'STIXGeneral' #'serif'
matplotlib.rcParams['font.size'] = '16'
matplotlib.rcParams['ps.fonttype'] = 42 #note: fontype 42 compatible with MNRAS style file when saving figs
matplotlib.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.linewidth'] = 1.
plt.rcParams['xtick.major.size'] = 6
plt.rcParams['xtick.minor.size'] = 3
plt.rcParams['ytick.major.size'] = 6
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12
plt.rcParams['legend.numpoints'] = 1  # uses 1 symbol instead of 2
plt.rcParams['legend.frameon'] = False 
plt.rcParams['legend.handletextpad'] = 0.3

im   = [ax.plot([],[], 'k')[0] for ax in axs]

# set label names
axs[1].set_xlabel("v [km/s]")
axs[0].set_ylabel("T",rotation=0,fontsize=fs)
axs[1].set_ylabel(r"$\xi$",rotation=0,fontsize=fs)
axs[2].set_ylabel(r"$\Xi$",rotation=0,fontsize=fs)

# minor axes on
axs[0].minorticks_on()
axs[1].minorticks_on()
axs[2].minorticks_on()

# tick params in
axs[0].tick_params(which='both',bottom=True, top=True, left=True, right=True,direction='in')
axs[1].tick_params(which='both',bottom=True, top=True, left=True, right=True,direction='in')
axs[2].tick_params(which='both',bottom=True, top=True, left=True, right=True,direction='in')

time_text = axs[1].text(450,10,' ',fontsize=fs)
for ax in axs:
    ax.set_xlim([0,600])
    ax.set_yscale('log')
    
def init():
    for sp in range(3):
        im[sp].set_data([], [],'k')
        #legs[sp].texts[0].set_text('')
    time_text.set_text('')
    return im, time_text

def update(i):
    hydro_file = path+lst[i]
    hydroData = read_tab(hydro_file)
    r = hydroData['x1v']
    r = r.tolist()
    rho = hydroData['rho']
    rho = rho.tolist()
    vel = hydroData['vel1']
    vel = vel.tolist()
    vel = [j/1e5 for j in vel]                # sign of velocity needs to be inverted
    press = hydroData['press']
    press = press.tolist()
    xiu = 1.37045e19
    xis = [xiu/(i*(j**2)) for i,j in zip (rho,r)]
    temp = []
    Xi = []
    n_den = []
    for k in range(len(vel)):
        temp.append(press[k]*mu*mp/kb/rho[k])
        n_den.append(rho[k]/mu/mp)
        Xi.append(xis[k]/temp[k])
    for sp in range(3):
        x = vel
        if(sp==0):
            y = temp
        if(sp==1):
            y = xis
        if(sp==2):
            y = Xi
        
        im[sp].set_data(x,y)
        im[sp].axes.set_ylim(min(y),max(y))
    lab = str(i).zfill(5)
    time_text.set_text(lab)
    #legs[sp].texts[0].set_text(lab)
    #legs[sp].texts[1].set_text(lab)

    return im, time_text# +legs 

ani = anim.FuncAnimation(fig,update, frames=len(lst),blit=False,interval=100)
# for A 
#ani.save(filename='flowAx8.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
# for B
ani.save(filename='flowBx8.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()