from PIL import Image as im

import os
import glob
import numpy as np
import pdb
from pylab import gray
import cv2

def convertjpg(jpgfile, outdir, width=500, height=400):
    img = im.open(jpgfile).convert('L')
#     new_img = img.resize((width, height), im.BILINEAR)
    img1 = im.open('d:/image/img2.jpg').convert('L')
    
    gray()
    img.save(os.path.join(outdir, os.path.basename(jpgfile)))
    img1.save(os.path.join(outdir, os.path.basename('d:/image/bak/img2.jpg')))
    
    
def image_handle(input_dir, output_dir, jpgname):
    
    img = im.open(input_dir + jpgname + '.jpg').convert('L')
    img.save(output_dir + jpgname + '_gray.jpg')
    
    img = cv2.imread(output_dir + jpgname + '_gray.jpg')
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j][0] < 30:
                img[i][j] = 255
            else:
                img[i][j] = 0 
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    
    closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    
#     cv2.imwrite('d:/image/binary/img1.jpg', img)

    cv2.imshow('close', closed)
    cv2.imwrite(output_dir + jpgname + '.jpg', img)
    cv2.imwrite(output_dir + jpgname + '_close.jpg', closed)
    
    closed1 = im.open(output_dir + jpgname + '_close.jpg')
    
    box=(21,100,495,316)  
    closed1.crop(box).save(output_dir + jpgname + '_cut.jpg')  
    cut = im.open(output_dir + jpgname + '_cut.jpg')
    
    cutlst = []
    for i in range(4):    
#             for j in range(5):    
        box=(0,i*54,474,(i+1)*54)    
        cut.crop(box).save(output_dir + jpgname + '_cut_%d.jpg' % i)  
        cutlst.append(cv2.imread(output_dir + jpgname + '_cut_%d.jpg' % i))
        k=0  
#         pdb.set_trace()
        for m in range(0,54):  
            for mm in range(0,474):  
                if cutlst[i * 2][m][mm][0] < 100:  
                    k=k+1  
        cutlst.append(k)
    print cutlst[1::2]
    

if __name__ == '__main__':
    input = 'd:/image/'
    output = 'd:/image/output/'
    jpgname = 'img1'
    image_handle(input, output, jpgname)
    