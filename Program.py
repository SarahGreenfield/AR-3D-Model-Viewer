import cv2 #openCV Library imported
import pyvista as pv #pyvista used for being able to display .obj files
import vtk #another open-source library for 3D graphics. necessary for stl files
import open3d as o3d #importing open3D also

#files to import
import AR_Image
import AR2


WEBCAM = cv2.VideoCapture(0) #camera constant to be used in any function
#user input path example: C:/Users/sarah/Desktop/3D_Models/DeathStar.stl

#the function to get the object file
def getObject():
    print()
    #user input, the user is prompted to type in the path to their Object file
    #that input will be stored and returned to be used in other functions
    #myObject = o3d.data.ArmadilloMesh() #simply testing to ensure that the code will work
    #myObject = 'C:/Users/sarah/Desktop/3D_Models/DeathStar.stl' #hard-coding the path here for now
    #print("Enter")
    myObject = input("Enter the path to your 3D model file: ") #prompts the user to enter the path to the 3D object file they want to view.
    return myObject #so this variable can be used in other functions

#enable camera
#function for the camera will be changed since the while loop is within this function
def enableCamera(x, y):
    print()
    #will be testing out OpenCV here and maybe have the camera background needed when displaying the 3d object
    #using the youtube tutorial as reference
    camera = cv2.VideoCapture(x) #just accessing the webcam, not reading a video file
    #if statement for if there is no camera connected
    if not camera.isOpened():
        print("No Camera Identified. Please check your connection with the webcam/camera.")
        exit()
    
    #with a camera
    print("press 'x' to turn off the camera")
    while(True):
        ret, frame = camera.read()
        if not ret:
                print("no more video")
                break
        frameResized = cv2.resize(frame, (800,600))
        cv2.imshow("Object Viewer", frameResized)
        
        if cv2.waitKey(1) == ord('x'):
            break
        
    camera.release()
    cv2.destroyAllWindows()
    

#User input
def userControls(): #for use of arrow keys for control of the object (most likely going to be optional, since this one will be viewed on the computer and we already have access to the mouse to control it)
    print()

#to display the object using TriangleMesh
def displayObject(x):
    print()
    #if user is using .stl:

    #else, use o3d
    '''
    mesh = o3d.io.read_triangle_mesh(x)
    #mesh = o3d.io.read_point_cloud("DeathStar.ply")s
    mesh.compute_vertex_normals() # more info on that
    o3d.visualization.draw_geometries([mesh])'''
    
    #print(mesh)
    #PyVista Code Here!
    
    mesh = pv.read(x)
    mesh.plot(background='black', show_edges=True) 
    



#the main function will be defined here
def main(): 
    print("Hello! Welcome to the 3D Object Viewer!")
   # print("Hello") #test if everything is running.
    print()
    #Link = input("Please Launch your IP Webcam app server on your mobile device and type in the link: ")
    #x = '/video'
    #y = 'http://'
    #newLink = y + Link + x
    userInput = input("Select what you want: (s to show, q to quit)")
    while userInput != 'q':  #while loop so the user can decide to view another object or exit    
        if userInput != 'q': #for now it is a specific key for now. Right now, displaying the 3D model is a success! Now to try my hand at OpenCV
            #userObject = getObject()
            #enableCamera(0, userObject)
            print("Please ensure that the model you are going to view in AR is scaled down to show.")
            userFile = input("Enter the file path to your .obj file: ")
            #add the loop for the camera here and see what happens
            query = input("see through video feed (simple objects work best for runtime) (v) or images (i): ")
            if query == 'v':
                AR2.showAR(userFile)
            elif query == 'i':
                AR_Image.ShowImage(userFile)
                
            else:
                print("Invalid input. Please try again.")
                continue
            #"C:/Users/sarah/Desktop/3D_Models/AlienAnimal.obj"
            
            #displayObject(userObject)
        userInput = input("see another?: (q to quit)")
    
    print("thank you and have a nice day!")
    quit
    


#this is where the overall function will be called
main()
