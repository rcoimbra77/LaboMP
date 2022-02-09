#Nicolas Schneiders
import math
import pygame
import sys

# Constantes

NOIR = (0, 0, 0)
ROUGE = (255, 0, 0)
ORANGE = (255, 100, 10)
JAUNE = (255,255,0)
BLEU_CLAIR = (0, 255, 255)

G = 0.001

# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

# Variables

position_vaisseau = [100,100]
orientation_vaisseau = 0

compteur_propulseur = 0

position_planete = [0,0]
planete_up = False
masse_planete = 0


### Fonctions d'affichage ###


def dessiner_triangle(fenetre, couleur_turb, p, r, a, b):
    p1 = [p[0] + math.cos(a+b) * r , p[1] - math.sin(a+b) * r]
    p2 = [p[0] + math.cos(a-b) * r , p[1] - math.sin(a-b) * r]
    pygame.draw.polygon(fenetre, couleur_turb, [p, p1, p2])



def afficher_vaisseau(fenetre, couleur_vaisseau, rayon_vaisseau, couleur_turb ,position_vaisseau ,r ,a ,b):
    global compteur_propulseur
    p = position_vaisseau
    if compteur_propulseur > 0:
        dessiner_triangle(fenetre, JAUNE, p, 38, orientation_vaisseau + 21 * math.pi /20, math.pi /30)
        dessiner_triangle(fenetre, JAUNE, p, 38, orientation_vaisseau + 19 * math.pi /20, math.pi /30)
        compteur_propulseur -= 1
    dessiner_triangle(fenetre, couleur_turb, p, r, a, b)
    pygame.draw.circle(fenetre, couleur_vaisseau, p, rayon_vaisseau)



def afficher_planete(fenetre, position_planete, planete_up, couleur_planete, rayon_planete):
    if planete_up:
        pygame.draw.circle(fenetre, couleur_planete, position_planete, rayon_planete)


### Fonctions de calcul des mrua ###

def maj_position(position_objet, temps_mtn, masse_objet, force_poussee, orientation_objet, masse_planete, position_planete, planete_up):
    global compteur_propulseur, vx, vy, t0
    if planete_up:
        (acc_gravx, acc_gravy) = calcul_acc_grav(position_objet, position_planete, masse_objet, masse_planete)

    else:
        (acc_gravx, acc_gravy) = (0,0)

    if compteur_propulseur>0:
        a = force_poussee/masse_objet
        (ax, ay) = (a * math.cos(orientation_objet), -a * math.sin(orientation_objet))

    else:
        (ax, ay) = (0,0)

    acc_totx = ax + acc_gravx
    acc_toty = ay + acc_gravy
    deltaT = temps_mtn - t0
    [px,py] = position_objet

    px += vx * deltaT + (acc_totx * deltaT**2)/2
    py += vy * deltaT + (acc_toty * deltaT**2)/2
    vx += acc_totx * deltaT
    vy += acc_toty * deltaT
    t0 = temps_mtn

    return [int(px), int(py)]



def calcul_acc_grav(position_objet, position_planete, masse_objet, masse_planete):
    global G

    (px1,py1) = position_objet
    (px2,py2) = position_planete

    distance_centre_2 = ((px1-px2)**2 + (py1-py2)**2)
    f_attrac = (G*masse_objet*masse_planete) / distance_centre_2
    acc_grav = f_attrac/masse_objet

    vect_VP = [px2-px1, py2-py1]
    norme_VP = norme(vect_VP)
    vect_dir = [vect_VP[0] / norme_VP, vect_VP[1] / norme_VP]

    acc_gravx = vect_dir[0]*acc_grav
    acc_gravy = vect_dir[1]*acc_grav

    return (acc_gravx, acc_gravy)



def norme(vecteur):
    norme = (vecteur[0]**2 + vecteur[1]**2)**(1/2)
    return norme


### Gameplay supplémentaire ###

def pacman_like(position_objet, dimensions_fenetre):
    [px ,py] = position_objet
    [long,larg] = dimensions_fenetre
    if(py > larg + 100):
        py = -100
    elif(py < -100):
        py = larg + 100

    if(px > long + 100):
        px = -100
    elif(px < -100):
        long + 100

    return [px,py]


### Interpreter entrées ###

def gerer_touche():
    global orientation_vaisseau, compteur_propulseur
    if evenement.key == pygame.K_LEFT:
        orientation_vaisseau -= math.pi/20
    elif evenement.key == pygame.K_RIGHT:
        orientation_vaisseau += math.pi/20
    elif evenement.key == pygame.K_UP:
        compteur_propulseur += 3



def gerer_bouton():
    global position_planete, planete_up
    if evenement.button == 1:
        position_planete = evenement.pos
        planete_up = True
    elif evenement.button == 3:
        planete_up = False


### Fonction test ###

def test_collision(position_objet1, position_objet2, rayon1, rayon2, planete_up):
    if planete_up:
        (px1,py1) = position_objet1
        (px2,py2) = position_objet2
        distance_centre = ((px1-px2)**2 + (py1-py2)**2)**(1/2)
        if distance_centre < rayon1 + rayon2 and planete_up:
            pygame.quit()
            sys.exit()



def val_masse_planete(planete_up):
    global masse_planete
    if planete_up:
        masse_planete = 1600
    else:
        masse_planete = 0


# Initialisation

a=0
vx=0
vy=0
t0=0

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 7")

horloge = pygame.time.Clock()
couleur_fond = NOIR

pygame.key.set_repeat(10, 10)

while True:
    temps_mtn = pygame.time.get_ticks()

    for evenement in pygame.event.get():
        if evenement.type == pygame.KEYDOWN:
            gerer_touche()
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            gerer_bouton()
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    ###
    val_masse_planete(planete_up)
    position_vaisseau = pacman_like(position_vaisseau, dimensions_fenetre)
    ###
    fenetre.fill(couleur_fond)
    ###
    afficher_planete(fenetre, position_planete, planete_up, BLEU_CLAIR, 40)
    position_vaisseau = maj_position(position_vaisseau, temps_mtn, 1, 0.0003, orientation_vaisseau, masse_planete, position_planete, planete_up)
    afficher_vaisseau(fenetre, ROUGE, 15, ORANGE, position_vaisseau, 23, orientation_vaisseau + math.pi, math.pi/7)
    ###
    pygame.display.flip()
    test_collision(position_vaisseau, position_planete, 15, 40, planete_up)
    horloge.tick(images_par_seconde)
