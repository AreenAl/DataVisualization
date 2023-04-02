import numpy as np
# pip3 install numpy
from stl import mesh
# pip3 install numpy-stl
from PIL import Image
import matplotlib.pyplot as plt
import pathlib
from PyPDF2 import PdfReader
import shutil
import os
import fitz
import cv2
# pip install opencv-python opencv-python-headless
import pyvista as pv
# pip install pyvista


# image to stl converter function
def ImageConverter(path, destDir):
    """Read Image from file and Display"""
    img = Image.open(path)
    # enhance the image graph quality and switch black to white
    # Load the image
    img = cv2.imread(path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get pure black and white
    _, bw_img = cv2.threshold(gray_img, 212, 255, cv2.THRESH_BINARY)

    image = Image.fromarray(bw_img).convert('L')
    data = np.array(image)
    print('data shape')
    # Create a mesh grid from the data
    x1, y1 = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))
    # Normalize the data to a range of 0 to 1 # to increase and decrease the density of the Z index
    z1 = (data/255)*8

    grid1 = pv.StructuredGrid(x1, y1, z1)

    # Define the dimensions of the grid
    dims = (10, 10, 10)

    # Define the coordinates of the points of the grid
    print(grid1.dimensions[0])
    print(grid1.dimensions[1])
    x = np.linspace(-1, grid1.dimensions[1], dims[0])
    y = np.linspace(-1, grid1.dimensions[0], dims[1])

    z = np.linspace(-1, 3, dims[2])  # density of the floor
    xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')  # building the floor
    points = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))

    # Create the structured grid
    grid = pv.StructuredGrid()
    grid.dimensions = dims
    grid.points = points
    print(grid)  # bulding the floor
    grid1 = grid1.flip_z()
    comp = grid+grid1  # compine the floor and the object
    comp = comp.flip_z()  # to flip the final object for the printer
    comp = comp.rotate_x(180)
    iso = comp.extract_geometry()
    iso.smooth(n_iter=100) # smooth the surface
    finalPath = destDir + f'/stlFiles/surface.stl'
    iso.save(finalPath)
    print(iso)

def PDFConverter(path,DestDir):
    reader = PdfReader(path)
    count = 0
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        for img in page.images:
            with open(str(count) +img.name, "wb") as fp:
                fp.write(img.data)
                count += 1

            Dir=os.path.abspath(os.getcwd())
            old=os.path.join(Dir, str(count-1) +img.name)
            finalPath = DestDir + f'/images/'+str(count-1) +img.name
            shutil.move(old, finalPath)