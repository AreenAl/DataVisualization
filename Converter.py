import numpy as np
from stl import mesh
from PIL import Image
import matplotlib.pyplot as plt
import pathlib
import os
import fitz



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
    # Define path for saved images
    images_path = 'images/'

    # Open PDF file
    pdf_file = fitz.open(path)

    # Get the number of pages in PDF file
    page_nums = len(pdf_file)

    # Create empty list to store images information
    images_list = []

    # Extract all images information from each page
    for page_num in range(page_nums):
        page_content = pdf_file[page_num]
        images_list.extend(page_content.get_images())

    # Raise error if PDF has no images
    if len(images_list) == 0:
        raise ValueError(f'No images found in {path}')

    # Save all the extracted images
    for i, img in enumerate(images_list, start=1):
        # Extract the image object number
        xref = img[0]
        # Extract image
        base_image = pdf_file.extract_image(xref)
        # Store image bytes
        image_bytes = base_image['image']
        # Store image extension
        image_ext = base_image['ext']
        # Generate image file name
        image_name = str(i) + '.' + image_ext
        # Save image
        with open(os.path.join(images_path, image_name), 'wb') as image_file:
            image_file.write(image_bytes)
            image_file.close()
