import cv2
import imutils
import numpy as np
import math
import calibration as cal
import shape_detection as shape
import cv2.aruco as aruco

def zajem (cam):
	kalib_slika = cv2.imread('kalib_slika_koncna.png')
	video_capture = cv2.VideoCapture(cam)
	# Check success
	if not video_capture.isOpened():
		raise Exception("Could not open video device") #zajem slike!!
	# Read picture. ret === True on success
	ret, frame = video_capture.read()
	# Close device
	frame1 = cal.img_cal(kalib_slika,frame)
	aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
	parameters =  aruco.DetectorParameters_create()
	gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
	corners, ids, rejectedImgPoints = aruco.detectMarkers(gray1, aruco_dict, parameters=parameters)
	x1 = corners[0][0][0][0]
	x2 = corners[0][0][1][0]
	x3 = corners[0][0][2][0]
	x4 = corners[0][0][3][0]
	y1 = corners[0][0][0][1]
	y2 = corners[0][0][1][1]
	y3 = corners[0][0][2][1]
	y4 = corners[0][0][3][1]
	a = (x1+x2)/2
	b = (y1+y4)/2
	x = math.floor(a)
	y = math.floor(b)
	center_marker =[a,b]
	x_dist1 = (x2 - x1)/0.1
	x_dist2 = (x3 - x4)/0.1  # calculated distance between the marker corners
	y_dist1 = (y3 - y1)/0.1  # we know that the marker is 10x10 cm so we devide the 
	y_dist2 = (y4 - y2)/0.1  # pixles lenght with 10 to get how many pixles are in 1cm
	mask = 255*np.ones(frame1.shape, dtype = "uint8")
	cv2.rectangle(mask, (300, 0), (1000, 350), (0, 0, 0), -1)
	maskedImg = cv2.bitwise_or(frame1, mask) 
	gray = cv2.cvtColor(maskedImg, cv2.COLOR_BGR2GRAY)
	gray = -gray + 255
	blurred = cv2.GaussianBlur(gray, (15, 15), 0)
	thresh = cv2.threshold(blurred, 150, 255, cv2.THRESH_BINARY)[1]

	cnts= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cx = []
	cy= []
	shape1 =[]
	angle =[]
	# loop over the contours
	for c in cnts:
		# compute the center of the contour
		M = cv2.moments(c)
		if(M['m00']!=0):
			#find centroid
			cX = int(M['m10'] / M['m00'])
			cY = int(M['m01'] / M['m00'])


		else:
			cX,cY=0,0 
		cx.append(cX)
		cy.append(cY)
		shape1.append(shape.detect(c))
		cent,width,angle_ = cv2.minAreaRect(c)
		box = cv2.boxPoints((cent,width,angle_))
		box = np.int0(box)
		angle.append(angle_)
		cv2.drawContours(frame1,[box],0,(0,0,255),2)
		cv2.circle(frame1,(cX,cY),3,(255,255,255),-1)
		cent,width,angle = cv2.minAreaRect(c)
		box1 = np.int0(cv2.boxPoints((cent,width,angle)))
		cv2.drawContours(calibrated_img,[box1],0,(0,0,255),2)
		angles.append(angle)

	true_angles = []
	for i in range(len(angles)):
		angles1 = angles[i] + 90
		true_angles.append(angles1)


	cv2.circle(frame1,(x,y),3,(255,255,255),-1)		
	hsv = cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)

	distance = []
	vectors = []
	h = []
	s = []
	v = []
	colors = []
	object_shape = []
	found_object = []
	font = cv2.FONT_HERSHEY_SIMPLEX
	angles = []

	i = 0
	for i in range(len(cx)):
		# compute the centres, distances and vectors from the objects and the marker
		shapes = shape1[i]
		center = [cx[i],cy[i]]
		dist = (math.sqrt((center[0] - center_marker[0])**2+(center[1] - center_marker[1])**2))/y_dist1
		vector_x = (center[0] - center_marker[0])/y_dist1
		vector_y = (abs(center[1] - center_marker[1]))/y_dist1  ## y has to  be positive, because the y in the picture points downwards
		vector =[vector_x, vector_y]
		distance.append(dist)
		vectors.append(vector)
		h1 = hsv[cy[i],cx[i],0]
		s1 = hsv[cy[i],cx[i],1]
		v1 = hsv[cy[i],cx[i],2]
	# determine the shape of the recognized object
	if shapes == 'triangle':
		object_shape ='triangel'
		cv2.putText(frame,'triangle',(cx[i]+10,cy[i]+30), font, 0.5,(255,255,255),2,cv2.LINE_AA)
	elif shapes == 'square':
		cv2.putText(frame,'square',(cx[i]+10,cy[i]+30), font, 0.5,(255,255,255),2,cv2.LINE_AA)
		object_shape ='square'
	elif shapes == 'pentagon':
		cv2.putText(frame,'pentagon',(cx[i]+10,cy[i]+30), font, 0.5,(255,255,255),2,cv2.LINE_AA)
		object_shape == 'pentagon'
	elif shapes == 'hexagon':
		cv2.putText(frame,'hexagone',(cx[i]+10,cy[i]+30), font, 0.5,(255,255,255),2,cv2.LINE_AA)
		object_shape == 'hexagone'
	else: 
		object_shape == 'trapez'
		cv2.putText(frame,'trapez',(cx[i]+10,cy[i]+30), font, 0.5,(255,255,255),2,cv2.LINE_AA)

	# determine the color of the recognized object
	if ((h1<=80 and h1>= 40) and (s1<=255 and s1>= 180) and (v1<=100 and s1>= 45)):
		#print('barva jezelena')
		color = 'green'
		cv2.putText(frame,'green',(cx[i]+10,cy[i]+10), font, 0.5,(255,255,255),2,cv2.LINE_AA)
	elif((h1<=180 and h1>= 80) and (s1<=230 and s1>= 180) and (v1<=70 and s1>= 20)):
		#print('barva je modra')
		color = 'blue'
		cv2.putText(frame,'blue',(cx[i]+10,cy[i]+10), font, 0.5,(255,255,255),2,cv2.LINE_AA)
	elif((h1<=20 and h1>= 0) and (s1<=240 and s1>= 200) and (v1<=200 and s1>= 150)):
		#print('barva je oranžna')
		color = 'red'
		cv2.putText(frame,'red',(cx[i]+10,cy[i]+10), font, 0.5,(255,255,255),2,cv2.LINE_AA)
	else:
		#print('barva ni prepoznana')
		color = 'color not defined'
		cv2.putText(frame,'Not identified',(cx[i]+10,cy[i]+10), font, 0.5,(255,255,255),2,cv2.LINE_AA)
	colors.append(color)

	#object1 = color+ ' '+  object_shape
	#found_object.append(object1)
	cv2.imshow('',frame1)
	return(distance,vectors,true_angles)