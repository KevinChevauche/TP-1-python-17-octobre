import pygame
import sys
import os

pygame.init()

# --- CONSTANTES ---
LARGEUR = 1250
HAUTEUR = 600
FPS = 60
GRAVITE = 1
VITESSE_JOUEUR = 5
SAUT_JOUEUR = 18

COULEUR_CIEL = (0, 0, 255)
COULEUR_SOL = (102, 102, 102)
COULEUR_PLATEFORME = (0,255,0)
COULEUR_JOUEUR = (255,0,0)
COULEUR_MENU = (115, 38, 23)
COULEUR_IMEUBLE = (255, 145, 0)
COULEUR_ECHELLE = (186, 62, 0)
COULEUR_REP = (212, 0, 255)

#Dossier dans lequel se trouve les visuels ----
dossier_actuel = os.path.dirname(__file__)

#Etat du jeu au lencement donc menu
etat = "menu"

# --- FENÊTRE ---
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("test_jeu_POO")
clock = pygame.time.Clock()

# --- CLASSES ---
class Joueur(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(COULEUR_JOUEUR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 0
        self.vy = 0
        self.saute = False
    #Méthode qui mets à jour la position du joueur en fonction 
    #des collisions aves les plateformes et les echelles

    def update(self, plateformes, sur_echelle=False):

        if not sur_echelle:
            self.vy += GRAVITE

        if self.vy > 10:
            self.vy = 10

        self.rect.x += self.vx
        self._collision_x(plateformes)

        self.rect.y += self.vy
        self._collision_y(plateformes)

    #Méthode des collisions
    def _collision_x(self, plateformes):
        for p in plateformes:
            if self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.rect.right = p.rect.left
                elif self.vx < 0:
                    self.rect.left = p.rect.right

        

    def _collision_y(self, plateformes):
        for p in plateformes:
            if self.rect.colliderect(p.rect):
                if self.vy > 0:
                    self.rect.bottom = p.rect.top
                    self.vy = 0
                    self.saute = False
                elif self.vy < 0:
                    self.rect.top = p.rect.bottom
                    self.vy = 0

    #Méthode pour le saut
    def jump(self, plateformes):
        self.rect.y += 2
        collisions = any(self.rect.colliderect(p.rect) for p in plateformes)
        self.rect.y -= 2
        if collisions and not self.saute:
            self.vy = -SAUT_JOUEUR
            self.saute = True
    def collision_echelle(self, echelles):
        return any(self.rect.colliderect(e.rect) for e in echelles)

    
    def victoire(self, rep):
        return self.rect.colliderect(rep.rect)
    
        
    

        

class Plateforme(pygame.sprite.Sprite):
    def __init__(self, x, y, largeur, hauteur):
        super().__init__()
        self.image = pygame.Surface((largeur, hauteur))
        self.image.fill(COULEUR_PLATEFORME)
        self.rect = self.image.get_rect(topleft=(x, y))

class Imeuble(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((270,358))
        self.image.fill(COULEUR_IMEUBLE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Echelle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((35, 324))
        self.image.fill(COULEUR_ECHELLE)
        self.rect = self.image.get_rect(topleft=(x, y))

class Republique(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((442, 574))
        self.image.fill(COULEUR_REP)
        self.rect = self.image.get_rect(topleft=(x, y))

class Fourgon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((333, 187))
        self.image.fill(COULEUR_JOUEUR)
        self.rect = self.image.get_rect(topleft=(x, y))






# --- CRÉATION DES ÉLÉMENTS ---
toutes_les_sprites = pygame.sprite.Group()
plateformes = pygame.sprite.Group()
imeubles = pygame.sprite.Group()
echelles = pygame.sprite.Group()
fourgons = pygame.sprite.Group()

joueur = Joueur(0, 500)
rep = Republique(2558, 0)
toutes_les_sprites.add(joueur)
toutes_les_sprites.add(rep)



# Sol et plateformes


niveau = [
    #Sol
    (-150, 560, 3500, 40),
    #toits
    (261, 248, 255, 28),
    (700, 248, 486, 28),
    (1291, 248, 255, 28),
    (1647, 248, 255, 28),
    (2010, 248, 466, 28)

]

for x, y, w, h in niveau:
    p = Plateforme(x, y, w, h)
    plateformes.add(p)
    toutes_les_sprites.add(p)

batiment = [

    (239, 244),
    (690, 244),
    (939, 244),
    (1287, 244),
    (1642, 244),
    (1998, 244),
    (2231, 244)
]

for x,y in batiment:
    b = Imeuble(x, y)
    imeubles.add(b)
    toutes_les_sprites.add(b)


entree_sortie = [
    (225, 249),
    (2482,249)

]
for x,y in entree_sortie:
    es = Echelle(x, y)
    echelles.add(es)
    toutes_les_sprites.add(es)





# --- CAMERA (défilement horizontal) ---
camera_x = 0


# Boucle de menu -----
while etat == "menu":
    en_cours = False
    toutes_les_sprites.remove(joueur, p)
    

    for event in pygame.event.get():
       if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                etat = "Jeu"
                en_cours= True

    
    

    # --- AFFICHAGE DU MENU ---
    fenetre.fill(COULEUR_MENU)
    for sprite in toutes_les_sprites:
        rect_decal = sprite.rect.move(camera_x, 0)
        fenetre.blit(sprite.image, rect_decal)
    pygame.display.flip()
    

# --- BOUCLE DE JEU ---
en_cours = True
while en_cours:
    toutes_les_sprites.add(joueur, plateformes)
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_cours = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                joueur.jump(plateformes)

    touches = pygame.key.get_pressed()
    joueur.vx = 0
    if touches[pygame.K_LEFT]:
        joueur.vx = -VITESSE_JOUEUR
    if touches[pygame.K_RIGHT]:
        joueur.vx = VITESSE_JOUEUR

    
    # Détection de l'échelle
    sur_echelle = joueur.collision_echelle(echelles)

    # Déplacement vertical
    if sur_echelle:
        if touches[pygame.K_UP]:
            joueur.vy = -5
        elif touches[pygame.K_DOWN]:
            joueur.vy = 5
        else:
            joueur.vy = 0
    else:
        # On quitte l'échelle
        pass
    fin_de_partie = joueur.victoire(rep)
    #Condition de la victoire------
    if fin_de_partie:
        etat="menu"
    # Mise à jour du joueur
    joueur.update(plateformes, sur_echelle)

    # --- Camera suit le joueur ---
    camera_x = -(joueur.rect.x - LARGEUR // 2)

    
        

    # --- AFFICHAGE ---
    fenetre.fill(COULEUR_CIEL)
    for sprite in toutes_les_sprites:
        rect_decal = sprite.rect.move(camera_x, 0)
        fenetre.blit(sprite.image, rect_decal)

    

    pygame.display.flip()

pygame.quit()
sys.exit()
