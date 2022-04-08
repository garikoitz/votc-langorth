#!/bcbl/home/home_g-m/glerma/software/Anaconda/bin python
# -*- coding: UTF-8 -*-
# File    : PonerMarco.py
# Author  : Garikoitz Lerma-Usabiaga garikoitz@gmail.com
# Version : 0.2: added black line before the white frame, in FACES wasn't visible
# Date    : 12.Jan.2015
# Usage   : Call the function with 1 image from iPython and it will write an 
#           image called TASK_<originalimage>
#           
# Todo    : 1.-
#           2.-
#

# Actual function definition
def PonerMarco(ImgFileName, DEBUG):
    from PIL import Image
    Img = Image.open(ImgFileName)
    # Load required packages
    # Create a blank image with black background, this is what we will return
    Imgx = Img.size[0]
    Imgy = Img.size[1]
	
     # Crear una base negra
    BlackMarcoWidth = 1
    BMarcox = Imgx + BlackMarcoWidth*2
    BMarcoy = Imgy + BlackMarcoWidth*2
    BImgBlank = Image.new("RGB", (BMarcox, BMarcoy), "black")

    # Crear la imagen blanca
    WhiteMarcoWidth = 3
    Marcox = Imgx + (BlackMarcoWidth + WhiteMarcoWidth) * 2
    Marcoy = Imgy + (BlackMarcoWidth + WhiteMarcoWidth) * 2
    ImgBlank = Image.new("RGB", (Marcox, Marcoy), "black") # now that the image
    # are grey the marco is going to be black 

    # Paste black image to white background
    ImgBlank.paste(BImgBlank, (WhiteMarcoWidth, WhiteMarcoWidth))	

    # Paste image to final image
    ImgBlank.paste(Img, 
				  ((BlackMarcoWidth + WhiteMarcoWidth), 
				   (BlackMarcoWidth + WhiteMarcoWidth)))
    # pre = ImgFileName[0:2]
    # izena = 'TASK_' + pre + ImgFileName[6:len(ImgFileName)]
    izena = 'TASK_' + ImgFileName
    if DEBUG:
        print(izena)
    else:
        ImgBlank.save(izena)	
    
    return True


