#this code was done through a tutorial by Kevin Wood | Robotics & AI on YouTube
#Links: https://www.youtube.com/watch?v=H5qbRTikxI4&t=1s Camera Calibration Tutorial

#libraries and modules to import from python
import numpy as np  
import cv2 as cv  
import glob 
import os 
import matplotlib.pyplot as plt

#This will be the separate file to only calibrate the camera before plugging in the values of the Camera Matrices into the functions back in Program.py

#total number of corners in the chessboard: excluding the border corners:


#the calibrate function
def calibrate(pics=True):
    #this is to read the images in the folder of ChessBoardPictures
    root = os.getcwd()
    #for now going through still images (will use live video after the AR works)
    calibrationDir = os.path.join(root, 'ChessBoardPictures')
    imgPathList = glob.glob(os.path.join(calibrationDir, '*.jpg'))
    
    #initialize
    Rows = 9 #number of corners for rows and columns for the chessboard png
    Cols = 6
    termCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30,  0.001)
    worldPtsCur = np.zeros((Rows*Cols, 3), np.float32)
    worldPtsCur[:,:2] = np.mgrid[0:Rows,0:Cols].T.reshape(-1,2)
    #empty lists to add into to calibrate the camera
    worldPtsList = []
    imgPtsList = []
    
    #find the corners
    for curImgPath in imgPathList:
        imgBGR = cv.imread(curImgPath)
        imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)
        cornersFound, cornersOrg = cv.findChessboardCorners(imgGray,(Rows,Cols),None)
        
        #resize to the window does not overtake the screen :) using the resize function in openCV
        imgBGR_resized = cv.resize(imgBGR, (800,600))
        
        
        if cornersFound == True:
            worldPtsList.append(worldPtsCur)
            cornersRefined = cv.cornerSubPix(imgGray,cornersOrg,(11,11),(-1,-1),termCriteria)
            imgPtsList.append(cornersRefined)
            if pics: #if true
                cv.drawChessboardCorners(imgBGR_resized, (Rows,Cols), cornersRefined, cornersFound)
                cv.imshow('Image', imgBGR_resized)
                cv.waitKey(500)
    cv.destroyAllWindows()
    
    #now to do the calibration after reading through the images
    #to help find the Intrinsics and Extrinsics values
    repError, camMatrix, distCoeff, rvecs, tvecs = cv.calibrateCamera(worldPtsList, imgPtsList, imgGray.shape[::-1], None, None)
    #printing the values for the Camera Matrix and Reprojecting Errors
    print("Camera Matrix:\n",camMatrix)
    print("Reproj Error (pixels): {:.4f}".format(repError))
        

#runCalibration function
def runCalibration():
    #this runs the calibrate function with parameter for the boolean to be true
    calibrate(pics=True)

#ultimate main function for this application
if __name__ == '__main__':
    #runCalibration app
    runCalibration()