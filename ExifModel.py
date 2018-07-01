#!/usr/bin/env python
from __future__ import division
import PIL.Image
import exiftool
import PIL.ImageTk
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image, ImageTk



class Model:    

	def __init__(self): #initialize arrays
		self.images = []   #image 
		self.EXIFdata = []  #EXIF


	def loadImage(self,path):


		self.im = PIL.Image.open(path) #load the image 
		self.images.append(self.im)    #insert into the images array 
		return self.im


	def numberElements(self):  #return the number of elements of the images array


		self.numberElement = len(self.images)  
		return self.numberElement

		
	def getWidth(self,im): #return the width of an image


		return im.width


	def getHeight(self,im): #return the height of an image


		return im.height


	def getImageFromArray(self,index): #return the image of the array with the current index


		return self.images[index]



	def loadExif(self,path):   #load the EXIF


		files = [path]
		with exiftool.ExifTool() as self.et:
			self.metadata = self.et.get_metadata_batch(files)[0]
		self.EXIFdata.append(self.metadata)  #insert in EXIF array


	def getExifValue(self,indexImg,i):  #return the value of EXIF data


		return self.EXIFdata[indexImg][i]


	def getLatitude(self,IndexImg):   #if there is latitude,return it 


		for d in self.EXIFdata[IndexImg]:
			if d == "EXIF:GPSLatitude":
				return self.EXIFdata[IndexImg][d] 



	def getLongitude(self,IndexImg):  #if there is longitude,return it 

		
		for d in self.EXIFdata[IndexImg]:
			if d == "EXIF:GPSLongitude":
				return self.EXIFdata[IndexImg][d]














