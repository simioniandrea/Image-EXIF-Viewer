# Image-EXIF-Viewer
Project for the exam of Human Computer Interaction. The Image-EXIF Viewer implements the following features:
* Support JPEG images
* Rescaling
* Left and right rotation (90°)
* EXIF data extractor and viewer
* GPS Tags (if they are present in the image)
* Geolocalization: Allow to see the position on Google Maps
* View multiple images

```MainView``` consists of menu bar where the user can upload an image,rotate it on the left/right,get EXIF data and slide to next previous/image through several buttons. In particular,the button related to EXIF opens a new window where all extracted data are placed in a table. If there are presents both latitude and longitude in data,a button appears on the bottom of table that sends a HTTP request to Google Maps 



