# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:25:14 2023

@author: Admin
"""


import os
import cv2

def add_image(base,image,pos):
    
    pos 0,1,2,3
    
    add to base image
    

if __name__ == '__main__':
    
    files = [f for f in os.listdir() if 'spread' not in f]
    files = [f for f in files if 'Album' in f]
    
    pages = set([int(f.split('Album')[-1].split('.')[0][:-1]) for f in files])
    
    for i in range(max(baseimage)):
        
        baseimage = ?? 10*15 blank white image
        
        for j,l in enumerate(['a','b','c','d']):
            
            baseimage = add_image(baseimage,cv2.readimage('Album{}{}.jpg'.format(i+1,l)),j)
            
        baseimage.write(r'polaroids/Album{}.jpg'.format(i+1))