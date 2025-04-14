#For pose estimation. Lock in the optimal coordinates on the chessboard pattern grid to display the 3d object or graphic
#link to video tutorial walkthrough used for more understanding and pacing: https://www.youtube.com/watch?v=bs81DNsMrnM 

#library imports
import cv2 as cv
import os
import numpy as np 
import glob 
from enum import Enum
import trimesh

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
def loadObject():
    #using the trimesh method to load the object file.
    #mesh = trimesh.load("C:/Users/sarah/Desktop/3D_Models/Hourglass.obj")
    print()
    
    
def drawObject(img, imgpts):
    #mesh = trimesh.load("C:/Users/sarah/Desktop/3D_Models/Hourglass.obj")
    #vertices = np.array(mesh.vertices, dtype=np.float32)
    print()

    


#main function for this file: Pose Estimation
def poseEstimation(option: DrawOption, mesh):
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
    #vertices, faces = loadObject(objFilePath)
    
    #world points of the options to draw 
    axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]])
    cubeCorners = np.float32([[0,0,0], [0,3,0], [3,3,0], 
                              [3,0,0], [0,0,-3], [0,3,-3], 
                              [3,3,-3], [3,0,-3]])
    
    #while True:
    #find Corners, similar to CameraCalibration.py
    for curImgPath in imgPathList:
            #ret, imgBGR = cap.read()
        
            #if not ret:
                #break
        
        imgBGR = cv.imread(curImgPath)
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
                
                    
                    #honest: used ChatGpt to figure out an error from loading object as scene and not a trimesh object
                    #check to ensure the program will not break down
                if isinstance(mesh, trimesh.Trimesh):
                    mesh = mesh
                    
                elif isinstance(mesh, trimesh.Scene):
                        #mesh = mesh.dump(concatenate=True) #using the .dump function to get rid of any scene object
                        #mesh = mesh.to_geometry()
                    mesh = trimesh.util.concatenate(list(mesh.geometry.values())) #returns not a single mesh and then merges all meshes together
                        
                else:
                    raise ValueError("The object you are trying to load in the Augmented Reality feature is not compatible.")
                    
                vertices = np.array(mesh.vertices, dtype=np.float32)
                    
                    #imgpts, _ = cv.projectPoints(vertices, rvecs, tvecs, camMatrix, distCoeff)
                    #imgBGR = drawObject(imgBGR, imgpts, faces)
                projVertices, _ = cv.projectPoints(vertices, rvecs, tvecs, camMatrix, distCoeff)
                    
                    #extra step to avoid any errors that could crash the code
                if np.any(np.isnan(projVertices)):
                    print("Skipping this as the 3D model you are trying to view contains values that are incorrect for this program.")
                    continue
                    
                projVertices = np.array(projVertices, dtype=np.int32).reshape(-1, 2)
                    
                for face in mesh.faces:
                    v1, v2, v3 = projVertices[face[0]], projVertices[face[1]], projVertices[face[2]]
                    cv.line(imgBGR, v1, v2, (0, 255, 0), 2)
                    cv.line(imgBGR, v2, v3, (0, 255, 0), 2)
                    cv.line(imgBGR, v3, v1, (0, 255, 0), 2)
                    
                 
        cv.imshow('AR', imgBGR)
            
        cv.waitKey(0)
        #if cv.waitKey(1) & 0xFF == ord('q'):
         #   break
        
    cap.release()
    cv.destroyAllWindows()
            
def ShowImage(x):
    #objFilePath = "C:/Users/sarah/Desktop/3D_Models/Hourglass.obj"
    #to draw the AXES
    #poseEstimation(DrawOption.AXES, objFilePath) 
    
    #to draw the CUBE
    #poseEstimation(DrawOption.CUBE, objFilePath) 
    
    #to draw the 3d object
    mesh = trimesh.load(x)
    poseEstimation(DrawOption.OBJECT, mesh)
    
#ShowImage(x)