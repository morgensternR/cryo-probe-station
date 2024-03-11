# Create a plane using 3 points (x,y,z)
# Plane Eq: Ax + By + Cz = D
# [A, B, C] are normal vector coeff to the plane
# [D] is the dot product of the normal vector with any one of the input position point vectors (X_n, Y_n, Z_n)
#Steps:
    # 1. Give 3 x (X_n, Y_n, Z_n) coordinates as the input
    # 2. Find two (non-zero) vectors With the any respect coords
    # 3. Cross product the two vectors to find the orthoginal plane direction to make [A, B, C]
    # 4. Dot product the orthoginal plane direciton with respect to anyone one of the input coordinates to make [D]
    # 5. Output will be a numpy array of the form [A, B, C, D] -> Ax + By + Cz = D
# To Plot, generate points for X and Y and Plot Z
# Form : z = (D - A * x - B * y) / C
    
import numpy as np
import matplotlib.pyplot as plt

def conv_points_to_plane_eq(ref1, ref2, ref3):
    ref_array = np.array([ref1, ref2, ref3])
    for ref in ref_array:
        if ref.size != 3:
            raise Exception('3D point must have 3 Params "X,Y,Z"')
    ref_vec1 = ref2 - ref1
    ref_vec2 = ref3 - ref1
    normal_vec = np.cross(ref_vec1, ref_vec2)
    #Assign Plane Eq Inputs
    A, B, C = normal_vec
    D = np.dot(normal_vec, ref1)
    
    plane_eq_coeff = np.array([A, B, C, D])

    return  plane_eq_coeff, ref_array
    
def plot_plane(plane_eq_coeff, ref_array= None, mesh_count = 10):
    #Check for proper size of params for Plane Eq
    if plane_eq_coeff.size != 4:
        raise Exception('Plane equation must include 3 Params [A, B, C, D] = Ax + By + Cz = D')
        
    # create the figure
    fig = plt.figure()
    
    #Generate X and y mesh grid points with mech_counts amount
    x_grid = np.linspace(-mesh_count, mesh_count, int(mesh_count*1e2))
    y_grid = np.linspace(-mesh_count, mesh_count, int(mesh_count*1e2))
    xx, yy = np.meshgrid(x_grid, y_grid)
    #Generate array of points Z points of plane for plotting
    z = (plane_eq_coeff[3] - plane_eq_coeff[0] * xx - plane_eq_coeff[1] * yy) / plane_eq_coeff[3]
    
    # add axes
    ax = fig.add_subplot(111,projection='3d')
    
    # plot the plane
    ax.plot_surface(xx, yy, z, alpha=0.5)
    
    #Plot input points
    if isinstance(ref_array, np.ndarray):
        ax.scatter(xs = ref_array[:,0], ys = ref_array[:,1], zs = ref_array[:,2])
    plt.show()
    return z
#%%
#Simulate Refeerence points given from Stepper positions 
#

point1 = np.array([0 ,0, 1])
point2 = np.array([25 , 25, 1])
point3 = np.array([25 , -25, 1])

plane_coeff, ref_array = conv_points_to_plane_eq(point1, point2, point3)
z = plot_plane(plane_coeff,  ref_array = ref_array,  mesh_count = 25)

#%%

#Goal: Using grid coordi9nates, correleate those to stepper locations. Subtract known physical offsets of probe center to each stepper axis
#1. Input coordinate "ref" [x,y,z]. This is where you want the probe head to go
#2. Remove/add offsets to translate probe head locaiton to stepper location
#3. return coords to use with stepper functions
# X Axis
# X Axis is expected to fault out at 100mm, this is out starting point
#
#

def remove_probe_offsets(ref, y_stage_offset = 1.5 , x_stage_offset, z_stage_offset, y_probe, x_probe, y_probe, z_probe):
    