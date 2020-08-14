#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 15:01:27 2020

@author: ganguly93
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 13:51:12 2020

@author: ganguly93
"""

mp  = 1.6726231e-24                      # 1.67262178e-24 g

# function for getting files for different models

def get_Model(mname):
    if (mname=='A'): # Model A
        hydro_file   = "Athenatab/hep18/agn1.hep18.merged.out1.01200.tab"
        hydro_file1 =  "Athenatab/hep18/agn1.hep18.merged.out2.01200.tab"
    if (mname=='B'): # Model B
        hydro_file   = "Athenatab/hep17/agn1.hep17.merged.out1.01200.tab"
        hydro_file1 =  "Athenatab/hep17/agn1.hep17.merged.out2.01200.tab"
    if (mname=='ddAx8'): # high-res Model A 
        hydro_file = "Athenatab/ddAx8/agn1.out1.01750.tab" 
        hydro_file1 = "Athenatab/ddAx8/agn1.out2.01750.tab"		
    if (mname=='ddBx8'): # high-res Model B
        hydro_file = "Athenatab/ddBx8/agn1.out1.01950.tab" 
        hydro_file1 = " "
    if (mname=='hiresA_800'):
        hydro_file = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out1.00800.tab"
        hydro_file1 = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out2.00800.tab"
    if (mname=='hiresA_820'):
        hydro_file = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out1.00820.tab"
        hydro_file1 = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out2.00820.tab"
    if (mname=='Ax8'):
        hydro_file = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out1.00840.tab"
        hydro_file1 = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/agn1.out2.00840.tab"
        sn = str(840).zfill(5)
    if (mname=='hiresB_1950'):
        hydro_file = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out1.01950.tab"
        hydro_file1 = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out2.01950.tab"
    if (mname=='hiresB_1975'):
        hydro_file = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out1.01975.tab"
        hydro_file1 = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out2.01975.tab"
    if (mname=='Bx8'):
        hydro_file = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out1.02000.tab"
        hydro_file1 = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/agn1.merged.out2.02000.tab"
        sn = str(2000).zfill(5)
    if (mname=='Ax8'):
        hydro_file = "model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/"
    if (mname=='Bx8'):
        hydro_file = "model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/"
    return hydro_file

# function for getting files for different lines

def get_Line(line):
    # non-doublets
    if (line=='C II'):
        opacity_file = "XSTARtab/c_ii_1335.dat"
        lines = [1335.71, 1334.52]
        matom = mp * 12      # mass of target atom in g
    if (line=='Fe XXV'):
        opacity_file = "XSTARtab/fe_xxv_6.7keV.dat"
        lines = [1.8505]
        matom = mp * 52       # mass of target atom in g
    if (line=='O VII'):
        opacity_file = "XSTARtab/o_vii_22.dat"
        lines = [21.602]
        matom = mp * 16      # mass of target atom in g
    if (line=='Ne VIII'):
        opacity_file = "XSTARtab/ne_viii_780.dat"
        lines = [780.324]
        matom = mp * 20.     # mass of target atom in g 
    if (line=='S IV'):
        opacity_file = "XSTARtab/s_iv_1073.dat"
        lines = [1072.97, 1073.51]
        matom = mp * 32.     # mass of target atom in g 
    if (line=='S IV*'):
        opacity_file = "XSTARtab/s_iv_1063.dat"
        lines = [1062.66]
        matom = mp * 32.     # mass of target atom in g 
    if (line=='Si III'):
        opacity_file = "XSTARtab/si_iii_1206.dat"
        lines = [1206.5]
        matom = mp * 28.     # mass of target atom in g 
    if (line=='Mg II'):
        opacity_file = "XSTARtab/mg_ii_2798.dat"
        lines = [2798.75]
        matom = mp * 24.
    if (line=='S XVI'):
        opacity_file = "XSTARtab/s_xvi_4.dat"
        lines = [3.9908] 
        matom = mp * 32.
    if (line=='Ar XVIII'):
        opacity_file  = "XSTARtab/ar_xviii_4.dat"
        lines = [3.7311] 
        matom = mp * 36.
    
    # doublets
    if (line=='C IV'):
        opacity_file = "XSTARtab/c_iv_1550.dat"
        lines = [1550.77, 1548.2]
        matom = mp * 12      # mass of target atom in g
    if (line=='C VI'):
        opacity_file = "XSTARtab/c_vi_33.dat"
        lines = [33.7396, 33.7342]	
        matom = mp * 12      # mass of target atom in g
    if (line=='Fe XXVI'):
        opacity_file = "XSTARtab/fe_xxvi_6.966keV.dat"
        lines = [1.78344, 1.77802]
        matom = mp * 52       # mass of target atom in g
    if (line=='O VI'):
        opacity_file = "XSTARtab/o_vi_1034.dat"
        lines = [1031.91, 1037.61] 
        matom = mp * 16      # mass of target atom in g
    if (line=='He II'):
        opacity_file = "XSTARtab/he_ii_304.dat"
        lines = [303.786, 303.78]
        matom = mp * 4       # mass of target atom in g
    if (line=='N V'):
        opacity_file = "XSTARtab/n_v_1240.dat"
        lines = [1238.82,1242.8]
        matom = mp * 14.     # mass of target atom in g  
    if (line=='O VIII'):
        opacity_file = "XSTARtab/o_viii_19.dat"
        lines = [18.9725,18.9671]
        matom = mp * 16      # mass of target atom in g
    if (line=='Si IV'):
        opacity_file = "XSTARtab/si_iv_1394.dat"
        lines = [1393.76, 1402.77]
        matom = mp * 28.     # mass of target atom in g 
    if (line=='Mg XII'):
        opacity_file = "XSTARtab/mg_xii_7.dat"
        lines = [7.10691, 7.10577]
        matom = mp * 24
    if (line=='N VII'):
        opacity_file = "XSTARtab/n_vii_25.dat"
        lines = [24.7846, 24.7792]
        matom = mp * 14  
    if (line=='Ne X'):
        opacity_file = "XSTARtab/ne_x_10.dat"
        lines = [10.2396, 10.2385]
        matom = mp * 20.
    if (line=='O VIII 15'):
        opacity_file = "XSTARtab/o_viii_15.dat"
        lines = [15.1765, 15.176]
        matom = mp * 16.
    if (line=='O VIII 16'):
        opacity_file = "XSTARtab/o_viii_16.dat"
        lines = [16.0067, 16.0055]
        matom = mp * 16.
    if (line=='Si XIV 5'):
        opacity_file = "XSTARtab/si_xiv_5.dat"
        lines = [5.21795,5.21681]
        matom = mp * 28.
    if(line=='Si XIV 6'):
        opacity_file = "XSTARtab/si_xiv_6.dat"
        lines = [6.18583,6.18042]
        matom = mp * 28.
    return (opacity_file,lines,matom)