# On importe tout les modules qui nous seront utile par la suite.
import pygame, sys, os, random
# On initalise tout le module pygame pour ne pas le rappeler plus tard.
pygame.init()


#On crée les caractéristiques de la fenetre de jeu.
LARGEUR, HAUTEUR, FPS = 1920, 1080, 120
#On crée la fenetre python.
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
#Crée un chrono pour mesurer le temps dans le jeu et limiter la vitesse.
clock = pygame.time.Clock()


#On enregistre les différentes couleurs dans des variables.
FOND_CIEL = (135, 206, 235)
TOIT = (160, 60, 60)
RUE = (50, 53, 60)
BLANC = (255, 255, 255)
ROUGE = (230, 50, 50)
VERT = (50, 220, 90)
BLEU = (50, 120, 255)
ORANGE = (230, 130, 40)
#On enregistre la couleur des nuages avec un 200 supplémentaire pour les rendre un peu transparent.
COULEUR_NUAGE = (255, 255, 255, 200)


#On crée des polices pour définir la taille et forme des différents textes.
p_titre, p_texte, p_petit, p_alerte = pygame.font.SysFont(None, 60), pygame.font.SysFont(None, 34), pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 40)
#Position verticale des toits.
HAUTEUR_TOITS = 700
#Position verticale de la rue.
HAUTEUR_RUE = 1050
#Etat du jeu au début(on est alors au menu!)
etat = "menu"


#Récupère le dossier du code python afin de mettre les images et le fichier 
#python dans le même dossier et ainsi de pouvoir charger les images.
dossier_actuel = os.path.dirname(__file__)

# Essaie de charger l'image ; si ça échoue on passe au except.
try:
    #Charge l'image de facade et la convertit en gardant la transparence du png.
    img_brute = pygame.image.load(os.path.join(dossier_actuel, "facade-immeuble-haussmann-paris.png")).convert_alpha()
    #On séletionne la partie non transparente.
    zone_utile = img_brute.get_bounding_rect()
    #Decoupe l'image pour enlever les marges.
    img_rognee = img_brute.subsurface(zone_utile)
    #Hauteur voulue de l'immeuble.
    hauteur_cible = HAUTEUR_RUE - HAUTEUR_TOITS
    #Coefficient pour atteindre la bonne hauteur.
    ratio = hauteur_cible / img_rognee.get_height()
    #Largeur proportionnelle, arrondie en entier.
    largeur_cible = int(img_rognee.get_width() * ratio)
    #Redimensionne l'image à la taille finale.
    img_immeuble_base = pygame.transform.scale(img_rognee, (largeur_cible, hauteur_cible))
except Exception as e:
    #On affiche un message d'erreur.
    print(f"Erreur image immeuble : {e}")
    #On défini la largeur.
    largeur_cible = 250
    #On remplace l'imeuble par un carré moche.
    img_immeuble_base = pygame.Surface((largeur_cible, HAUTEUR_RUE - HAUTEUR_TOITS))
    #La remplit de couleur pour remplacer l'image manquante.
    img_immeuble_base.fill(TOIT)

#Mémorise la largeur d'un immeuble.
img_w = img_immeuble_base.get_width()

# On essaye de charger l'image du fourgon de police ou on le remplace.
try:
    #On charge l'image.
    img_fourgon_brut = pygame.image.load(os.path.join(dossier_actuel, "Fourgon.png")).convert_alpha()
    #Taille voulue du fourgon: largeur 220, et hauteur 120.
    f_w, f_h = 220, 120
    # Redimensionne l'image à cette taille.
    img_fourgon = pygame.transform.scale(img_fourgon_brut, (f_w, f_h))
except Exception as e:
    #On affiche l'erreur dans la console.
    print(f"Erreur image Fourgon : {e}")
    #Définit la taille du fourgon même si pas chargé.
    f_w, f_h = 220, 120
    #Crée un rectangle vide
    img_fourgon = pygame.Surface((f_w, f_h))
    #Colorie le rectange vide en gris.
    img_fourgon.fill((80, 80, 80))

# On essaye de charger les poubelles.
try:
    #Essaye de charger l'image des poubelles.
    img_poubelles_brut = pygame.image.load(os.path.join(dossier_actuel, "poubelles.png")).convert_alpha()
    #Taille voulue pour les poubelles.
    p_w, p_h = 90, 75
    #Redimensionne l'image.
    img_poubelles = pygame.transform.scale(img_poubelles_brut, (p_w, p_h))
except Exception as e:
    #Affiche l'erreur dans la console.
    print(f"Erreur image Poubelles : {e}")
    #Taille voulue pour les poubelles.
    p_w, p_h = 90, 75
    #Crée un rectangle vide de remplacement.
    img_poubelles = pygame.Surface((p_w, p_h))
    #Colore le rectangle en gris.
    img_poubelles.fill((100, 100, 100))

#Création du rectangle de l'échelle.
echelle = pygame.Rect(400, HAUTEUR_TOITS, 50, HAUTEUR_RUE - HAUTEUR_TOITS)
#Liste vide qui contiendra les immeubles.
plateformes = []
#Largeur de chaque immeuble en multipliant la valeur de base(3= fois 3).
sequence_batiments = [1, 1, 2, 1, 3, 1, 1, 2, 1, 3, 1, 2, 1, 1, 3, 1, 2, 1]
#Position du premier immeuble.
current_x = 450
#Espace de départ entre deux immeubles
base_gap = 180

#On assigne à chaque immeuble un numéro.
for i, mult in enumerate(sequence_batiments):
    #Largeur réelle de cet immeuble en pixels.
    largeur_plat = img_w * mult
    #Ajoute le rectangle de cet immeuble.
    plateformes.append(pygame.Rect(current_x, HAUTEUR_TOITS, largeur_plat, HAUTEUR_RUE - HAUTEUR_TOITS))
    #Calcule l'espace avant le prochain immeuble. Grandit de 12px à chaque immeuble.
    gap_progressif = base_gap + int(i * 12)
    #Avance la position.
    current_x += largeur_plat + gap_progressif

#Coordonnée de la fin de zone des toits plus un peu de marge.
LIMITE_FIN = current_x - gap_progressif + 150
#Largeur totale du niveau.
LARGEUR_MONDE = LIMITE_FIN + 800

#Rectangle du drap des pompiers.
drap = pygame.Rect(plateformes[-1].right - 50, HAUTEUR_RUE - 30, 350, 30)
#Personnage d'arrivé nommé "manif".
bonhomme = pygame.Rect(LARGEUR_MONDE - 300, HAUTEUR_RUE - 80, 40, 80)

#Liste des fourgons.
liste_fourgons = [
    pygame.Rect(950, HAUTEUR_RUE - f_h, f_w, f_h),                             
    pygame.Rect(LIMITE_FIN + 300, HAUTEUR_RUE - f_h, f_w, f_h),                 
    pygame.Rect(LIMITE_FIN + 650, HAUTEUR_RUE - f_h, f_w, f_h)                  
]

#Liste des poubelles.
liste_poubelles = [
    pygame.Rect(LIMITE_FIN + 180, HAUTEUR_RUE - p_h, p_w, p_h),
    pygame.Rect(LIMITE_FIN + 530, HAUTEUR_RUE - p_h, p_w, p_h)
]

#Utilise le hasard pour générer les nuages.
random.seed(42)
#Liste vide qui contiendra les nuages.
nuages = []
for _ in range(35):
    #Position x alétoire du nuage.
    nx = random.randint(-500, LARGEUR_MONDE + 500)
    #position y aléatoire, dans le ciel au dessus des toit.
    ny = random.randint(50, HAUTEUR_TOITS - 100)
    #Largeur alétoire du nuage.
    nw = random.randint(180, 400)
    #Hauteur alétoire du nuage.
    nh = random.randint(40, 90)
    #Ajoute le nuage sous forme de 4 valeurs.
    nuages.append((nx, ny, nw, nh))

#Point de vie et endurance de départ.
vies, endurance = 100, 100
#Position de spawn du joueur.
jx, jy, jl, jh = 100, HAUTEUR_RUE - 85, 45, 85
#Vitesse horizontale 7, vitesse verticale 0, gravité 0.55 par image, vitesse de saut - 15 (négatif = vers le haut)
jvx, jvy, gravite, saut = 7, 0, 0.55, -15
#Le joueur n'est pas au sol au départ (évite que ça bug).
au_sol, coyote = False, 0
#Temps passé près d'un fourgon, en secondes.
temps_proximite_menace = 0.0

def reset():
    #Autorise la fonction à modifier ces variables extérieures.
    global jx, jy, jvy, au_sol, vies, endurance, temps_proximite_menace
    #Replace le joueur à gauche, sur la rue, au sol.
    jx, jy, jvy, au_sol, vies, endurance, temps_proximite_menace = 100, HAUTEUR_RUE - jh, 0, True, 100, 100, 0.0

#Appelle la fonction pour initaliser la partie.
reset()

dt = 0.0  # Initialisation sécurisée de dt

while True:
    #Parcourt tous les événements.
    for e in pygame.event.get():
        #Si on clique sur la croix OU qu'on appuie sur Echap.
        if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            #Ferme pygame puis arrête le programme.
            pygame.quit(); sys.exit()
        #Si une touche vient d'être enfoncé.
        if e.type == pygame.KEYDOWN:
            #Si c'est Entrée ET qu'on est sur un écran de menu.
            if e.key == pygame.K_RETURN and etat in ["menu", "game_over", "victoire", "interpellation"]:
                #Lance la partie et remet le joueur à l'état de départ.
                etat = "jeu"; reset()
            #Si c'est espace et qu'on touche le sol et qu'on joue.
            if e.key == pygame.K_SPACE and (au_sol or coyote > 0) and etat == "jeu":
                #Consomme 10 d'endurance par saut (sans descendre sous 0)
                endurance = max(0, endurance - 10)
                #Donne la vitesse de saut vers le haut, plus au sol, délai coyote annulé.
                jvy, au_sol, coyote = saut, False, 0

    #Tout ce bloc s'éxécute durant la partie.
    if etat == "jeu":
        #Récupère l'état de toutes les touches actullement enfoncés.
        keys = pygame.key.get_pressed()
        #Sprint actif si maj gauche ou droit tenu et suffisament d'endurance.
        sprint = (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and endurance > 5
        # vitesse = 7 fois 1,4 pour le sprint et sinon 7.
        vitesse = jvx * 1.4 if sprint else jvx
        
        #régénération de la stamina.
        endurance = max(0, endurance - 0.45) if sprint else min(100, endurance + 0.08)

        #Gestion de la flèche gauche et droite pour les déplacements latéraux.
        if keys[pygame.K_LEFT]: jx -= vitesse
        if keys[pygame.K_RIGHT]: jx += vitesse

        #Crée le rectangle de collision du joueur à sa position actuelle
        r_joueur = pygame.Rect(jx, jy, jl, jh)

        #Gestion de l'échelle.
        sur_echelle = r_joueur.colliderect(echelle)
        #Vrai si le joueur touche l'échelle.
        if sur_echelle and (keys[pygame.K_UP] or keys[pygame.K_z] or keys[pygame.K_DOWN] or keys[pygame.K_s]):
            #Si la touche haut ou Z est enfoncé.
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                #Vitesse verticale -5.
                jvy = -5
            #Si la touche bas ou S est enfoncé.
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                #Vitesse verticale 5.
                jvy = 5
            #Sinon
            else:
                #Pas de mouvements verticale.
                jvy = 0
            #Permet de sauter depuis l'échelle car elle est identifié comme le sol.
            au_sol = True
        else:
            #La gravité augmente la vitesse de chute à chaque image.
            jvy += gravite

        #Déplace le joueur verticalement selont sa vitesse.
        jy += jvy
        #Si au sol délai de grâce est rechargé à 12 images, sinon il diminue.
        coyote = 12 if au_sol else max(0, coyote - 1)
        #On remet au_sol à faux.
        au_sol = False
        #On recrée le joueur à la nouvelle position.
        r_joueur = pygame.Rect(jx, jy, jl, jh)

        #Rectangle au sol de toute la largeur du monde (c'est la rue).
        sol_rect = pygame.Rect(0, HAUTEUR_RUE, LARGEUR_MONDE, HAUTEUR)
        #Si le joueur tombe sur le sol et ses pied viennent par le dessus.
        if r_joueur.colliderect(sol_rect) and jvy > 0 and jy + jh - jvy <= HAUTEUR_RUE + 15:
            #Pose le joueur sur la rue et annule sa vitesse.
            jy, jvy, au_sol = HAUTEUR_RUE - jh, 0, True

        #Au début on suppose qu'il n'est pas près d'un fourgon.
        proche_menace_cette_frame = False
        #Pour chaque fourgon.
        for f_rect in liste_fourgons:
            #Mur invisible: le fourgon bloque sur toute la hauteur, des toits à la rue.
            mur_vertical_complet = pygame.Rect(f_rect.x, HAUTEUR_TOITS, f_rect.w, HAUTEUR_RUE - HAUTEUR_TOITS)
            #Si le joueur touche ce mur.
            if r_joueur.colliderect(mur_vertical_complet):
                #Si il vient de la gauche.
                if vitesse > 0 and r_joueur.right >= f_rect.left and jx < f_rect.left:
                    #Le remet à gauche (il ne passe pas).
                    jx = f_rect.left - jl
                #Si il vient de la droite.
                elif vitesse < 0 and r_joueur.left <= f_rect.right and jx > f_rect.right:
                    #Le remet à droite (il ne passe pas).
                    jx = f_rect.right

            #zone de danger autour du fourgon: 120px de chaque coté.
            zone_arrestation = pygame.Rect(f_rect.x - 120, HAUTEUR_RUE - jh - 20, f_rect.w + 240, jh + 40)
            
            #Si le joeur touche la zone d'arrestation.
            if r_joueur.colliderect(zone_arrestation):
                #Marque qu'une menace est proche.
                proche_menace_cette_frame = True

        #Pour chaque poubelle
        for pub in liste_poubelles:
            #Si le joueur touche cette poubelle.
            if r_joueur.colliderect(pub):
                #S'il tombe et arrive par dessus.
                if jvy > 0 and jy + jh - jvy <= pub.y + 15:
                    #se pose sur la poubelle.
                    jy, jvy, au_sol = pub.y - jh, 0, True
                #Sinon si il arrive par la gauche.
                elif vitesse > 0 and r_joueur.right >= pub.left and jx < pub.left:
                    #Le bloque sur le coté gauche.
                    jx = pub.left - jl
                #Sinon si il arrive par la droite.
                elif vitesse < 0 and r_joueur.left <= pub.right and jx > pub.right:
                    #Le bloque sur le coté droit.
                    jx = pub.right

        #Si le joueur est prêt d'un fourgon.
        if proche_menace_cette_frame:
            #Le timer augmente un peu le temps écoulé depuis la dernière image pour la jouabilité.
            temps_proximite_menace += dt
            #Si il y reste plus ou durant 2.5 secondes.
            if temps_proximite_menace >= 2.5:
                #définir l'état sur interpellation.
                etat = "interpellation"
        else:
            #Le timer redescend 1.5 fois plus vite qu'il ne monte.
            temps_proximite_menace = max(0.0, temps_proximite_menace - dt * 1.5)

        #Pour chaque immeuble.
        for p in plateformes:
            #Si le joueur le touche.
            if r_joueur.colliderect(p):
                #Seulement si il est au niveau des toits.
                if jy < HAUTEUR_TOITS + 20:
                    #S'il arrive par le dessus.
                    if jvy > 0 and jy + jh - jvy <= p.y + 15: 
                        #Il se pose sur le toit.
                        jy, jvy, au_sol = p.y - jh, 0, True
                    #Sinon si il arrive par la gauche.
                    elif vitesse > 0 and r_joueur.right >= p.left and jx < p.left: 
                        #Il est bloqué contre le mur gauche.
                        jx = p.left - jl
                    #Sinon si il arrive par la droite.
                    elif vitesse < 0 and r_joueur.left <= p.right and jx > p.right: 
                        #Il est bloqué contre le mur droite.
                        jx = p.right

        #Si le joeur tombe sur le drap par dessus.
        if r_joueur.colliderect(drap) and jvy > 0 and jy + jh - jvy <= drap.y + 15: 
            #Il se pose sans subir de dégats.
            jy, jvy, au_sol = drap.y - jh, 0, True
        #Si le joueur touche le personnage d'arrivée.
        if r_joueur.colliderect(bonhomme): 
            #C'est gagné.
            etat = "victoire"
        #début de la zone de danger.
        limite_degats_x = liste_fourgons[0].right if liste_fourgons else 950
        #Si le joueur est entre les toit, sous leurs niveau, pas encore dans la rue, sans appuie, hors sol, et hors drap.
        if limite_degats_x < jx < plateformes[-1].left and jy > HAUTEUR_TOITS + 40 and jy < HAUTEUR_RUE - 20 and not au_sol and not r_joueur.colliderect(sol_rect) and not r_joueur.colliderect(drap):
            #Les points de vie tombent à 0
            vies = 0
            #On passe l'état à perdu.
            etat = "game_over"
        
        #Empêche le joueur de sortir du monde.
        jx = max(0, min(jx, LARGEUR_MONDE - jl))

    #efface l'écran en le remplissant du ciel bleu.
    fenetre.fill(FOND_CIEL)
    
    #Decallage horizontale de la caméra sur le joeur à lécran(la caméra suit le joeur.)
    cx = max(0, min(jx - LARGEUR // 2, LARGEUR_MONDE - LARGEUR))
    #Décallage verticale inexistant.
    cy = 0

    #si on est dans le menu.
    if etat == "menu":
        #On affiche le titre avec police titre en blanc.
        t = p_titre.render("17 OCTOBRE 2026 : LA MANIFESTATION", True, BLANC)
        #Met le titre au centre de l'écran.
        fenetre.blit(t, (LARGEUR//2 - t.get_width()//2, 350))
        #Affiche la consigne en vert au milieu.
        fenetre.blit(p_texte.render("Appuyez sur [ ENTRÉE ] pour commencer", True, VERT), (LARGEUR//2 - 200, 480))
    #si on a perdu1.
    elif etat == "game_over":
        #On affiche le titre avec police titre en rouge.
        t = p_titre.render("MISSION COMPROMISE (CHUTE DANS LE VIDE)", True, ROUGE)
        #Met le titre au centre de l'écran.
        fenetre.blit(t, (LARGEUR//2 - t.get_width()//2, 400))
        #Affiche la consigne en vert au milieu.
        fenetre.blit(p_texte.render("Appuyez sur [ ENTRÉE ] pour recommencer", True, VERT), (LARGEUR//2 - 220, 520))
    #si on a perdu2.
    elif etat == "interpellation":
        #On affiche le titre avec police titre en rouge.
        t = p_titre.render("INTERPELLÉ PAR LES FORCES DE L'ORDRE !", True, ROUGE)
        #Met le titre au centre de l'écran.
        fenetre.blit(t, (LARGEUR//2 - t.get_width()//2, 400))
        #Affiche la consigne en vert au milieu.
        fenetre.blit(p_texte.render("Appuyez sur [ ENTRÉE ] pour recommencer", True, VERT), (LARGEUR//2 - 220, 520))
    #si on a gagné
    elif etat == "victoire":
        #On affiche le titre avec police titre en vert.
        t = p_titre.render("VICTOIRE ! VOUS AVEZ REJOINT LE GROUPE !", True, VERT)
        #Met le titre au centre de l'écran.
        fenetre.blit(t, (LARGEUR//2 - t.get_width()//2, 400))
        #Affiche la consigne en vert au milieu.
        fenetre.blit(p_texte.render("Appuyez sur [ ENTRÉE ] pour rejouer", True, BLANC), (LARGEUR//2 - 180, 520))
    #sinon
    else:
        #Les nuages bougent à la moitié de la vitesse de la caméra.
        parallax_cx = cx * 0.5
        #Pour chaque nuage (position et taille).
        for nx, ny, nw, nh in nuages:
            #Crée une image transparente (support du nuage).
            surf_nuage = pygame.Surface((nw, nh), pygame.SRCALPHA)
            #Dessine une ellipse blanche semitransparente.
            pygame.draw.ellipse(surf_nuage, COULEUR_NUAGE, (0, 0, nw, nh))
            #Colle le nuage à l'écran, décalé par la camera ralentie.
            fenetre.blit(surf_nuage, (int(nx - parallax_cx), ny))

        #On dessine l'asphalte gris sur toute la largeur du monde.
        pygame.draw.rect(fenetre, RUE, (0 - cx, HAUTEUR_RUE - cy, LARGEUR_MONDE, HAUTEUR * 2))
        #Dessine le trottoir (bande plus claire de 15px)
        pygame.draw.rect(fenetre, (70, 75, 85), (0 - cx, HAUTEUR_RUE - cy, LARGEUR_MONDE, 15))
        
        #Tout les 140 px.
        for lx in range(0, LARGEUR_MONDE, 140):
            #Trait de route 1.
            pygame.draw.rect(fenetre, (200, 200, 210), (lx - cx, HAUTEUR_RUE + 40 - cy, 70, 6))
            #Trait de route 2.
            pygame.draw.rect(fenetre, (200, 200, 210), (lx - cx, HAUTEUR_RUE + 120 - cy, 70, 6))
            #Trait de route 3.
            pygame.draw.rect(fenetre, (200, 200, 210), (lx - cx, HAUTEUR_RUE + 200 - cy, 70, 6))

        #Dessine l'échelle.
        pygame.draw.rect(fenetre, (180, 140, 60), (echelle.x - cx, echelle.y - cy, echelle.w, echelle.h))
        #Pour chauqe position verticale tout les 30 px sur l'échelle.
        for ey in range(echelle.y, echelle.y + echelle.h, 30):
            #Dessine un barreau pour l'échelle.
            pygame.draw.rect(fenetre, (120, 90, 30), (echelle.x - cx, ey - cy, echelle.w, 6))
        
        #Si le joueur est au-dessus de la ligne des toits.
        if jy < HAUTEUR_TOITS:
            #Décalage visuel de 45px vers le bas.
            decalage_visuel_y = 45 if jy <= HAUTEUR_TOITS + 5 else 0
            #Dessine le corp du joueur.
            pygame.draw.rect(fenetre, BLEU, (jx - cx, jy - cy + 25 + decalage_visuel_y, jl, jh - 25))
            #Dessine la tête du joueur.
            pygame.draw.rect(fenetre, (240, 205, 170), (jx - cx + 7, jy - cy + decalage_visuel_y, 30, 28))

        #Pour chaque immeuble.
        for p in plateformes:
            #Etire l'image de façade à la largeur exacte de cet immeuble.
            img_batiment = pygame.transform.scale(img_immeuble_base, (p.w, HAUTEUR_RUE - HAUTEUR_TOITS))
            #Colle l'imeuble à l'écran.
            fenetre.blit(img_batiment, (p.x - cx, p.y - cy))

        #Si le joueur est au niveau des toits ou plus bas.
        if jy >= HAUTEUR_TOITS:
            #Dessine le corp par dessus les immeubles.
            pygame.draw.rect(fenetre, BLEU, (jx - cx, jy - cy + 25, jl, jh - 25))
            #Dessine la tête.
            pygame.draw.rect(fenetre, (240, 205, 170), (jx - cx + 7, jy - cy, 30, 28))

        #Dessine le drap des pompiers.
        pygame.draw.rect(fenetre, (255, 120, 120), (drap.x - cx, drap.y - cy, drap.w, drap.h))
        #Perso d'arrivé avec t shirt vert.
        pygame.draw.rect(fenetre, VERT, (bonhomme.x - cx, bonhomme.y - cy + 25, bonhomme.w, bonhomme.h - 25))
        #dessine sa tête.
        pygame.draw.rect(fenetre, (240, 205, 170), (bonhomme.x - cx + 5, bonhomme.y - cy, 30, 28))
        
        #Pour chaque fourgon.
        for f_rect in liste_fourgons:
            #Met le fourgon sur sa position.
            fenetre.blit(img_fourgon, (f_rect.x - cx, f_rect.y - cy))
        
        #Pour chaque poubelle.
        for pub in liste_poubelles:
            #Colle l'image des poubelles à sa position.
            fenetre.blit(img_poubelles, (pub.x - cx, pub.y - cy))
            
        #Si le timer commence.
        if temps_proximite_menace > 0:
            #Montre le temps qu'il reste avant l'interpellation.
            temps_restant = max(0.0, 2.5 - temps_proximite_menace)
            #Crée le texte d'alerte avec 1 décimale.
            txt_timer = p_alerte.render(f"RISQUE D'INTERPELLATION : {temps_restant:.1f}s", True, ROUGE)
            #L'alerte est centré en haut de l'écran.
            fenetre.blit(txt_timer, (LARGEUR // 2 - txt_timer.get_width() // 2, 120))

        #Dessine le fond sombre du panneau d'infos.
        pygame.draw.rect(fenetre, (15, 15, 25), (30, 40, 420, 100), border_radius=8)
        #Dessine le contour blanc du panneau.
        pygame.draw.rect(fenetre, BLANC, (30, 40, 420, 100), 2, border_radius=8)
        
        #Dessine le fond gris de la barre de vie.
        pygame.draw.rect(fenetre, (60, 60, 70), (50, 55, 380, 18), border_radius=4)
        #Si vivant, dessine la partie rouge proportionnelle à la vie.
        if vies > 0: pygame.draw.rect(fenetre, ROUGE, (50, 55, int((vies/100)*380), 18), border_radius=4)
        #Ecrite "VIE" au dessus de la barre.
        fenetre.blit(p_petit.render(f"VIE : {int(vies)} / 100", True, BLANC), (60, 56))

        #Dessine le fond gris de la barre d'endurance.
        pygame.draw.rect(fenetre, (60, 60, 70), (50, 80, 380, 18), border_radius=4)
        #Dessine la barre d'endurance orange.
        pygame.draw.rect(fenetre, ORANGE, (50, 80, int((endurance/100)*380), 18), border_radius=4)
        #Ecris "ENDURANCE" au dessus de la barre.
        fenetre.blit(p_petit.render(f"ENDURANCE : {int(endurance)}%", True, BLANC), (60, 81))

    #Affiche à l'écran tout ce qui vient d'être dessiné en arrière plan.
    pygame.display.flip()
    #Utilise les fps récupéré plus tot et récupère le temps écoulé pour la prochaine frame.
    dt = clock.tick(FPS) / 1000.0
