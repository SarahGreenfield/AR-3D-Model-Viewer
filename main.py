import cv2 #openCV Library imported
import pyvista as pv #pyvista used for being able to display .obj files
import vtk #another open-source library for 3D graphics. necessary for stl files
import open3d as o3d #importing open3D also

#the function to get the object file
def getObject():
    print()
    #user input, the user is prompted to type in the path to their Object file
    #that input will be stored and returned to be used in other functions
    #myObject = o3d.data.ArmadilloMesh() #simply testing to ensure that the code will work
    #myObject = 'C:/Users/sarah/Desktop/3D_Models/Goat skull.ply' #hard-coding the path here for now
    #print("Enter")
    myObject = input("Enter the path to your 3D model file: ") #prompts the user to enter the path to the 3D object file they want to view.
    return myObject #so this variable can be used in other functions

#enable camera
def enableCamera():
    print()
    #will be testing out OpenCV here and maybe have the camera background needed when displaying the 3d object

#User input
def userControls():
    print()

#to display the object using TriangleMesh
def displayObject(x):
    print()
    #if user is using .stl:

    #else, use o3d
    mesh = o3d.io.read_triangle_mesh(x)
    #mesh = o3d.io.read_point_cloud("DeathStar.ply")s
    mesh.compute_vertex_normals() # more info on that
    o3d.visualization.draw_geometries([mesh])

    #print(mesh)



#the main function will be defined here
def main(): 
    print("Hello! Welcome to the 3D Object Viewer!")
   # print("Hello") #test if everything is running.
    print()
    userInput = input("Select what you want: (s to show, q to quit)")
    while userInput != 'q':  #while loop so the user can decide to view another object or exit    
        if userInput == 's': #for now it is a specific key for now. Right now, displaying the 3D model is a success! Now to try my hand at OpenCV
            userObject = getObject()
            displayObject(userObject)
        userInput = input("see another?: (q to quit)")
    
    print("thank you and have a nice day!")
    quit
    


#this is where the overall function will be called
main()
