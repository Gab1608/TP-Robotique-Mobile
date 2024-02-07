from os import get_handle_inheritable
import numpy as np
import math
from scipy.optimize import fmin
import matplotlib.pyplot as plt

#################################################
##               FUNCTIONS                     ##
#################################################

#######
# 3.1 #
#######

def reprojection(H, focal, L):
    matIntrinsect = np.mat([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1/focal, 0]])

    matIntrinsect = matIntrinsect @ H

    C = []
    for point in L:
        # Transformons tous les points L en coordonnées homogènes
        point = np.append(point, [1])
        x_points = matIntrinsect @ point
        C.append([x_points[0, 0] / x_points[0, 2], x_points[0, 1] / x_points[0, 2]])

    return C

# H contient matrice de rotation auteur de l'axe y ainsi que matrice de translation
def get_H_matrix(rotation, translationX, translationZ):
    return np.array([[math.cos(rotation), 0, math.sin(rotation), translationX],
             [0, 1, 0, 0],
             [-math.sin(rotation), 0, math.cos(rotation), translationZ],
             [0, 0, 0, 1]])

#######
# 3.2 #
#######

# Réécriture de la fonction pour n'accepter qu'un point de repère L homogène.
# On retourne seulement une position (u, v) sur l'image et non une liste.
def reprojection_3_2(H, focal, L):
    matIntrinsect = np.mat([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1/focal, 0]])

    matIntrinsect = matIntrinsect @ H

    x_points = matIntrinsect @ L
    return [x_points[0, 0] / x_points[0, 2], x_points[0, 1] / x_points[0, 2]]


def distance(a, b):
    return math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))


def somme_des_residuels_au_carre(pose_camera, focal, L, C):
    total = 0
    Tx = pose_camera[0]
    Tz = pose_camera[1]
    A = pose_camera[2]

    H = get_H_matrix(A, Tx, Tz)
    
    for index, l in enumerate(L):
        r = distance(c[index], reprojection_3_2(H, focal, l))
        total += math.pow(r, 2)

    return total

#################################################
##                  MAIN                       ##
#################################################


#######
# 3.1 #
#######

A = 0  # Angle de rotation
Tx = 0 # Translation x
Tz = 0 # Translation y

H = get_H_matrix(A, Tx, Tz)

L = np.array([[-0.3, 0, 1.3],
              [0, 0, 1],
              [0.3, 0, 1.3]])

focal = 1100
c = reprojection(H, focal, L)
print("C = ", c, end = '\n')


#######
# 3.2 #
#######

L = np.array([[-0.3, 0, 1.3, 1],
              [0, 0, 1, 1],
              [0.3, 0, 1.3, 1]])

pose_initiale_camera = [0.2, 0.2, 0.2]
print("Pose initial: ", pose_initiale_camera, end = '\n')
pose_solution = fmin(somme_des_residuels_au_carre, pose_initiale_camera, args=(focal, L, c), maxiter=1000)
print("Pose solution: ", pose_solution, end = '\n')


#######
# 3.3 #
#######

x_points = []
z_points = []
for meter in range(0, 8):
    H = get_H_matrix(0, 0, meter)
    for i in range(0, 1000):
        for l in L:
            point = reprojection_3_2(H, focal, l)
            x_points.append(point[0] + 3 * np.random.randn())
            z_points.append(pose_solution[1] + meter)

fig, ax = plt.subplots()
ax.set_xlim(-12, 12)
ax.set_ylim(-2, 8)
plt.plot(x_points, z_points, 'o')
plt.show()