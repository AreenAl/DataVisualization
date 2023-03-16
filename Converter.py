import numpy as np
from stl import mesh
from PIL import Image
import matplotlib.pyplot as plt
import pathlib
import os
import PyPDF2


#image to stl converter function
def ImageConverter(path,destDir) :
    """Read Image from file and Display"""
    img = Image.open(path)

    """Convert Image to GreyScale"""
    grey_img =  img.convert("L")
    """Create syrface 1000x5000 with N traingles"""

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
            if z<1 or z is None:
                vertices[y][x] = (x, y,10)
            else:
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
    finalPath = destDir + f'/stlFiles/surface.stl'
    surface.save(finalPath)
    print(surface)

def PDFConverter(path):
    print('aaaaaa')
    pdf_file = open(path, 'rb')

    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Loop through each page in the PDF file
    for page_num in range(pdf_reader.numPages):
        # Get the current page
        page = pdf_reader.getPage(page_num)

        # Loop through each object on the page
        for obj in page['/Resources']['/XObject'].values():
            # Check if the object is an image
            if obj['/Subtype'] == '/Image':
                # Extract the image data
                img_data = obj.getData()

                # Save the image to a file
                with open('image{}.png'.format(page_num), 'wb') as img_file:
                    img_file.write(img_data)
