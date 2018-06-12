#!/usr/bin/python
import os
import signal
import pygame, sys
import kairos_face
import MySQLdb
from pygame.locals import *
import pygame.camera
width = 640
height = 480

from google.cloud import storage
import RPi.GPIO as GPIO
import time
import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor

#Connect to Database
print "Initializing . . ."
try:
    print "Connecting to database"
    #Connect to Google MySql
    dbconn = MySQLdb.connect("address","username","password","database_name")
    print "Connected to cloud database"
except:
    print "Can not connect to Database"
    print "Terminated program"
    dbconn.close()
    exit()
cursor = dbconn.cursor()
#Set up API key
kairos_face.settings.app_id = 'kairos_app_id'
kairos_face.settings.app_key = 'kairos_app_key'
print "Set up Kairos face API key"

#Set up Google Storage
storage_client = storage.Client()
print "Connected to cloud storage"

print "Initializing completed!"

try:
    while True:
        i=GPIO.input(11)
        if i==0:                 #When output from motion sensor is LOW
            print "No intruders",i
            time.sleep(5)
        elif i==1:               #When output from motion sensor is HIGH         
            #initialise pygame
            pygame.init()
            pygame.camera.init()
            cam = pygame.camera.Camera("/dev/video0",(width,height))
            cam.start()
             
            #setup window
            windowSurfaceObj = pygame.display.set_mode((width,height),1,16)
            pygame.display.set_caption('Camera')
            
            print "Intruder detected",i
            #time.sleep(2)
                 
            #recent time
            d = datetime.datetime.now()
            rd = d.strftime("%Y-%m-%d %I:%M:%S %p")
            print (rd)
             
            #take a picture
            print "Taking picture"
            image = cam.get_image()
            cam.stop()
             
            #display the picture
            print "display picture"
            catSurfaceObj = image
            windowSurfaceObj.blit(catSurfaceObj,(0,0))
            pygame.display.update()
	    time.sleep(2)
	    
            #save picture
	    print "saving photo"
            pygame.image.save(windowSurfaceObj,rd+'.jpg')
            print "save complete"
             
            #Upload image to storage
            bucket = storage_client.get_bucket('google_storage_name')
            blob = bucket.blob(rd + '.jpg')
            blob.upload_from_filename('/home/pi/Desktop/' + rd + '.jpg' ,content_type='image/jpg')
            #make image public
            blob.make_public()
            img_link = "storage.googleapis.com/google_storage_name/" + rd + ".jpg"
             
            #Recognition (if error, than enroll)(if yes, run mySQL find the same face_id + 1)
            image_file = '/home/pi/Desktop/' + rd + '.jpg'
            print image_file
            try:
                print "Recognizing . . ."
                recognized_face = kairos_face.recognize_face(file=image_file ,gallery_name='b-gallery')
                myface_id = recognized_face[u'images'][0][u'candidates'][0][u'face_id']
                print "Face_id: " ,myface_id
                #cursor.execute("INSERT INTO customerData (face_id, link, counting) VALUES ('lol', 'why', 1)")
                cursor.execute("UPDATE customerData SET counting = counting + 1 ,link = %s WHERE face_id = %s", (img_link, myface_id,))
                dbconn.commit()
                print "Recognize complete, counting has been updated"
            except:
            #Enroll face
                try:
                    print "Enrolling face . . ."
                    result = kairos_face.enroll_face(file=image_file, subject_id= rd + '.jpg', gallery_name='b-gallery')
                    myface_id = result[u'face_id'] 
                    print "Face_id: " ,myface_id
                    cursor.execute("INSERT INTO customerData (face_id, link, counting) VALUES (%s, %s, 1)", (myface_id, img_link,))
                    dbconn.commit()
                    print "Enroll complete, data has been inserted"
                    #break
                except :
                    print 'ERROR No Face No Face!'
                    os.remove(image_file)
                    blob.delete()
                    
            #Sleep
            print "Sleep for 20 secs"
            time.sleep(20)
            
except KeyboardInterrupt:
    print "Exit"
    cursor.close()
    dbconn.close()
