#!/usr/bin/env python
from __future__ import division
import PIL.Image
import exiftool
import PIL.ImageTk
import tkMessageBox
from PIL.ExifTags import TAGS, GPSTAGS
from PIL import Image, ImageTk
from Tkinter import * 
import Tkinter as tk
import tkFileDialog as filedialog
from tktable import *
import webbrowser
import ttk
from MODEL import Model

class App(Frame):
    model = Model()  
    exif_window_open = False
    indexCurrentImage = 0
    
    #Attributes:
        #model         reference to an object of class MODEL

    def chg_image(self):     #change the image of the label


        if self.im.mode == "1": # bitmap image
            self.img = PIL.ImageTk.BitmapImage(self.im2, highlightbackground= "white", background = "white")   
        else:              # photo image
            self.img = PIL.ImageTk.PhotoImage(self.im2)
        self.la.configure(image=self.img, bg="#000000",
            width=self.img.width(), height=self.img.height(),highlightbackground= "white",background = "white")

        

         
    def open(self):  #open and load an image 


        filename = filedialog.askopenfilename() #open dialog window to select the path of the image
        if filename != "":
            try:

                self.im = self.model.loadImage(filename)   #Load an image
                self.W =  self.model.getWidth(self.im)     #image width
                self.H =  self.model.getHeight(self.im)    #image height
                self.R = self.W/self.H                     #image ratio
                self.first_resize() 
                self.model.loadExif(filename)               #load EXIF of image
                self.img_copy= self.im2.copy()              #create copy for resize
                self.chg_image()

                if self.resized == True:                     #if true resize the new image with the parameters of the last image
                    self.resize(self.W2,self.H2)

                self.image = self.im2                         #initialize 
                self.NumberofElements = self.model.numberElements()   #load the number of elements of the images array
                self.indexCurrentImage = self.NumberofElements - 1    #set the index of the image
                self.Rotazione = 0 #reset the rotation
                self.la.pack_propagate(flag = True)

            except IOError:
                tkMessageBox.showerror("Error","File is not an image!")



    def first_resize(self): #resizes the loaded image so that height and length do not exceed 512


        self.master.minsize(700,350) #set the minimum dimension of the frame

        if self.W < 512 and self.H < 512:  #control if the image exceed 512 in width and height or not 

            self.im2 = self.im   #initialize 

        else:

            if self.R>1: #image with width>height

                self.W = 512
                self.H = 512/self.R 
                self.im2= self.im.resize((self.W,int(self.H)),PIL.Image.ANTIALIAS)

            else:   #image with width<=height

                self.H = 512
                self.W = self.R*self.H
                self.im2= self.im.resize((int(self.W),self.H),PIL.Image.ANTIALIAS) 

        

    def _resize_image(self,event): #calls the method resize if there have been changes in frame rescaling 


        self.resize(event.width, event.height)


    def resize(self,w, h): #resize the image based on the length w and height h values



        if self.im2 != None: 

            new_width = w   #set new_width 
            new_height = h  #set new_height
            self.resized = True

            if new_width < self.W:   # new_width is less than current width (horizontal case)
   
                self.H = min(512,int(new_width/self.R))  #min to not exceed 512,recalculation of current height
                self.W = int(new_width)  # current width becomes new_width
                
                if self.H > new_height:  #after the new assignment current height is greater than new_height 

                    self.H1 = min(512,new_height)
                    self.image = self.img_copy.resize((min(512,int(self.H1*self.R)),int(self.H1)),PIL.Image.ANTIALIAS) #recalculation of weight and height and resize
                    self.la_image = ImageTk.PhotoImage(self.image) 

                else:

                    self.image = self.img_copy.resize((self.W, self.H),PIL.Image.ANTIALIAS) #resize
                    self.la_image = ImageTk.PhotoImage(self.image)
            

            else:                        #vertical case
   
                self.W =  min(512,int(new_height*self.R)) #recalculation

                if self.W > new_width:  #after the new assignment current width is greater than new_width 

                    self.W1 = min(512,new_width)
                    self.image = self.img_copy.resize((int(self.W1), min(512,int(self.W1/self.R))),PIL.Image.ANTIALIAS)  #recalculation of weight and height and resize
                    self.la_image = ImageTk.PhotoImage(self.image)

                
                else: 
                  
                    self.H = min(512,int(new_height))   #current height becomes new_height
                    self.image = self.img_copy.resize((self.W, self.H),PIL.Image.ANTIALIAS)   #resize
                    self.la_image = ImageTk.PhotoImage(self.image)
            

            self.la.configure(image = self.la_image,highlightbackground= "white",background = "white")
            self.W2 = self.W   #value of last width 
            self.H2 = self.H   #value of last height
            
            

    def seek_prev(self): #if multiple images are loaded,load the previous image to the current one


        if self.indexCurrentImage > 0:   #control if there are at least 2 image and/or current index isn't of the first image loaded (index == 0)
            self.indexCurrentImage = self.indexCurrentImage - 1   #set the current index with the previous one
            self.im = self.model.getImageFromArray(self.indexCurrentImage)   #load the image with the new current index (previous image)
            self.W = self.model.getWidth(self.im)   #get width 
            self.H = self.model.getHeight(self.im)   #get height 
            self.R = self.W/self.H   #ratio
            self.first_resize()  
            self.img_copy= self.im2.copy() 
            self.chg_image()
            self.Rotazione = 0   #reset rotation
            self.resize(self.W2,self.H2) #resize with the last values of width and height

        else:

            tkMessageBox.showerror("Error","No previous image!")


    def seek_next(self): #if multiple images are loaded,load the next image to the current one


        if self.im2 != None and self.indexCurrentImage < self.NumberofElements -1:   #control if the current index isn't of the last image loaded
            self.indexCurrentImage = self.indexCurrentImage + 1   #set the current index with the next one
            self.im = self.model.getImageFromArray(self.indexCurrentImage)   #load the image with the new current index (next image)
            self.W = self.model.getWidth(self.im)   #get width
            self.H = self.model.getHeight(self.im)  #get height 
            self.R = self.W/self.H   #ratio
            self.first_resize()
            self.img_copy= self.im2.copy()
            self.chg_image()
            self.Rotazione = 0 #reset rotation
            self.resize(self.W2,self.H2) #resize with the last values of width and height

        else:

            tkMessageBox.showerror("Error","Load an image first!")


    def RotateR(self): #right rotate

        if self.im2 != None:

            self.effectiveRotate("right")  #effective rotation
            self.resize(self.W, self.H) #resize rotated image

        else:

            tkMessageBox.showerror("Error","Load an image first!")


    def RotateL(self): #left rotate

        if self.im2 != None:

            self.effectiveRotate("left") #effective rotation
            self.resize(self.W, self.H)  #resize rotated image

        else:

            tkMessageBox.showerror("Error","Load an image first!")


    def effectiveRotate(self,RDirection): #depending of RDirection parameter, rotate right or left of 90 degrees


        if RDirection == "right":
            self.Rotazione -= 90 
        elif RDirection == "left":
            self.Rotazione +=90
        self.R = 1/self.R #invert the ratio for maintaining the right proportions
        self.img2 = self.im2.rotate(self.Rotazione, expand = True) #rotation
        self.img_copy= self.img2.copy()
        self.img2 = PIL.ImageTk.PhotoImage(self.img2)
        self.la.configure(image=self.img2, height = self.img2.height(),width = self.img2.width())
        self.rotated = True


    def on_closing(self): #close EXIF window 


        self.exif_window_open = False
        self.window.destroy()


    def GetExif(self):  #load the EXIF data of the current image, and put all of them in a table;
                        #if there are also GPS data, a button on window opens Google Maps to see the position 

        if self.im2 != None:

            if not self.exif_window_open:

                self.exif_window_open = not self.exif_window_open
            else:
                return 

            self.window = tk.Toplevel(self.fram) #create a new window
            self.window.resizable(False,False) 
            self.window.title("Exif Viewer")
            self.table = Table(self.window, ["Number","Type", "Result"], column_minwidths=[100,100,100]) #create a table https://github.com/nbro/tktable
            self.window.protocol('WM_DELETE_WINDOW',self.on_closing) #protocol on closing 

            c = 0
            for d in self.model.EXIFdata[self.indexCurrentImage]: 
                self.table.insert_row([c,d,self.model.getExifValue(self.indexCurrentImage,d)]) #insert EXIF data in the table: first column represent the number of exifdata,
                c += 1                                                                         #second the type and the third the respective value 
            self.table.pack(padx=10,pady=10)


            self.Latitude = self.model.getLatitude(self.indexCurrentImage) #if there is latitude between the data, load it
            self.Longitude = self.model.getLongitude(self.indexCurrentImage) #if there is longitude between the data,load it

            if self.Latitude != None and self.Longitude != None:        #if both latitude and longitude are present,show the button for Google Maps

                pathIcon = "images/iconMaps.png"
                self.icon = PIL.Image.open(pathIcon)
                self.icon = self.icon.resize((50,50))
                self.imgIcon = PIL.ImageTk.PhotoImage(self.icon)
                b = Button(self.window,command = self.Position) #button
                b.config(text= "Go to position",image= self.imgIcon,compound="left")
                b.pack()
        else:

            tkMessageBox.showerror("Error","Load an image first!")


    def Position(self): #open the default browser with Latitude and Longitude values in URL

        webbrowser.open_new('https://maps.google.com/?q='+str(self.Latitude)+','+str(self.Longitude))
    

    def __init__(self, master=None): #initialize variables,create main frame and label


        Frame.__init__(self, master)
        self.master.title('Image Viewer')
        s=ttk.Style()
        s.theme_use('alt')
        self.Rotazione = 0
        self.master.minsize(750,50)  #minimum size of the frame to see only the bar initially
        self.master.maxsize(900,700) #maximum size of the frame
        self.Latitude = None
        self.Longitude = None
        self.image_first = False
        self.resized = False
        self.fram = Frame(self)

        #button icons 
        pathImgIcon = "images/imageLogo.png"
        pathLeftIcon = "images/LeftLogo.png"
        pathRightIcon = "images/RightLogo.png"
        PathRotateRIcon = "images/rotateRightLogo.png"
        PathRotateLIcon = "images/rotateLeftLogo.png"
        PathExifIcon = "images/exif.png"

        #load and resize icons
        self.Photoicon = PIL.Image.open(pathImgIcon)
        self.Photoicon = self.Photoicon.resize((60,60),PIL.Image.ANTIALIAS)
        self.PhotoLeftIcon = PIL.Image.open(pathLeftIcon)
        self.PhotoLeftIcon = self.PhotoLeftIcon.resize((60,60))
        self.PhotoRightIcon = PIL.Image.open(pathRightIcon)
        self.PhotoRightIcon = self.PhotoRightIcon.resize((60,60),PIL.Image.ANTIALIAS)
        self.PhotoRotateRIcon = PIL.Image.open(PathRotateRIcon)
        self.PhotoRotateRIcon = self.PhotoRotateRIcon.resize((60,60))
        self.PhotoRotateLIcon = PIL.Image.open(PathRotateLIcon)
        self.PhotoRotateLIcon = self.PhotoRotateLIcon.resize((60,60))
        self.EXIFicon = PIL.Image.open(PathExifIcon)
        self.EXIFicon = self.EXIFicon.resize((60,60))


        self.imgPhotoIcon = PIL.ImageTk.PhotoImage(self.Photoicon)
        self.imgPhotoLeftIcon = PIL.ImageTk.PhotoImage(self.PhotoLeftIcon)
        self.imgPhotoRightIcon = PIL.ImageTk.PhotoImage(self.PhotoRightIcon)
        self.imgPhotoRotateRIcon = PIL.ImageTk.PhotoImage(self.PhotoRotateRIcon)
        self.imgPhotoRotateLIcon = PIL.ImageTk.PhotoImage(self.PhotoRotateLIcon)
        self.imgEXIFIcon = PIL.ImageTk.PhotoImage(self.EXIFicon)

        #create buttons
        imgB = Button(self.fram,command=self.open)
        imgB.config(text= "Load Image",image= self.imgPhotoIcon, compound="left")
        imgB.pack(side = LEFT)

        LeftB = Button(self.fram,command=self.seek_prev)
        LeftB.config(image= self.imgPhotoLeftIcon, compound="left")
        LeftB.pack(side = LEFT)

        RightB = Button(self.fram,command=self.seek_next)
        RightB.config(image= self.imgPhotoRightIcon, compound="right")
        RightB.pack(side = LEFT)

        LeftRotateB = Button(self.fram,command=self.RotateL)
        LeftRotateB.config(text= "RotateL",image= self.imgPhotoRotateLIcon, compound="left")
        LeftRotateB.pack(side = LEFT)

        RightRotateB = Button(self.fram,command= self.RotateR)
        RightRotateB.config(text= "RotateR",image= self.imgPhotoRotateRIcon, compound="right")
        RightRotateB.pack(side = LEFT)

        EXIFB = Button(self.fram,command=self.GetExif)
        EXIFB.config(text = "get EXIF", image = self.imgEXIFIcon,compound = "left")
        EXIFB.pack(side = LEFT)


        Label(self.fram).pack(side=LEFT)
        self.fram.pack(side=TOP, fill=BOTH)
        self.im2 = None
        self.la_image = None
        self.la = Label(self)
        self.la.pack(fill=BOTH, expand=YES)
        self.la.bind('<Configure>', self._resize_image) 
        self.pack()
    

if __name__ == "__main__":
    app = App(); app.mainloop()