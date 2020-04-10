# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 13:56:27 2020

@author: Harshal
"""

import json
import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor, ImageFont


with open("test.json") as json_file:
    cvdict = json.load(json_file)
    
bucket="harshal-inferences-3"
photo="cable_sheath/cablepic1.png"
model='arn:aws:rekognition:us-east-1:340160437697:project/cable-duct-green-sheath/version/cable-duct-green-sheath.2020-04-03T09.48.14/1585877536653'
min_confidence=30




s3_connection = boto3.resource('s3')
s3_object = s3_connection.Object(bucket,photo)
s3_response = s3_object.get()
stream = io.BytesIO(s3_response['Body'].read())
image=Image.open(stream)

imgWidth, imgHeight = image.size
draw = ImageDraw.Draw(image)
   
# calculate and display bounding boxes for each detected custom label
print('Detected custom labels for ' + photo)
for customLabel in cvdict["CustomLabels"]:
    print('Label ' + str(customLabel['Name']))
    print('Confidence ' + str(customLabel['Confidence']))
    if 'Geometry' in customLabel:
        box = customLabel['Geometry']['BoundingBox']
        left = imgWidth * box['Left']
        top = imgHeight * box['Top']
        width = imgWidth * box['Width']
        height = imgHeight * box['Height']
   
        #fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 50)
        draw.text((left,top), customLabel['Name'], fill='#5d002e')
        print('Left: ' + '{0:.0f}'.format(left))
        print('Top: ' + '{0:.0f}'.format(top))
        print('Label Width: ' + "{0:.0f}".format(width))
        print('Label Height: ' + "{0:.0f}".format(height))
        points = (
        (left,top),
        (left + width, top),
        (left + width, top + height),
        (left , top + height),
        (left, top))
        draw.line(points, fill='#ff2290', width=2)
   
image.show()
