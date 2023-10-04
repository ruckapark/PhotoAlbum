# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 22:25:14 2023

@author: Admin
"""


import os
import numpy as np
import cv2

def find_mindim(images):
    
    #for square images
    mindim = 1000000
    for key in images:
        dim = images[key].shape[0]
        if dim < mindim: 
            mindim = dim    
    
    return mindim

def find_basedims(images,ratio = 4.8):
    
    mindim = find_mindim(images)
    height,width = int(mindim * (15/ratio)),int(mindim * (10/ratio))
    return mindim,height,width

def add_image(images,num):
    
    mindim,height,width = find_basedims(images)
    for l in images: images[l] = cv2.resize(images[l],(mindim,mindim)) #resize all images
    base = np.zeros((height,width,3), np.uint8)
    base.fill(255)
    
    #topleft corner coordinates
    x = {0:int((0.1/10)*width),1:int((5.1/10)*width)}
    y = {0:int((1/15)*height),1:int((8.5/15)*height)}
    for i,l in enumerate([*images]):
        row,col = i//2,i%2
        start_x,start_y = x[col],y[row]
        base[:, start_x:start_x+mindim][start_y:start_y+mindim] = images[l]
    
    return base                     
    

if __name__ == '__main__':
    
    files = [f for f in os.listdir() if 'spread' not in f]
    files = [f for f in files if 'Album' in f]
    
    pages = set([int(f.split('Album')[-1].split('.')[0][:-1]) for f in files])
    images = {}
    
    for i in range(max(pages)):
        
        for l in ['a','b','c','d']:
            
            images.update({l:cv2.imread('Album{}{}.jpg'.format(i+1,l))})
            
        baseimage = add_image(images,i)
        cv2.imwrite(r'polaroids/Album{}.jpg'.format(i+1),baseimage)