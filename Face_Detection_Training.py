import os
import numpy
import PIL
import face_recognition
import mysql.connector  # Python native MySQL connector


mydb = mysql.connector.connect(host="10.0.0.207", user="root", password="", database="facerecon")




condb = mydb.cursor()
print(condb)
print(mydb)


filepath = input("Choose photos directory: ")
files = os.listdir(filepath)
files = [f for f in files if os.path.isfile(filepath + '/' + f)]


for item in files:
   fullimage = filepath + "/" + item
   tfname = fullimage + ".tdata"
   print(tfname)


   image = face_recognition.load_image_file(fullimage)
   print(item)
   try:
       image1_face_encoding = face_recognition.face_encodings(image)[0]
       print(image1_face_encoding)
       image_face_encoding_str = ','.join([str(codes) for codes in image1_face_encoding])
       print(image_face_encoding_str)


       insql = "INSERT INTO encodings (filename, imageencoding) VALUES (%s, %s)"
       vals_enc = (fullimage, image_face_encoding_str)
       condb.execute(insql, vals_enc)
       mydb.commit()
       print(image1_face_encoding)
   except Exception:
       continue