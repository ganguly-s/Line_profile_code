#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 20:46:02 2020

@author: ganguly93
"""
import os
import fnmatch
import threading
import Queue
import time
import get_inp as gi
import line_profile_test_02 as lptst

num_threads = 25

q = Queue.Queue()

Model = ['Ax8', 'Bx8']
Line = ['Mg XII','Mg II','C II','Fe XXV','Fe XXVI','O VII','Ne VIII','S IV','S IV*','Si III','C IV','C VI','O VI','He II','N V','O VIII','Si IV','N VII','O VIII 15','O VIII 16','Ne X','S XVI 4','Ar XVIII','Si XIV 5','Si XIV 6']
Doublets = ['Si XIV 6','Si XIV 5','Mg XII','C II','S IV','C IV','C VI','Fe XXVI','O VI','He II','N V','O VIII','Si IV']

def worker():
    while True:
        q.get()
        lptst.LP_vel(q[0],)
        q.task_done()
        
for i in range(num_threads):
    t = threading.Thread(target=worker, daemon=True)
    t.start()

for mod in Model:
    lst = fnmatch.filter(os.listdir(gi.get_Model(mod)), '.out1.*')
    lst.sort()
    for sn in lst:
        for l in Line:
            q.put([mod, sn, l])
    
q.join()