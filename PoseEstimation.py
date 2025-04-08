#For pose estimation. Lock in the optimal coordinates on the chessboard pattern grid to display the 3d object or graphic
#link to video tutorial walkthrough used for more understanding and pacing: https://www.youtube.com/watch?v=bs81DNsMrnM 

#library imports
import cv2 as cv
import os
import numpy as np 
import glob 
from enum import Enum

#DrawOption Class
class DrawOption(Enum):
    AXES = 1
    CUBE = 2
    OBJECT = 3
    
def drawAxes(img, corners, imgpts):
    #defining a tuple
    def tupleOfInts(arr):
        return tuple(int(x) for x in arr)
    
    corner = tupleOfInts(corners[0].ravel())
    img = cv.line(img,corner,tupleOfInts(imgpts[0].ravel()[:2]), (255,0,0),5)
    img = cv.line(img,corner,tupleOfInts(imgpts[1].ravel()[:2]), (0,255,0),5)
    img = cv.line(img,corner,tupleOfInts(imgpts[2].ravel()[:2]), (0,0,255),5)
    return img
    
def drawCube(img, imgpts):
    imgpts = np.int32(imgpts).reshape(-1,2)
    
    img = cv.drawContours(img, [imgpts[:4]], -1, (0,255,0), -3)
    
    for i, j in zip(range(4), range(4,8)):
        img = cv.line(img, tuple(imgpts[i]), tuple(imgpts[j]), (255), 3)
    
    img = cv.drawContours(img, [imgpts[4:]], -1, (0,0,255), 3)
    
    return img    

#defining the function to first load the object file in
def loadObject(x):
    #we are loading the vertices and faces so making empty lists that will be added in as we parse through the file
    vertices = []
    faces = []
    
    with open(x, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('v '): #if the line starts with vertex add it into vertices
                parts = line.split()
                vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
            elif line.startswith('f '): #if the line starts with face add it into faces
                parts = line.split()
                face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
                faces.append(face)
    return np.array(vertices, dtype=np.float32), faces
        
    
    
def drawObject(img, imgpts, faces):
    #drawing the 3D object now.
    imgpts = np.int32(imgpts).reshape(-1, 2)
    
    for face in faces:
            for i in range(len(face)):
                cv.line(img, imgpts[face[i-1][0]-1], imgpts[face[i][0]-1], (0, 0, 255), 2)
                #start_point = imgpts[face[i]]
                #end_point = imgpts[face[(i+1) % len(face)]]
                #img = cv.line(img, tuple(start_point), tuple(end_point), (0, 255, 0), 2)
    
    return img

    


#main function for this file: Pose Estimation
def poseEstimation(option: DrawOption, objFilePath):
    root = os.getcwd()
    #gets the parameters collected after camera calibration from the calibration folder
    paramPath = os.path.join(root, 'CameraCalibrationFolder/cal.npz')
    data = np.load(paramPath)
    camMatrix = data['camMatrix']
    distCoeff = data['distCoeff']
    
    #getting the paths for the images (will do live video afterwards)
    calibrationDir = os.path.join(root, 'CameraCalibrationFolder/ChessBoardPictures')
    imgPathList = glob.glob(os.path.join(calibrationDir, '*.jpg'))
    
    cap = cv.VideoCapture(0)
    
    #initializing the criteria. Exactly like in CameraCalibration.py
    Rows = 9
    Cols = 6
    termCriteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30,  0.001)
    worldPtsCur = np.zeros((Rows*Cols, 3), np.float32)
    worldPtsCur[:,:2] = np.mgrid[0:Rows,0:Cols].T.reshape(-1,2)
    
    #load the object from the file
    vertices, faces = loadObject(objFilePath)
    
    #world points of the options to draw 
    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]])
    cubeCorners = np.float32([[0,0,0], [0,3,0], [3,3,0], 
                              [3,0,0], [0,0,-3], [0,3,-3], 
                              [3,3,-3], [3,0,-3]])
    
    while True:
    #find Corners, similar to CameraCalibration.py
    #for curImgPath in imgPathList:
        ret, imgBGR = cap.read()
        
        if not ret:
            break
        
        #imgBGR = cv.imread(curImgPath)
        imgGray = cv.cvtColor(imgBGR, cv.COLOR_BGR2GRAY)
        cornersFound, cornersOrg = cv.findChessboardCorners(imgGray, (Rows, Cols), None)
        
        #to resize the view window so it is not bigger than the computer screen itself
        imgBGR = cv.resize(imgBGR, (800,600))
        
        if cornersFound ==True:
            cornersRefined = cv.cornerSubPix(imgGray, cornersOrg, (11,11), (-1,-1), termCriteria)
            ret, rvecs, tvecs = cv.solvePnP(worldPtsCur, cornersRefined, camMatrix, distCoeff)
            
            #have the different options depending on what the DrawOption is whether is it AXES, CUBE, or OBJECT
            
            if option == DrawOption.AXES:
                imgpts,_ = cv.projectPoints(axis,rvecs,tvecs,camMatrix,distCoeff)
                imgBGR = drawAxes(imgBGR, cornersRefined, imgpts) #calling the drawAxes function defined above 
            
            if option == DrawOption.CUBE:
                imgpts,_ = cv.projectPoints(cubeCorners, rvecs, tvecs, camMatrix, distCoeff)
                imgBGR = drawCube(imgBGR, imgpts)
                
            if option == DrawOption.OBJECT:
                imgpts, _ = cv.projectPoints(vertices, rvecs, tvecs, camMatrix, distCoeff)
                imgBGR = drawObject(imgBGR, imgpts, faces)
                 
        cv.imshow('AR', imgBGR)
            
            #cv.waitKey(1000)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv.destroyAllWindows()
            
if __name__== '__main__':
    objFilePath = "C:/Users/sarah/Desktop/3D_Models/AlienAnimal.obj"
    #to draw the AXES
    #poseEstimation(DrawOption.AXES) 
    
    #to draw the CUBE
    poseEstimation(DrawOption.CUBE, objFilePath) 
    
    #to draw the 3d object
    
    #poseEstimation(DrawOption.OBJECT, objFilePath)