#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 22 13:44:48 2020

@author: ganguly93
"""
import os
import fnmatch
import get_inp as gi
import line_profile_test_02 as lptst

if 0:
    Model = ['Ax8']#,'Bx8']
    Line = ['Mg XII','Mg II','C II','Fe XXV','Fe XXVI','O VII','Ne VIII','S IV','S IV*','Si III','C IV','C VI','O VI','He II','N V','O VIII','Si IV']
    Doublets = ['Si XIV 6','Mg XII','C II','S IV','C IV','C VI','Fe XXVI','O VI','He II','N V','O VIII','Si IV']
    Line = ['Si XIV 6']
    Line = ['He II']
    for i in range(len(Model)):
        f1,f2,sn = gi.get_Model(Model[i])
        for j in range(len(Line)):
            ot, line, ma = gi.get_Line(Line[j])
            lptst.LP_vel(f1,f2,ot,line, ma, Model[i],Line[j],sn)
            if Line[j] in Doublets:
                lptst.LP_freq(f1,f2,ot,line, ma, Model[i],Line[j],sn)
            
if 1:
    Line = ['Mg XII','C II','Fe XXV','Fe XXVI','O VII','Ne VIII','S IV','S IV*','Si III','C IV','C VI','O VI','He II','N V','O VIII','Si IV']
    Line = ['Si XIV 6']
    Doublets = ['Si XIV 6','Mg XII','C II','S IV','C IV','C VI','Fe XXVI','O VI','He II','N V','O VIII','Si IV']
    # trying to extract hydrofile from a folder
    # computing line profile for multiple snapshots
    # output will be stored in Output folder
    if 1: # for high res model A
        Model = 'Ax8'
        path = 'model_dumps/AGN1-HEP19-3e-1-es-hi-hires-x8/'
        lst1 = fnmatch.filter(os.listdir(path), 'agn1.out1.*')
        lst2 = fnmatch.filter(os.listdir(path), 'agn1.out2.*')  
    if 0: # for high res model B
        Model = 'Bx8'
        path = 'model_dumps/AGN1-HEP17-3e-1-es-hi-hires-x8/'
        lst1 = fnmatch.filter(os.listdir(path), 'agn1.merged.out1.*')
        lst2 = fnmatch.filter(os.listdir(path), 'agn1.merged.out2.*') 
    lst1.sort()
    lst2.sort()
    # computing LP for all lines including doublets
    if 0:
        for i in range(len(lst1)):
            snap = str(i).zfill(5)
            f1 = path+lst1[i]
            f2 = path+lst2[i]
            for j in range(len(Line)):
                fop, line, ma = gi.get_Line(Line[j])
                #print(f1,f2,fop,lines,matom,Model,Line,snap)
                lptst.LP_vel(f1,f2,fop,line, ma, Model,Line[j],snap)
    # computing composite LP for doublets or 2 lines
    if 1:
        for i in range(len(lst1)):
            snap = str(i).zfill(5)
            f1 = path+lst1[i]
            f2 = path+lst2[i]
            for j in range(len(Line)):
                fop, line, ma = gi.get_Line(Doublets[j])
                lptst.LP_freq(f1,f2,fop,line, ma, Model,Line[j],snap)
        
                