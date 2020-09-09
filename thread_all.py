#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 20:46:02 2020

@author: ganguly93
"""
import os
from fnmatch import filter
from threading import Thread
from queue import Queue
from time import time
import get_inp as gi
import line_profile_op as lptst
from multiprocessing.pool import Pool

num_threads = 1

q = Queue()

Model = ['Ax8', 'Bx8']
Line = ['Mg XII','Mg II','C II','Fe XXV','Fe XXVI','O VII','Ne VIII','S IV','S IV*','Si III','C IV','C VI','O VI','He II','N V','O VIII','Si IV','N VII','O VIII 15','O VIII 16','Ne X','S XVI 4','Ar XVIII','Si XIV 5','Si XIV 6']
Doublets = ['Si_XIV 6','Si_XIV 5','Mg_XII','C_II','S_IV','C_IV','C_VI','Fe_XXVI','O_VI','He_II','N_V','O_VIII_19','Si_IV']
Line = ['C_IV']
start = time()
#lptst.LP_calc('Ax8','agn1.out1.00000.tab','C_IV')
#lptst.LP_calc('Ax8','agn1.out1.00001.tab','C_IV')

def worker():
	while True:
		val = q.get()
		lptst.LP_calc_1D(val[0],val[1],val[2])
		q.task_done()
        
for i in range(num_threads):
	t = Thread(target=worker, daemon=True)
	t.start()

for mod in Model:
	lst = filter(os.listdir(gi.get_Model(mod)), '*.out1.*')
	lst.sort()
	for i,sn in enumerate(lst):
		for l in Line:
			q.put([mod, sn, l])
		#if i==1:
		break
	break

q.join()

finish = time()
print(f"DOne in {round(finish-start,2)} seconds")

