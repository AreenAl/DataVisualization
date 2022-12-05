import numpy as np
from stl import mesh
from PIL import Image 
import matplotlib.pyplot as plt 
import numpy as np
from stl import mesh
import pathlib
import os

#image to stl converter function
def ImageConverter(path,destDir) :
    """Read Image from file and Display"""
    img = Image.open(path)
    plt.imshow(img)

    """Conver Image to GreyScale"""

    grey_img =  Image.open(path).convert("L")
    plt.imshow(grey_img)

    """create simple 2d square surface with 2 traingles"""



    # Define the 4 vertices of the cube
    vertices = np.array([\
        [-1, -1, -1],
        [+1, -1, -1],
        [+1, +1, -1],
        [-1, +1, -1]])

    # Define the 2 triangles composing the cube
    faces = np.array([\
        [1,2,3],
        [3,1,0]])

    # Create the mesh
    cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            cube.vectors[i][j] = vertices[f[j],:]

    # Write the mesh to file "cube.stl"
    cube.save('surface.stl')

    """Create syrface 1000x5000 with N traingles"""

    grey_img = Image.open(path).convert('L')

    max_size=(500,500)
    max_height=10
    min_height=0

    grey_img.thumbnail(max_size)
    imageNp = np.array(grey_img)
    maxPix=imageNp.max()
    minPix=imageNp.min()


    print(imageNp)
    (ncols,nrows)=grey_img.size

    vertices=np.zeros((nrows,ncols,3))

    for x in range(0, ncols):
        for y in range(0, nrows):
            pixelIntensity = imageNp[y][x]
            z = (pixelIntensity * max_height) / maxPix
            #print(imageNp[y][x])
            vertices[y][x]=(x, y, z)

    faces=[]

    for x in range(0, ncols - 1):
        for y in range(0, nrows - 1):
            # create face 1
            vertice1 = vertices[y][x]
            vertice2 = vertices[y+1][x]
            vertice3 = vertices[y+1][x+1]
            face1 = np.array([vertice1,vertice2,vertice3])

        # create face 2 
            vertice1 = vertices[y][x]
            vertice2 = vertices[y][x+1]
            vertice3 = vertices[y+1][x+1]

            face2 = np.array([vertice1,vertice2,vertice3])

            faces.append(face1)
            faces.append(face2)

    print(f"number of faces: {len(faces)}")
    facesNp = np.array(faces)
    # Create the mesh
    surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            surface.vectors[i][j] = facesNp[i][j]
    # Write the mesh to file "cube.stl"
    print(destDir)
    filenumber = 1
    finalPath = destDir + f'/stlFiles/surface.stl'

    '''
    while(os.path.exists(destDir + f'/stlFiles/surface{filenumber}.stl')):
        filenumber+=1
        finalPath = destDir + f'/stlFiles/surface{filenumber}.stl'
'''
    surface.save(finalPath)
    print(surface)



