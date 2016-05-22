# -*- coding: utf-8 -*-  
from PIL import Image  
from pylab import imshow  
from pylab import show
import os  

  
pil_im = Image.open('d:/image/img2.jpg').convert('L')  
# gray()  
imshow(pil_im)  
show()  

pil_im.save('d:/image/bak/test.jpg')
