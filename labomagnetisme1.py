
import math
import pygame
import sys

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

dimensions_fenetre = (1600, 900)  # en pixels
images_par_seconde = 25
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
        print(couleur)
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

def ajouter_objet(x,y,z):
    objets.append((x,y,z))

def print_objets():
    for o in objets:
        print(o)   


def dessiner_objets():
    for o in objets:
        if (o[2]<0):
            pygame.draw.circle(fenetre, NOIR , (o[0], o[1]), 10)
        else:
            pygame.draw.circle(fenetre, ROUGE, (o[0], o[1]), 10)

def dessiner_champ(pas):
    x = -pas
    while(x < dimensions_fenetre[0] + pas):
        y = -pas
        while(y < dimensions_fenetre[1] + pas):
            vecteur = calculer_champ(x,y)

            if (vecteur != None):

                e = math.sqrt(vecteur[0]*vecteur[0] + vecteur[1]*vecteur[1])
                print(" ")
                print("norme de e:")
                print(e)

                v = math.sqrt(e)/20000 #NON
                print(" ")
                print("v:")
                print(v)
                print(" ")

                if(v >=0 and v<8):
                    couleur = (255,255*v/8,0)
                elif(v >8 and v<=16):
                    couleur = (255-(v-8)/8,255,255*(v-8)/8) 
                elif(v >16 and v<=24):
                    couleur = (0,255-(v-16)/8,255)
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
ajouter_objet(800,200,pow(10,6))
ajouter_objet(800,700,-pow(10,6))


horloge = pygame.time.Clock()
couleur_fond = BLEUCLAIR

# Dessin

fenetre.fill(couleur_fond)

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    fenetre.fill(couleur_fond)
    dessiner_objets()
    dessiner_champ(50)


    pygame.display.flip()
    horloge.tick(images_par_seconde)
