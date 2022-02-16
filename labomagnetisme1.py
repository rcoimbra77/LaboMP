import math
import pygame
import sys
import random


DEFAUT      = 0
EXPERIENCE1 = 1
EXPERIENCE2 = 2
EXPERIENCE3 = 3
EXPERIENCE4 = 4
EXPERIENCE5 = 5
EXPERIENCE6 = 6
EXPERIENCE7 = 7
EXPERIENCE8 = 8

RAYON = 10

mode     = EXPERIENCE2 # Choisir l'expérience. DEFAULT, EXPERIENCE1, EXPERIENCE2 pour le cours, le reste pour la curiosité. 
mobilite = 0


# Constantes

BLEUCLAIR = (127, 191, 255)
NOIR      = (0,0,0)
ROUGE     = (255,0,0)
A = 2
B = 5
C = 20
#k = 8 987 600 000
k = 8.9876 * pow(10,9)



# La norme de ce vecteur est égale à k|q|r2, où r est la distance qui sépare p et p′,
# Paramètres
LARGEUR = 1600
HAUTEUR = 900
dimensions_fenetre = (LARGEUR, HAUTEUR)  # en pixels
images_par_seconde = 50
objets = []

def deplacer_pol(point, distance, orientation):
    x, y = point

    x = point[0] + (distance * math.cos(orientation))
    y = point[1] + (distance * math.sin(orientation))

    return (x, y)

def dessiner_vecteur(fenetre, couleur, origine, vecteur):

    p = origine
    p4 = p + vecteur
    angle = math.atan2(vecteur[1], vecteur[0])

    if math.sqrt(vecteur[1]**2 + vecteur[0]**2) >= 20:
        p4 = (p[0] + vecteur[0], p[1] + vecteur[1])
        pp4 = math.sqrt(vecteur[1]**2 + vecteur[0]**2)
        p1 = deplacer_pol(p, A, angle - math.pi/2)
        p7 = deplacer_pol(p, A, angle + math.pi/2)
        p2 = deplacer_pol(p1, pp4 - C, angle)
        p6 = deplacer_pol(p7, pp4 - C, angle)
        p3 = deplacer_pol(p2, B, angle - math.pi/2)
        p5 = deplacer_pol(p6, B, angle + math.pi/2)
        #print(couleur)
        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4, p5, p6, p7])

    else:
        p3 = (p[0] + vecteur[0], p[1] + vecteur[0])
        p1 = deplacer_pol(p3, C, angle + math.pi)
        p2 = deplacer_pol(p1, A + B, angle - math.pi/2)
        p4 = deplacer_pol(p1, A + B, angle + math.pi/2)

        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4])

def dessiner_vecteur_centre(fenetre, couleur, origine, vecteur):
    x = (origine[0] + origine[0]-vecteur[0]) //2
    y = (origine[1] + origine[1]-vecteur[1]) //2
    dessiner_vecteur(fenetre, couleur, (x,y), vecteur)

def ajouter_objet(x,y,z, vx, vy):
    objets.append([x,y,z, vx, vy])

def print_objets():
    for o in objets:
        print(o)


def dessiner_objets():
    for o in objets:
        if (o[2]<0):
            pygame.draw.circle(fenetre, NOIR , (o[0], o[1]), RAYON)
        else:
            pygame.draw.circle(fenetre, ROUGE, (o[0], o[1]), RAYON)

def bouger_objets():
    for o in objets:
        o[0] += o[3]
        o[1] += o[4]

        if (o[0] < 0):
            o[0] = LARGEUR
        if (o[0] > LARGEUR):
            o[0] = 0

        if (o[1] < 0):
            o[1] = HAUTEUR
        if (o[1] > HAUTEUR):
            o[1] = 0

        #print(o)

def dessiner_champ(pas):
    x = -pas
    while(x < dimensions_fenetre[0] + pas):
        y = -pas
        while(y < dimensions_fenetre[1] + pas):
            vecteur = calculer_champ(x,y)

            if (vecteur != None):

                e = math.sqrt(vecteur[0]*vecteur[0] + vecteur[1]*vecteur[1])
                #print(" ")
                #print("norme de e:")
                #print(e)

                v = math.sqrt(1000 * e) #NON
                #print(" ")
                #print("v:")
                #print(v)
                #print(" ")

                if(v >=0 and v<=8):
                    couleur = (255,255*v/8,0)
                elif(v >8 and v<=16):
                    couleur = (255-(v-8)/8*255,255,(v-8)*255/8)
                elif(v >16 and v<=24):
                    couleur = (0,255-(v-16)*255/8,255)
                elif(v >24 and v<=32):
                    couleur = (255*(v-24)/8,0,255)
                elif(v >32):
                    couleur =  (255, 0, 255)
                else:
                    couleur = (0,0,0)

                vecteur = normer_vecteur(40, vecteur)

                dessiner_vecteur_centre(fenetre, couleur, (x,y), (vecteur[0], vecteur[1]))

            y += pas
        x += pas

def normer_vecteur(tailleMax, v):
    norme   = math.sqrt(v[0]*v[0] + v[1]*v[1])
    vecteur = [0,0]
    if (norme !=0):
        vecteur = [ v[0]*tailleMax/norme, v[1]*tailleMax/norme ]
    return vecteur


def calculer_champ(x,y):
    norme = 0
    v = [0,0]

    for o in objets:
        r     = math.sqrt( (x-o[0]) * (x-o[0]) + (y-o[1]) * (y-o[1]) )
        if(r > 20):
            norme = k * abs(o[2]) / (r*r)
        else:
            return None
        angle = math.atan2( (y-o[1]), (x-o[0]) )

        if (o[2]<0):
            vtemp = (-norme * math.cos(angle) , -norme * math.sin(angle))
        else:
            vtemp = (norme * math.cos(angle) , norme * math.sin(angle))


        v[0] += vtemp[0]
        v[1] += vtemp[1]

    return v


#print_objets()
# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 1")

if (mode == DEFAUT):
    ajouter_objet(800,200,pow(10,-6), 0, 0)
    ajouter_objet(800,700,-pow(10,-6), 0, 0)

elif (mode == EXPERIENCE1):
    ajouter_objet(550,200,-pow(10,-6) ,  0, 0)
    ajouter_objet(1050,700,-pow(10,-6),  0, 0)
    ajouter_objet(1050,200,pow(10,-6) ,  0, 0)
    ajouter_objet(550,700,pow(10,-6)  ,  0, 0)

elif (mode == EXPERIENCE2):

    for x in range(20): 
        ajouter_objet(600+x*RAYON*2,300,pow(10,-7), 0, 0)
        ajouter_objet(600+x*RAYON*2,600,-pow(10,-7), 0, 0)


elif (mode == EXPERIENCE3):

    for x in range(20): 
        ajouter_objet(600+x*RAYON*2,300, pow(10,-7), 0, 8)
        ajouter_objet(600+x*RAYON*2,600,-pow(10,-7), 0, -8)

elif (mode == EXPERIENCE4):

    ajouter_objet(1300,200,-pow(10,-6),  -5, 0)
    ajouter_objet(300 ,700,-pow(10,-6),  5, 0)
    ajouter_objet(300 ,200,pow(10,-6) ,  5, 0)
    ajouter_objet(1300,700,pow(10,-6) ,  -5, 0)

elif (mode == EXPERIENCE5):
    
    ajouter_objet(550 ,200,-pow(10,-6),  5, 5)
    ajouter_objet(650 ,300,-pow(10,-6),  5, 5)
    ajouter_objet(1050,700,-pow(10,-6), -5, -5)
    ajouter_objet(950 ,600,-pow(10,-6), -5, -5)

    ajouter_objet(1050,200,pow(10,-6),  -5, 5)
    ajouter_objet(550 ,700,pow(10,-6),   5, -5)
    ajouter_objet(950 ,300,pow(10,-6),  -5, 5)
    ajouter_objet(650 ,600,pow(10,-6),   5, -5)

elif (mode == EXPERIENCE6):

    for x in range (random.randint(5,10)):
        ajouter_objet(random.randint(0, LARGEUR), random.randint(0, HAUTEUR), pow(10,-6) , random.randint(-10,10), random.randint(-10,10))
        ajouter_objet(random.randint(0, LARGEUR), random.randint(0, HAUTEUR), -pow(10,-6), random.randint(-10,10), random.randint(-10,10)) 


elif (mode == EXPERIENCE7):
    ajouter_objet(0,400 , pow(10,-6), 6, 0)
    ajouter_objet(50,400,-pow(10,-6), 6, 0)
    ajouter_objet(0,500 ,-pow(10,-6), 6, 0)
    ajouter_objet(50,500, pow(10,-6), 6, 0)

    ajouter_objet(1600 ,400 , pow(10,-6), -6, 0)
    ajouter_objet(1550 ,400 ,-pow(10,-6), -6, 0)
    ajouter_objet(1600 ,500 ,-pow(10,-6), -6, 0)
    ajouter_objet(1550 ,500 , pow(10,-6), -6, 0)

elif (mode == EXPERIENCE8):
    ajouter_objet(0,400 , pow(10,-6), 6, 0)
    ajouter_objet(50,400,-pow(10,-6), 6, 0)
    ajouter_objet(0,500 ,-pow(10,-6), 6, 0)
    ajouter_objet(50,500, pow(10,-6), 6, 0)
    ajouter_objet(0,450 ,-pow(10,-6), 6, 0)
    ajouter_objet(50,450, pow(10,-6), 6, 0)

    ajouter_objet(1600 ,400 , pow(10,-6), -6, 0)
    ajouter_objet(1550 ,400 ,-pow(10,-6), -6, 0)
    ajouter_objet(1600 ,500 ,-pow(10,-6), -6, 0)
    ajouter_objet(1550 ,500 , pow(10,-6), -6, 0)
    ajouter_objet(1600 ,450 , pow(10,-6), -6, 0)
    ajouter_objet(1550 ,450 ,-pow(10,-6), -6, 0)

    ajouter_objet(800 ,0   , pow(10,-6) , 0 , 5)
    ajouter_objet(800 ,100 , -pow(10,-6) , 0 , 5)
    ajouter_objet(800 ,900 ,pow(10,-6) , 0 , -5)
    ajouter_objet(800 ,800 ,-pow(10,-6) , 0 , -5)


horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

# Dessin

fenetre.fill(couleur_fond)

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if (evenement.button == 1):
                ajouter_objet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],pow(10,7),  0,0)
            elif (evenement.button == 3):
                ajouter_objet(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],-pow(10,7), 0,0)

    fenetre.fill(couleur_fond)
    bouger_objets()
    dessiner_objets()
    dessiner_champ(50)


    pygame.display.flip()
    horloge.tick(images_par_seconde)
