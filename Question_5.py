from Question_4 import detection_coin_FAST, longest_streak
from PIL import Image, ImageDraw
import cv2
import numpy as np
import random as rand
import math

img_Gauche = Image.open('bw-rectified-left-022148small.png') #L'image de gauche
img_Droite = Image.open('bw-rectified-right-022148small.png')#L'image de droite
draw = ImageDraw.Draw(img_Gauche) #Nous allons seulement dessiner sur l'image de gauche

def createImagePatch(position,image): #On crée la patch de 15X15 pixels autour du point passé en paramètre et on spécifie sur quelle image
    list_patch = []
    for y in range(position[1]-7,position[1]+8):
        for x in range(position[0]-7, position[0]+8):
            pixel = image.getpixel((x,y))
            list_patch.append(pixel)
    return list_patch #On retourne une liste des valeurs d'intensité des pixels allant d'en haut à gauche jusqu'en bas à droite

def createBriefDescriptorConfig(): #On crée la liste des tuples de deux points aléatoires qui sera testé pour obtenir le descripteur
    list_tuples_testing = []
    x = 0
    while x < 200:
        n1 = rand.randrange(start = 0, stop = 224, step = 1) #Ces nombres correspondent au nombre de valeurs qu'on retrouve dans la patch
        n2 = rand.randrange(start = 0, stop = 224, step = 1)
        list_tuples_testing.append((n1,n2))
        x += 1

    return list_tuples_testing #On retourne la liste des tuples à tester à chaque fois que ExtractBRIEF est appelé


def ExtractBRIEF(ImagePatch, BriefDescriptorConfig): #Extrait le descripteur (vecteur binaire) de la patch d'image avec les paires de pixels générés par la fonction createBriefDescriptorConfig
    descriptor = []
    for element in BriefDescriptorConfig:
        A = ImagePatch[element[0]]
        B = ImagePatch[element[1]]
        if A > B:
            descriptor.append(1)
        else:
            descriptor.append(0)
    return descriptor

list_genere = createBriefDescriptorConfig() #La liste des paires de pixels n'est générée qu'une seule fois

list_position_intensite = []
#On parcours toute l'image en tenant compte d'une bordure de 8 pixels
#On ajoute un tuple contenant l'intensité du coin trouvé et ses coordonnées dans une liste pour utiliser plus tard
for n in range(8,632):
    for m in range(8,472):
        if detection_coin_FAST('bw-rectified-left-022148small.png', (n,m), 10)[0] == True:
            list_position_intensite.append(((n,m), detection_coin_FAST('bw-rectified-left-022148small.png', (n,m), 10)[1]))

def get_intensite(x):
    return x[1]
list_position_intensite.sort(reverse=True, key=get_intensite) #On trie la liste des coins selon leur intensité en ordre décroissant
total_corners = len(list_position_intensite)
total_strongest_corners = math.floor(total_corners / 10)
list_position_intensite_strongest = list_position_intensite[0:total_strongest_corners]

list_descriptors_left = [] #On crée une liste avec tous les descripteurs pour l'image gauche et l'image droite
list_descriptors_right = []
for element in list_position_intensite_strongest:
    position = (element[0][0],element[0][1])
    list_descriptors_left.append((position, ExtractBRIEF(createImagePatch(position, img_Gauche), list_genere)))
    list_descriptors_right.append((position, ExtractBRIEF(createImagePatch(position, img_Droite), list_genere)))

list_appariement = [] #Liste contenant les appariements entre les pixels de l'image gauche avec l'image droite

z = 0
while z < 100: #On conserve seulement une centaine d'appariements, donc 100 lignes crée dans l'image de gauche
    m = rand.randrange(start = 0, stop = len(list_descriptors_left), step = 1) 
    d1 = list_descriptors_left[m][1] #On commence à choisir un des descripteurs parmi la liste des descripteurs de l'image gauche
    count_min = 10000000 #On garde le compte de la plus petite distance de Hamming avec la position du point
    position_min = (0,0)
    for element in list_descriptors_right: #On compare le descripteur de gauche choisi au hasard avec tous les descripteurs de l'image droite
        d2 = element[1]
        x = 0
        d_list = []
        while x < 200:
            d = d1[x] ^ d2[x]
            d_list.append(d)
            x += 1
        count = d_list.count(1)
        if count < count_min:
            count_min = count
            position_min = (element[0])
        
    list_appariement.append([list_descriptors_left[m][0],position_min])
    z += 1

for elem in list_appariement: #On dessine chaque appariement en créant une ligne dans l'image de gauche
    draw.line(elem)

img_Gauche.show()
img_Gauche.save("Q5.png")



