# Create a plane using 3 points (x,y,z)
# Plane Eq: Ax + By + Cz = D
# [A, B, C] are normal vectors to the plane
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
    ref_list = [ref1, ref2, ref3]
    for ref in ref_list:
        if ref.size != 3:
            raise Exception('3D point must have 3 Params "X,Y,Z"')
    ref_vec1 = ref2 - ref1
    ref_vec2 = ref3 - ref1
    normal_vec = np.cross(ref_vec1, ref_vec2)
    #Assign Plane Eq Inputs
    A, B, C = normal_vec
    D = np.dot(normal_vec, ref1)
    
    plane_eq_coeff = np.array([A, B, C, D])

    return  plane_eq_coeff, ref_list
    
def plot_plane(plane_eq_coeff, ref_list = None, mesh_count = 10):
    #Check for proper size of params for Plane Eq
    if plane_eq_coeff.size != 4:
        raise Exception('Plane equation must include 3 Params [A, B, C, D] = Ax + By + Cz = D')
        
    # create the figure
    fig = plt.figure()
    
    #Generate X and y mesh grid points with mech_counts amount
    xx, yy = np.meshgrid(range(mesh_count), range(mesh_count))
    #Generate array of points Z points of plane for plotting
    z = (plane_eq_coeff[3] - plane_eq_coeff[0] * xx - plane_eq_coeff[1] * yy) / plane_eq_coeff[3]
    
    # add axes
    ax = fig.add_subplot(111,projection='3d')
    
    # plot the plane
    ax.plot_surface(xx, yy, z, alpha=0.5)
    
    #Plot input points
    if ref_list != None:
        ax.scatter(ref_list)
    plt.show()

#Simulate Refeerence points given from Stepper positions 
#

point1 = np.array([ , , ])
point2 = np.array([ , , ])
point3 = np.array([ , , ])
