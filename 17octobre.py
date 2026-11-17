#On importe les modules necessaires
import pygame
import sys

#On lance pygame.
pygame.init()

#On défini les propriétés de la fenetre de base.
LARGEUR, HAUTEUR = 1920, 1080

#On crée la fenetre de jeu et le temps.
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("17 octobre 2026")
clock = pygame.time.Clock()

#On défini une police d'écriture pour le texte
police = pygame.font.SysFont(None, 80)

#On défini l'état du jeu actuelle, le joueur est il dans le menu ou en jeu ?
etat_jeu = "menu"
manif = True

#C'est la boucle principale du jeu.
while manif:

    #On parcours la liste de tout les événement crées par l'utilisateur.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            manif = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                manif = False

        #Sur quel page sommes nous ?
        if etat_jeu == "menu":
            etat_jeu = "niveau1"
        elif etat_jeu == "niveau1":
            etat_jeu = "menu"

    fenetre.fill((0, 0, 0))

    #On dessine le texte à l'écran:
    if etat_jeu == "menu":
        texte=police.render("Menu Principal", True, (255, 255, 255))
    elif etat_jeu == "niveau1":
        texte = police.render("Niveau 1 - Cliquez pour retourner au Menu", True, (255, 255, 255))

    fenetre.blit(texte, (600, 500))

    #Affiche la page jusque la invisible au joueur quand elle est chargé.
    pygame.display.flip()
#On ferme le jeu.
pygame.quit()
sys.exit()
