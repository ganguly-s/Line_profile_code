#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 20:46:02 2020

@author: ganguly93
"""
import os
import fnmatch
import threading
import queue
import time
import get_inp as gi
import line_profile_op as lptst

Model = ['Ax8', 'Bx8']
Line = ['Mg_XII','Si_XIV_6','Si_XIV_5','Fe_XXV','Fe_XXVI','O_VII','Ne_VIII','S_IV','S_IV*','Si_III','C_IV','C_VI','O_VI','He_II','N_V','O_VIII_19','Si_IV','N_VII','O_VIII_15','O_VIII_16','Ne_X','S_XVI_4','Ar_XVIII','Mg_II','C_II']
Line = ['Fe_XXV']
num_threads = 30

q = queue.Queue()

if 0:
	Model = 'Ax8'
	match  = '*.out1.00840.*'
	num_threads = len(Line)
if 0:
	Model = 'Bx8'
	match = '*.out1.*'
	num_threads = 30
start = time.time()
def worker():
	while True:
		val = q.get()
		lptst.LP_vel(val[0],val[1],val[2])
		q.task_done()
        
for i in range(num_threads):
	t = threading.Thread(target=worker, daemon=True)
	print(f"Begin executing thread {i}")
	t.start()

for mod in Model:
	lst = fnmatch.filter(os.listdir(gi.get_Model(mod)), '*.out1.*')
	#lst = fnmatch.filter(os.listdir(gi.get_Model(mod)), match)
	lst.sort()
	for i,sn in enumerate(lst):
		if i>1298 :
			for l in Line:
				q.put([mod, sn, l])
q.join()
print("Done executing thread")
finish = time.time()
print(f"DOne in {round(finish-start,2)} secs")
