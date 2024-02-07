from PIL import Image, ImageDraw
import cv2
import numpy as np

img = Image.open('bw-rectified-left-022148small.png') #Objet Image
draw = ImageDraw.Draw(img) #Objet Draw pour dessiner les points nécéssaires pour identifier les coins

def longest_streak(list, argument): #Cette fonction permet de savoir s'il y a un arc entre les 16 pixels utilisés pour FAST
    max_streak = 0
    current_streak = 0
    for i in list:
        if i == argument:
            current_streak +=1
        else:
            max_streak = max([max_streak, current_streak])
            current_streak = 0
    return max_streak 

def detection_coin_FAST(image, centre, seuil):
    img = Image.open(image) #l'image qu'on se sert pour trouver ses coins
    p = centre #les coordonnées du pixel à tester
    t = seuil #threshold pour évaluer s'il est similaire ou non
    p_color = img.getpixel(p) #valeur de l'intensité du pixel à tester
    
    #On obtient la position de chaque pixel qui fait le tour du pixel testé dans un rayon de 3 pixels
    #comme montré dans le schéma de la question
    p1 = ((p[0]),(p[1]-3))
    p2 = ((p[0]+1),(p[1]-3))
    p3 = ((p[0]+2),(p[1]-2))
    p4 = ((p[0]+3),(p[1]-1))
    p5 = ((p[0]+3),(p[1]))
    p6 = ((p[0]+3),(p[1]+1))
    p7 = ((p[0]+2),(p[1]+2))
    p8 = ((p[0]+1),(p[1]+3))
    p9 = ((p[0]),(p[1]+3))
    p10 = ((p[0]-1),(p[1]+3))
    p11 = ((p[0]-2),(p[1]+2))
    p12 = ((p[0]-3),(p[1]+1))
    p13 = ((p[0]-3),(p[1]))
    p14 = ((p[0]-3),(p[1]-1))
    p15 = ((p[0]-2),(p[1]-2))
    p16 = ((p[0]-1),(p[1]-3))

    #On crée une liste contenant les valeurs d'intensité des 16 pixels
    lst = [img.getpixel(p1),
       img.getpixel(p2),
       img.getpixel(p3),
       img.getpixel(p4),
       img.getpixel(p5),
       img.getpixel(p6),
       img.getpixel(p7),
       img.getpixel(p8),
       img.getpixel(p9),
       img.getpixel(p10),
       img.getpixel(p11),
       img.getpixel(p12),
       img.getpixel(p13),
       img.getpixel(p14),
       img.getpixel(p15),
       img.getpixel(p16),]
    
    #On calcule la valeur de intensite_coin ou V comme vu dans les diapositives du cours
    compteur_1 = 0
    compteur_2 = 0
    for valeur in lst:
        if (valeur - p_color) > t:
            compteur_1 += (valeur - p_color)
        elif (p_color - valeur) > t:
            compteur_2 += (p_color - valeur)
    intensite_coin = max(compteur_1,compteur_2)

    lst_corner = [] #Cette liste va donner un attribut brillant, sombre ou similaire au pixel testé pour les 16 pixels

    for elem in lst:
        if elem <= (p_color - t):
            lst_corner.append("darker")
        elif (p_color - t) < elem < (p_color + t):
            lst_corner.append("similar")
        elif (p_color + t) <= elem:
            lst_corner.append("brighter")

    N = 12 #nombre de pixels consécutifs qu'il faut pour avoir un coin
    is_fast_corner = False #le coin est mis à faux par défaut
    lst_corner_check = [lst_corner[0], lst_corner[4], lst_corner[8], lst_corner[12]] #On garde la liste des pixels de chaque extrémité pour tester une exception
    if lst_corner.count("brighter") < 12 and lst_corner.count("darker") < 12 : #Si la liste n'a pas assez de pixels brillants ou sombres, on peut déduire que ce n'est pas un coin
        return (is_fast_corner, intensite_coin)
    if lst_corner[0] == "similar" and lst_corner[8] == "similar": #Si les pixels du haut et du bas sont similaires au pixel testé, on peut déduire que ce n'est pas un coin
        return (is_fast_corner, intensite_coin)
    if lst_corner_check.count("brighter") < 3 and lst_corner_check.count("darker") < 3 : #Si dans les quatres extrémités il n'y a pas assez de pixels brillants ou sombres, on peut déduire que ce n'est pas un coin
        return (is_fast_corner, intensite_coin)
    lst_corner_check_plus = lst_corner + lst_corner + lst_corner #On duplique la liste à gauche et à droite de la liste de base pour vérifier s'il y a au moins 12 pixels pareils consécutifs
    brighter_streak = longest_streak(lst_corner_check_plus, "brighter")
    darker_streak = longest_streak(lst_corner_check_plus, "darker")
    if brighter_streak >= N or darker_streak >= N: #on vérifie s'il y a au moins 12 pixels pareils consécutifs
            is_fast_corner = True
    else:
        return (is_fast_corner, intensite_coin)

    return (is_fast_corner, intensite_coin)

number_of_corners = 0 #Garder le trac du nombre de coins trouvés
for n in range(8,632): #Le range représente les dimensions de l'image avec une bordure de 8 pixels
    for m in range(8,472):
        if detection_coin_FAST('bw-rectified-left-022148small.png', (n,m), 10)[0] == True:
            draw.ellipse((n-1,m-1,n+1,m+1),outline="black") #Si le pixel testé est un coin, alors on l'ajoute à la variable globale et on trace un point dans l'image
            number_of_corners += 1

print(number_of_corners)

img.show()
img.save("Q4_test.png") #On montre et sauvegarde l'image dans le répertoire avec le nom indiqué à cette ligne