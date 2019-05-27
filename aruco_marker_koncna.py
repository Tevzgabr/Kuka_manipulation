import numpy as np
import cv2 as cv
import cv2.aruco as aruco
import socket
import struct 
import simget

def send_vals(vals,vrednost,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_ip = '192.168.65.46'
    port1 = port

    packer = struct.Struct(vrednost)
    bin_data = packer.pack(*vals)
    sock.sendto(bin_data, (client_ip, port1))


# Camera parameters
calibrationFile = "logitech9000.yml"
calibrationParams = cv.FileStorage(calibrationFile, cv.FILE_STORAGE_READ)
camera_matrix = calibrationParams.getNode("camera_matrix").mat()
dist_coeffs = calibrationParams.getNode("distortion_coefficients").mat()
def marker(videoCapture):
    cap = cv.VideoCapture(videoCapture)
    # cv.namedWindow("test")
 
    while(True):
        # Frame-by-frame capture
        ret, frame = cap.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
        # Aruco dictionary
        aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
        parameters =  aruco.DetectorParameters_create()
      
    
        # Marker detection
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        # Estimated marker position
        if ids != None: # if marker is detecte
            rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, 0.10, camera_matrix, dist_coeffs)
            # rvecs = rotation
            # tvecs = translation
    
            arucoFrame = aruco.drawDetectedMarkers(frame, corners, ids, (0,255,0))
            # Marker axis
            aruco.drawAxis(arucoFrame, camera_matrix, dist_coeffs, rvecs, tvecs, 0.05)
        else: # if marker is not detected
            arucoFrame = frame
            rvecs = [[[0, 0, 0]]]
            tvecs = [[[0, 0, 0]]]
            ids = [[3,3]]
    
 
        vals=(rvecs[0][0][0],rvecs[0][0][1],rvecs[0][0][2],tvecs[0][0][0],tvecs[0][0][1],tvecs[0][0][2],ids[0][0])
        send_vals(vals,'f f f f f f f',55455)
        cv.imshow("aruco", arucoFrame)
        if cv.waitKey(1) & 0xFF == ord("q"): # za izhod pritisni q
            break
    
    x1 = corners[0][0][0][0]
    x2 = corners[0][0][1][0]
    x3 = corners[0][0][2][0]
    x4 = corners[0][0][3][0]
    y1 = corners[0][0][0][1]    
    y2 = corners[0][0][1][1]
    y3 = corners[0][0][2][1]
    y4 = corners[0][0][3][1]
    a = (x1+x2)/2
    b= (y1+y2)/2
    center =[a,b]
    # x_dist1 = (x2 - x1)/10
    # x_dist2 = (x3 - x4)/10  # calculated distance between the marker corners
    # y_dist1 = (y3 - y1)/10  # we know that the marker is 10x10 cm so we devide the 
    # y_dist2 = (y4 - y2)/10  # pixles lenght with 10 to get how many pixles are in 1cm
    cap.release()
    cv.destroyAllWindows()

    return(center)