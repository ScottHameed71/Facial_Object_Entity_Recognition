import face_recognition    #face recognition library using dlib' recognition system
import cv2    #The cv2 version of the OpenCV library whiich includes the NumPy support
import numpy as np    #Library for advancced n-dimensional array object and related math functions
import mysql.connector    #Python native MySQL connector
mydb = mysql.connector.connect(host="10.0.0.207", user="root", password="", database="facerecon") # initiating MySQL connection
con = mydb.cursor()


video_capture = cv2.VideoCapture(0) #intiates the first webcam for video capture


vsql = "select * from encodings"
con.execute(vsql)
rs = con.fetchall()
known_face_encodings = []
known_face_names = []


for i,x in enumerate(rs):
   known_face_encodings.append([float(y) for y in x[2].split(",")])
   known_face_names.append(x[1])


face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


while True:
   ret, frame = video_capture.read()    #read the video frame


   if process_this_frame:     #converting the frame size and then determining the location & encoding values
       small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)    #reduces the size to 25% of the original
       rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB) #code added to create compatibility for Mac

       #rgb_small_frame = small_frame[:, :, ::-1] #code previously in the Ubuntu sysem and worked perfectly but has been replaced with line immediately above for Mac compatbility


       face_locations = face_recognition.face_locations(rgb_small_frame)    #creates an array listing the co-ordinates of each face
       face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)     #captures a universal encoding of a face that can then be comparad to a face contained in any othher image


       face_names = []
       for face_encoding in face_encodings:
           matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
           #print(face_encoding)
           name = "Unknown"
           face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
           best_match_index = np.argmin(face_distances)
           if matches[best_match_index]:
               name = known_face_names[best_match_index]


           face_names.append(name)
   process_this_frame = not process_this_frame


   for (top, right, bottom, left), name in zip(face_locations, face_names):


       top *= 4
       right *= 4
       bottom *= 4
       left *= 4


       cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)


       cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
       font = cv2.FONT_HERSHEY_DUPLEX
       cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


   cv2.imshow('Video', frame)


   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


video_capture.release()
cv2.destroyAllWindows()