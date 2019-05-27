import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import math
import aruco_marker_koncna as marker
import obdelava_koncna as obdelava

stanje =1
while(1): #neskončna zanka ki preverja stanje naloge
	
	if(stanje == 1): # v stanju iskanja aruco markerja in premika na začetno pozicijo
		print('Stanje je ',stanje)
		center = marker.marker(0)
		print('Center markerja je ',center)


	elif(stanje == 2): # robot postavljen na začetni poziciji (zajem in obdelava slike)
		print('Stanje je ',stanje)
		#center= marker.marker(0)
		razdalja,vektorji,kot = obdelava.zajem(0)
		i = 0
		for i in range(len(razdalja)): 
			
		#vals = (vektorji[0][0],vektorji[0][1],vektorji[1][0],vektorji[1][1],vektorji[2][0],vektorji[2][1],razdalja[0],razdalja[1],razdalja[2])
			vals = (vektorji[i][0],vektorji[i][1], kot[i])
			marker.send_vals(vals,'f f f', 55454)
			center = marker.marker(0)
			razdalja,vektorji,kot = obdelava.zajem(0)
			
			
			print('Razdalje so: ',razdalja)
			print('Vektorji so: ',vektorji)
			print('Koti so: ',kot)
	elif(stanje == 3): # robot pobral objek iskanje aruko markerja in premik na končno točko 
		print('Stanje je ',stanje)
		print('Zaključil z nalogo')
		break
	stanje = stanje+1
		