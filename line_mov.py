#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 11:05:49 2020

@author: ganguly93
"""
import pickle
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
path = 'Output/fluxB_hires/Doublets/Mg XII/'
Model = 'Bx8'
Line = 'Mg XII'
lst = os.listdir(path)
lst.sort()

# figure setup
fs = 12
fig, axs = plt.subplots(nrows=1,ncols=1,figsize=(13,5))  
fig.suptitle(Line+", Model "+Model, fontsize=fs)
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

im   = axs.plot([],[], 'k')#[0] 
im1  = axs.plot([],[], 'k--')
# set label names
axs.set_xlabel("v [km/s]")
axs.set_ylabel(r"$I_\nu$",rotation=0,fontsize=fs)

# minor axes on
axs.minorticks_on()

# tick params in
axs.tick_params(which='both',bottom=True, top=True, left=True, right=True,direction='in')

time_text1 = axs.text(-550,0.3,' ',fontsize=fs)
time_text2 = axs.text(-550,0.25,' ',fontsize=fs-2)
axs.set_xlim([-600,100])
axs.set_ylim(0,1)
    
def init():
    for sp in range(1):
        im[sp].set_data([], [],'k')
        im1[sp].set_data([], [], 'k--')
        #legs[sp].texts[0].set_text('')
    time_text1.set_text('')
    time_text2.set_text('')
    return im, time_text1, time_text2

def update(i):
    f = pickle.load(open(path+"/"+lst[i],"rb"))
    f1 = pickle.load(open('Output/averageB/Doublets/Mg XII/flux_100.p','rb'))
    for sp in range(1):
        x = f['v']
        y = f[Line]
        im[sp].set_data(x,y)
        im1[sp].set_data(f1['v'],f1[Line])
        im[sp].axes.set_ylim(0,1)
    lab = str(i).zfill(5)
    time_text1.set_text(lab)
    time_text2.set_text('Ganguly et al.(2020) (in prep)')
    #legs[sp].texts[0].set_text(lab)
    #legs[sp].texts[1].set_text(lab)

    return im, time_text1, time_text2# +legs 

ani = anim.FuncAnimation(fig,update, frames=len(lst),blit=False,interval=100)
# for A 
#ani.save(filename='flowAx8.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
# for B
ani.save(filename='Mg_XII_Bx8.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()