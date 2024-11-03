import pyvista as pv
from stl import mesh
import numpy as np

# Load the STL file
your_mesh = mesh.Mesh.from_file('sun.stl')


# Define rotation angles (in radians)
angle_x = np.radians(90)  # 45 degrees around the X-axis
angle_y = np.radians(30)  # 30 degrees around the Y-axis
angle_z = np.radians(60)  # 60 degrees around the Z-axis

# Define rotation matrices for each axis
rotation_matrix_x = np.array([
    [1, 0, 0],
    [0, np.cos(angle_x), -np.sin(angle_x)],
    [0, np.sin(angle_x), np.cos(angle_x)]
])

rotation_matrix_y = np.array([
    [np.cos(angle_y), 0, np.sin(angle_y)],
    [0, 1, 0],
    [-np.sin(angle_y), 0, np.cos(angle_y)]
])

rotation_matrix_z = np.array([
    [np.cos(angle_z), -np.sin(angle_z), 0],
    [np.sin(angle_z), np.cos(angle_z), 0],
    [0, 0, 1]
])

# Combine rotations (rotation order: Z -> Y -> X)
rotation_matrix = rotation_matrix_z @ rotation_matrix_y @ rotation_matrix_x

# Apply the rotation to each vector in the mesh
your_mesh.vectors = np.dot(your_mesh.vectors, rotation_matrix)


faces = np.hstack([[3] + list(triangle) for triangle in your_mesh.vectors.reshape(-1, 3)])  # 3 vertices per face




##################
vertices = your_mesh.vectors.reshape(-1, 3)
faces = np.hstack([[3, i, i+1, i+2] for i in range(0, len(vertices), 3)])
# Create the PolyData mesh
pv_mesh = pv.PolyData(vertices, faces)

##################
# Convert STL mesh to PyVista format for visualization
# pv_mesh = pv.PolyData(your_mesh.vectors.reshape(-1, 3), faces)

# Set up the PyVista plotter
# pv.rcParams['transparent_background'] = True

plotter = pv.Plotter(off_screen=True)  # Use off_screen=True to avoid showing the window
plotter.add_mesh(pv_mesh, color="lightblue", show_edges=True)
plotter.background_color = None

# Save the screenshot
plotter.show(screenshot="object.png" )