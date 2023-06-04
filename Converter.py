import shutil
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
from PyPDF2 import PdfReader


# image to stl converter function
def ImageConverter(path, destDir):
    """Read Image from file and Display"""
    img = Image.open(path)
    # enhance the image graph quality and switch black to white
    # Load the image
    img = cv2.imread(path)

    # Get the current size of the image
    height, width = img.shape[:2]

    # Set the new size of the image to be 50% of the current size
    new_size = (int(width * 0.5), int(height * 0.5))

    # Resize the image to the new size using the resize() function
    minimized_image = cv2.resize(img, new_size)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(minimized_image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to get pure black and white
    _, bw_img = cv2.threshold(gray_img, 212, 255, cv2.THRESH_BINARY)

    image = Image.fromarray(bw_img).convert('L')
    data = np.array(image)
    print('data shape')
    # Create a mesh grid from the data
    x1 = np.arange(data.shape[1])
    y1 = np.arange(data.shape[0])
    x1, y1 = np.meshgrid(x1, y1)
    # Normalize the data to a range of 0 to 1 # to increase and decrease the density of the Z index
    z1 = (data/255)*10

    grid1 = pv.StructuredGrid(x1, y1, z1)
    print(grid1)

    # Define the dimensions of the grid
    dims = (10, 10, 10)

    x = np.linspace(-1, grid1.dimensions[1], dims[0])
    y = np.linspace(-1, grid1.dimensions[0], dims[1])

    z = np.linspace(-1, 3, dims[2])  # density of the floor
    xx, yy, zz = np.meshgrid(x, y, z, indexing='ij')  # building the floor
    points = np.column_stack((xx.ravel(), yy.ravel(), zz.ravel()))

    # Create the structured grid
    grid = pv.StructuredGrid(x, y, z)
    grid.dimensions = dims
    grid.points = points
    print("printing the floor")
    print(grid)  # bulding the floor
    grid1 = grid1.flip_z()
    comp = grid.merge(grid1)  # compine the floor and the object
    #comp = grid

    comp = comp.flip_z()  # to flip the final object for the printer
    #comp = comp.translate(xyz=(0.240,0.200,1),transform_all_input_vectors=True)
    comp = comp.scale(xyz=(0.2, 0.2, 0.5),
                      transform_all_input_vectors=True, inplace=True)
    comp = comp.rotate_x(180)
    iso = comp.extract_geometry()
    iso.smooth(n_iter=100)
    finalPath = destDir + f'/stlFiles/surface.stl'
    iso.save(finalPath)
    print(iso)


def PDFConverter(path, DestDir):
    reader = PdfReader(path)
    count = 0
    directory = DestDir + f'/images/'  # directory name
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)  # get the full file path
        if os.path.isfile(file_path):  # check if the path is a file
            os.remove(file_path)
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        for img in page.images:
            with open(os.path.join(DestDir, 'images', str(count)+img.name), "wb") as fp:
                fp.write(img.data)
                count += 1

    img = os.listdir(DestDir + f'/images/')
    for i in range(len(img)):
        temp = img[i]
        img[i] = 'images\\' + temp
    return img
