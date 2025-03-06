import cv2 #openCV Library imported
import pyvista as pv #pyvista used for being able to display .obj files
import vtk #another open-source library for 3D graphics. necessary for stl files
import open3d as o3d #importing open3D also

#the function to get the object file
def getObject():
    print()
    #myObject = o3d.data.ArmadilloMesh() #simply testing to ensure that the code will work
    myObject = 'C:/Users/sarah/Desktop/3D_Models/Goat skull.ply' #hard-coding the path here for now
    return myObject #so this variable can be used in other functions

#enable camera
def enableCamera():
    print()

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
    print()
   # print("Hello") #test if everything is running.
    userObject = getObject()
    displayObject(userObject)


#this is where the overall function will be called
main()
