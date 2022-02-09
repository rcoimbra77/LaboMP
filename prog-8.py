import math
import pygame
import sys

# Constantes

BLEU = (0,0,255)
ROUGE = (255, 0, 0)
JAUNEPALE = (255, 255, 192)
a = 0.000165
b = 0
c = -0.055
d = 0
e = 5
# Paramètres

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25
dimensions_terrain = (40, 30)
ratio = dimensions_fenetre[0]/dimensions_terrain[0]
gravite = -9.81
g = (0, gravite)
µ_c = 0.03

# Fonctions

### Initialise les differentes variables ###
def initialisation():
    global temps_precedent, premiere_iteration, position_piste, ancienne_position_piste, vitesse_max, acc_ressentie_max, acc_ressentie_min
    temps_precedent = 0
    premiere_iteration = True
    position_piste = [-dimensions_terrain[0]/2, hauteur(-dimensions_terrain[0]/2)]
    ancienne_position_piste = position_piste
    vitesse_max = 0
    acc_ressentie_max = 0
    acc_ressentie_min = 100


def fenetre_vers_piste(xf, yf):
    xp = -dimensions_terrain[0]/2 + xf/ratio
    yp = dimensions_terrain[1] - yf/ratio
    return xp, yp


def piste_vers_fenetre(xp, yp):
    xf = dimensions_fenetre[0]/2 + ratio*xp
    yf = dimensions_fenetre[1] - ratio*yp
    return xf, yf


def hauteur(x):
    h_x = a*x**4 + b*x**3 + c*x**2 + d*x + e
    return h_x


def dessiner_piste():
    xf, yf = 0, 0
    while xf < dimensions_fenetre[0]:
        xp , yp = fenetre_vers_piste(xf, yf)
        yp = hauteur(xp)
        xr , yr = piste_vers_fenetre(xp, yp) #x rail
        pygame.draw.rect(fenetre,BLEU,((xr ,yr),(1,dimensions_fenetre[0]-yr)))
        xf += 1


def dessiner_mobile(position_piste):
    position_fenetre = piste_vers_fenetre(position_piste[0], position_piste[1])
    pygame.draw.circle(fenetre, ROUGE, (int(position_fenetre[0]), int(position_fenetre[1])), 10)


def norme(vecteur):
    norme = (vecteur[0]**2 + vecteur[1]**2)**(1/2)
    return norme


def calcul_pente(position_piste):
    m = (hauteur(position_piste[0] + 10**(-6)) - hauteur(position_piste[0])) / 10**(-6)
    return m


def vect_unit(pente):
    k = (1 + pente**2)**(1/2)
    if ancienne_vitesse[0] >= 0:
        vect_u = [1/k, pente/k]
    else:
        vect_u = [-1/k, -pente/k]
    return vect_u


def normale(g, pente):
    k = (1 + pente**2)**(1/2)
    normale = [-pente/k, 1/k]
    return normale


def delta_t():
    global t_iteration, t0
    dt = t_iteration - t0
    return dt


def vect_vitesse(vect_unit, norme_vitesse):
    #if ancienne_vitesse[0] >= 0:
    vect_v = [norme_vitesse * vect_unit[0], norme_vitesse * vect_unit[1]]
    #else:
        #vect_v = [-norme_vitesse * vect_unit[0], -norme_vitesse * vect_unit[1]]
    return vect_v


def produit_scalaire(v1, v2):
    pdt_scal = v1[0]*v2[0] + v1[1]*v2[1]
    return pdt_scal


def acc_frottement(vec_acc_propre, n, v_u, µ_c):
    acc_frott = [-µ_c*abs(produit_scalaire(vec_acc_propre, n))*v_u[0], -µ_c*abs(produit_scalaire(vec_acc_propre, n))*v_u[1]]
    return acc_frott


### Résultante de toute les accélération###
def vect_acc(vitesse,g,pente, v_u, µ_c):
    global  ancienne_vitesse, acc_ressentie
    a_piste = [(vitesse[0] - ancienne_vitesse[0])/delta_t(), (vitesse[1] - ancienne_vitesse[1])/delta_t()]
    n = normale(g,pente)
    acc_res_g_n = [-produit_scalaire(g, n)*n[0], -produit_scalaire(g, n)*n[1]]
    acc_ressentie, vec_acc_propre = acc_propre(a_piste, acc_res_g_n)
    acc_frott = acc_frottement(vec_acc_propre, n, v_u, µ_c)
    vect_a = [acc_res_g_n[0] + a_piste[0] + g[0] + acc_frott[0], acc_res_g_n[1] + a_piste[1] + g[1] + acc_frott[1]]
    return vect_a


def acc_propre(acc_piste, acc_res_g_n):
    vec_acc_propre = [acc_piste[0] + acc_res_g_n[0], acc_piste[1] + acc_res_g_n[1]]
    acc_ressentie = norme(vec_acc_propre)
    return acc_ressentie , vec_acc_propre


def maj_vitesse(acc):
    global ancienne_vitesse
    vitesse = [ancienne_vitesse[0] + acc[0]*delta_t(),
    ancienne_vitesse[1] + acc[1]*delta_t()]
    ancienne_vitesse = vitesse
    return vitesse


def maj_position(vitesse):
    global ancienne_position_piste, position_piste
    position_piste = [ancienne_position_piste[0] + vitesse[0]*delta_t(), ancienne_position_piste[1] + vitesse[1]*delta_t()]
    ancienne_position_piste = position_piste
    return position_piste


###Mise à jour de toutes les variables via les différentes fonctions###
def mettre_a_jour(position_piste,temps_mtn,g):
    global premiere_iteration, t0, vitesse, ancienne_vitesse, m, t_iteration
    if premiere_iteration:
        vitesse = [0,0]
        ancienne_vitesse = vitesse
        premiere_iteration = False
        t0 = t_iteration
    else:
        norm_v = norme(vitesse)
        m = calcul_pente(position_piste)
        v_u = vect_unit(m)
        vitesse = vect_vitesse(v_u, norm_v)
        acc = vect_acc(vitesse, g, m, v_u, µ_c)
        tableau_de_bord(norm_v, g)
        vitesse = maj_vitesse(acc)
        position_piste = maj_position(vitesse)
        position_fenetre = piste_vers_fenetre(position_piste[0], position_piste[1])
        t0 = t_iteration
        return position_fenetre


###Permet 40 mise à jour par frame###
def anime(temps_mtn,g):
    global temps_precedent,t_iteration
    while temps_precedent <= temps_mtn-1:
        t_iteration = temps_precedent/1000
        mettre_a_jour(position_piste,t_iteration,g)
        temps_precedent += 1
    temps_precedent = temps_mtn


def tableau_de_bord(vitesse,g):
    global acc_ressentie
    texte_1 = "Vitesse : {0:.2f} m/s".format(vitesse)
    image_1 = police.render(texte_1, True, BLEU)
    fenetre.blit(image_1, (dimensions_fenetre[0]//20, dimensions_fenetre[1]//20))

    texte_3 = "Accélération ressentie : {0:.2f} g".format(acc_ressentie/norme(g))
    image_3 = police.render(texte_3, True, BLEU)
    fenetre.blit(image_3, (dimensions_fenetre[0]//20, dimensions_fenetre[1]//9))

    statistique(vitesse,acc_ressentie)

    texte_2 = "Vitesse max : {0:.2f} m/s".format(vitesse_max)
    image_2 = police.render(texte_2, True, BLEU)
    fenetre.blit(image_2, (dimensions_fenetre[0]//20, dimensions_fenetre[1]//12))

    texte_4 = "Accélération ressentie max : {0:.2f} g".format(acc_ressentie_max/norme(g))
    image_4 = police.render(texte_4, True, BLEU)
    fenetre.blit(image_4, (dimensions_fenetre[0]//20, dimensions_fenetre[1]//7.4))

    texte_5 = "Accélération ressentie min : {0:.2f} g".format(acc_ressentie_min/norme(g))
    image_5 = police.render(texte_5, True, BLEU)
    fenetre.blit(image_5, (dimensions_fenetre[0]//20, dimensions_fenetre[1]//6.3))


def statistique(vitesse,acc_ressentie):
    global vitesse_max,acc_ressentie_max, acc_ressentie_min
    if vitesse > vitesse_max:
        vitesse_max = vitesse

    if acc_ressentie > acc_ressentie_max:
        acc_ressentie_max = acc_ressentie

    if acc_ressentie < acc_ressentie_min:
        acc_ressentie_min =  acc_ressentie


# Initialisation
initialisation()

pygame.init()
police  = pygame.font.SysFont("monospace", 16)
fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 8")

horloge = pygame.time.Clock()
couleur_fond = JAUNEPALE

while True:
    temps_mtn = pygame.time.get_ticks()
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    fenetre.fill(couleur_fond)
    dessiner_piste()
    anime(temps_mtn,g)
    dessiner_mobile(position_piste)
    pygame.display.flip()
    horloge.tick(images_par_seconde)
