# ------------------------------------------------------------------------
# Laboratoires de programmation mathématique et physique 1
# ------------------------------------------------------------------------
#
# Programme 4: Affichage de vecteurs.
#
# *** CONSIGNES ***: Ne modifier que les fonctions
#                        deplacer_pol() et
#                        dessiner_vecteur()  !!!
#
# ------------------------------------------------------------------------

import math
import pygame
import sys

### Constante(s)

JAUNEMIEL = (255, 192, 0)
NOIR = (0, 0, 0)

A = 2
B = 5
C = 20


### Fonctions

# *** A MODIFIER *********************************************************

def deplacer_pol(point, distance, orientation):
    x, y = point

    x = point[0] + (distance * math.cos(orientation))
    y = point[1] + (distance * math.sin(orientation))

    return (x, y)

# *** A MODIFIER *********************************************************

def dessiner_vecteur(fenetre, couleur, origine, vecteur):

    p = origine
    p4 = p + vecteur
    angle = math.atan2(vecteur[1], vecteur[0])

    if math.sqrt(vecteur[1]**2 + vecteur[0]**2) >= C:
        p4 = (p[0] + vecteur[0], p[1] + vecteur[1])
        pp4 = math.sqrt(vecteur[1]**2 + vecteur[0]**2)
        p1 = deplacer_pol(p, A, angle - math.pi/2)
        p7 = deplacer_pol(p, A, angle + math.pi/2)
        p2 = deplacer_pol(p1, pp4 - C, angle)
        p6 = deplacer_pol(p7, pp4 - C, angle)
        p3 = deplacer_pol(p2, B, angle - math.pi/2)
        p5 = deplacer_pol(p6, B, angle + math.pi/2)

        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4, p5, p6, p7])

    else:
        p3 = (p[0] + vecteur[0], p[1] + vecteur[0])
        p1 = deplacer_pol(p3, C, angle + math.pi)
        p2 = deplacer_pol(p1, A + B, angle - math.pi/2)
        p4 = deplacer_pol(p1, A + B, angle + math.pi/2)

        pygame.draw.polygon(fenetre, couleur, [p1, p2, p3, p4])

# ************************************************************************

def traiter_clic(position, bouton):
    global premier_clic, ancienne_position

    if bouton == 3:
        premier_clic = True
        fenetre.fill(couleur_fond)
        return

    if bouton != 1:
        return

    if premier_clic:
        premier_clic = False
    else:
        dessiner_vecteur(fenetre, NOIR, ancienne_position,
                         (position[0] - ancienne_position[0],
                          position[1] - ancienne_position[1]))

    ancienne_position = position
    return

### Paramètre(s)

dimensions_fenetre = (800, 600)  # en pixels
images_par_seconde = 25

### Programme

# Initialisation

pygame.init()

fenetre = pygame.display.set_mode(dimensions_fenetre)
pygame.display.set_caption("Programme 4");

horloge = pygame.time.Clock()
couleur_fond = JAUNEMIEL

premier_clic = True

fenetre.fill(couleur_fond)

# Boucle principale

while True:
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            pygame.quit()
            sys.exit();
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            traiter_clic(evenement.pos, evenement.button)

    pygame.display.flip()
    horloge.tick(images_par_seconde)
