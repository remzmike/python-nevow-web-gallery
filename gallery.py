from __future__ import division
import os, os.path
from md5 import md5
import mx.DateTime
import urllib2
from ctypes import *

class GalleryImage:

  def __init__(self,section,filename,no):
    self.no = no
    self.name = filename
    self.section = section
    self.filename = filename
    self.path = os.path.join(section.path,self.filename)
    self.desc = None
    self.descpath = self.path[:-4]+'.txt'

  def loaddesc(self):
    if os.path.isfile(self.descpath):
      self.desc = file(self.descpath,'r').read()

  def getthumbfilename(self):
    inputfile = 'D:/Web/galleria/media/gallery/'+self.section.dirname+'/'+self.filename
    outputfilename = 'py'+md5('PyImageCR3_'+inputfile).hexdigest()+'.jpg'
    outputfile = 'D:/Web/galleria/thumbs/'+outputfilename
    if not os.path.isfile(outputfile):
      cr3 = cdll.ImageCR3
      cr3.ImageCR_Startup()
      img = cr3.ImageCR_New()
      cr3.ImageCR_Load(img,inputfile)
      width = cr3.ImageCR_GetWidth(img)
      height = cr3.ImageCR_GetHeight(img)    
      if width > height:
        y = 100
        x = int(round(width*(y/height)))
      else:
        x = 100
        y = int(round(height*(x/width)))
      cr3.ImageCR_Sharpen(img,0,1)            
      cr3.ImageCR_Resize(img,x,y,c_int(13),c_double(1.0))      
      cr3.ImageCR_AutoContrast(img)
      cr3.ImageCR_Strip(img)
      cx = int(round(x/2-100/2))
      cy = int(round(y/2-100/2))
      cr3.ImageCR_Crop(img,cx,cy,100,100)
      cr3.ImageCR_SetQuality(img,87)
      cr3.ImageCR_Save(img,outputfile)
      cr3.ImageCR_Free(img)
      cr3.ImageCR_Shutdown()
    return outputfilename

  # image is 'fixed' if need be before returning link to it, not to exceed 500 px wide
  def getfixedlink(self):
    inputfile = 'D:/Web/galleria/media/gallery/'+self.section.dirname+'/'+self.filename
    outputfilename = 'py'+md5('PyImageCR3_'+inputfile).hexdigest()+'.jpg'
    outputfile = 'D:/Web/galleria/cache/'+outputfilename

    if os.path.isfile(outputfile):
      result = '/cache/'+outputfilename
    else:
      cr3 = cdll.ImageCR3
      cr3.ImageCR_Startup()
      img = cr3.ImageCR_New()
      cr3.ImageCR_Load(img,inputfile)
      width = cr3.ImageCR_GetWidth(img)
      height = cr3.ImageCR_GetHeight(img)    
      
      if width>500:
        result = '/cache/'+outputfilename
        x = 500
        y = int(round(height*(x/width)))
        cr3.ImageCR_Resize(img,x,y,c_int(13),c_double(1.0))
        cr3.ImageCR_SetQuality(img,87)
        cr3.ImageCR_Save(img,outputfile)
      else:
        result = self.getoriginallink()

      cr3.ImageCR_Free(img)
      cr3.ImageCR_Shutdown()
    return result
    
  def getoriginallink(self):
    return '/photos/'+self.section.dirname+'/'+self.filename        

class GallerySection:
  def __init__(self,gallery,dirname,no):
    self.no = no
    splat = dirname.split('^')
    self.name = splat[1]
    self.date = mx.DateTime.DateFrom(splat[0])      
    self.gallery = gallery
    self.dirname = dirname
    self.path = os.path.join(gallery.path,self.dirname)
    self.desc = None
    self.descpath = os.path.join(self.path,'!.txt')
    self.imageextensions = ['jpg','jpeg','gif','png']
    self.images = None
  def loaddesc(self):
    if os.path.isfile(self.descpath):
      self.desc = file(self.descpath,'r').read()
    else:
      self.desc = 'No description.'
  def loadimages(self):
    self.images = []
    imagedir = os.listdir(self.path)
    i = 0
    for filename in imagedir:
      fileextension = filename.split('.')[-1]
      if fileextension in self.imageextensions:        
        i = i + 1
        self.images.append(GalleryImage(self,filename,i))        
  
class Gallery:
  def __init__(self,dirname):
    self.dirname = dirname
    self.path = self.dirname
    self.sections = None
  def loadsections(self):
    self.sections = []
    sectiondirs = os.listdir(self.path)    
    i = 0
    for sectiondir in sectiondirs:      
      i = i + 1
      self.sections.append(GallerySection(self,sectiondir,i))      
      