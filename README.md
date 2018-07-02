# Image-EXIF-Viewer
Project for the exam of Human Computer Interaction. The Image-EXIF Viewer implements the following features:
* Support JPEG images
* Rescaling
* Left and right rotation (90°)
* EXIF data extractor and viewer
* GPS Tags (if they are present in the image)
* Geolocalization: Allow to see the position on Google Maps
* View multiple images

```MainView``` consists of menu bar where the user can upload an image,rotate it on the left/right by 90°,get EXIF data and slide to next/previous image using several buttons. In particular,the button related to EXIF opens a new window where all  data extracted in ```ExifModel``` are placed in a table. If are presents both latitude and longitude in data, a button appears on the bottom of table that sends a HTTP request to Google Maps for geolocalization. For loading multiple images, the user has to reclick the button "Load Image" and select another one. All the images are inserted into an array in ```ExifModel```; the buttons with left/right arrow slide the array and allow the user to visualize previous and next images.


![Mockup](/mockup/mockup.png)

## Prerequisites
The software requires:

* Python 2.7
* Tkinter
* Pillow(PIL fork)
* PyExifTool

## Implementation
Image-EXIF Viewer was implemented using Python and pattern MVC. Tkinter was used for developing the GUI, and with several elements (```Button```,```Table```) allows the behaviours previously described.

## Functionalities
The program can be launched from the ```MainView.py``` script:


```$ python MainView.py```

## Possible Improvements
Any possible improvements to Image-EXIF Viewer could be:
* Instead to send an HTTP request for geolocalization,open a new frame with maps widget
* improve the resizing methods, because of rare anomalies during image rotation

