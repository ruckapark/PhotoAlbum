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
        dim = max(images[key].shape[0],images[key].shape[1])
        if dim < mindim: 
            mindim = dim    
    
    if len(images) == 1:
        return images[key].shape[:2]
    else:
        return mindim

def find_basedims(images):
    
    #based on 3:2
    mindim = find_mindim(images)
    ratio = 2.2
    
    if len(images) == 1:
        dim = max(mindim)
        height,width = int(dim),int(dim*(2/3))
        
    elif len(images) == 2:
        height = int(ratio*mindim)
        width = int(height*2/3)
        
    elif len(images) == 3:
        width = int(mindim * 1.5*ratio)
        height = int(width*2/3)
        
    elif len(images) == 4:
        width = int(mindim * ratio)
        height = int(1.5*width)
        
    else:
        print('Not coded yet')
        
    return mindim,height,width

def add_image(images,num):
    
    mindim,height,width = find_basedims(images)
    if len(images) > 1:
        for l in images: images[l] = cv2.resize(images[l],(mindim,mindim)) #resize all images
    base = np.zeros((height,width,3), np.uint8)
    base.fill(255)
    
    #topleft corner coordinates
    if len(images) == 1:
        start_x,start_y = int((width - min(mindim))/2),0
        for i,l in enumerate([*images]):
            base[:, start_x:start_x+min(mindim)][start_y:start_y+height] = images[l]
        
    elif len(images) == 2:
        margin_x = int((width - mindim)/2)
        margin_y = int(((height/2) - mindim)/2)
        
        start_x = margin_x
        y = {0:int(margin_y),1:int((height/2) + margin_y)}
        
        for i,l in enumerate([*images]):
            row = i
            start_y = y[row]
            base[:, start_x:start_x+mindim][start_y:start_y+mindim] = images[l]
            
    elif len(images) == 3:
        margin_x = int(((width/3) - mindim)/2)
        margin_y = int((height-mindim)/2)
        
        x = {0:margin_x,1:int(width/3)+margin_x,2:int(2*width/3)+margin_x}
        start_y = margin_y
        
        for i,l in enumerate([*images]):
            col = i
            start_x = x[col]
            base[:, start_x:start_x+mindim][start_y:start_y+mindim] = images[l]
    
    elif len(images) == 4:
        x = {0:int((0.1/10)*width),1:int((5.1/10)*width)}
        y = {0:int((1/15)*height),1:int((8.5/15)*height)}
        for i,l in enumerate([*images]):
            row,col = i//2,i%2
            start_x,start_y = x[col],y[row]
            base[:, start_x:start_x+mindim][start_y:start_y+mindim] = images[l]
    
    return base                     
    

if __name__ == '__main__':
    
    root = r'C:\Users\Admin\Pictures\Cagnotte Auréline Lalouette\finals'
    os.chdir(root)
    
    files = [f for f in os.listdir() if 'spread' not in f]
    files = [f for f in files if 'Album' in f]
    
    pages = set([int(f.split('Album')[-1].split('.')[0][:-1]) for f in files])
    pages = list(pages)
    images = {}
    
    for i,n in enumerate(pages):
        
        letters = ['a','b','c','d','e','f']
        photos = []
        images = {}
        for f in files:
            for l in letters:
                if 'Album{}{}'.format(n,l) in f: photos.append(f)
        
        for x,l in enumerate(letters[:len(photos)]):
            
            images.update({l:cv2.imread('{}'.format(photos[x]))})
            
        baseimage = add_image(images,n)
        cv2.imwrite(r'polaroids/Album{}.jpg'.format(n),baseimage)