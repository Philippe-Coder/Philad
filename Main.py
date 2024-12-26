import pygame
import random
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Jeu d'évitement d'obstacles")

# Couleurs
BLANC = (255, 255, 255)

# Chargement des images
image_joueur = pygame.image.load('joueur.png')
image_obstacle = pygame.image.load('obstacle.png')

# Chargement des sons
son_collision = pygame.mixer.Sound('explosion.ogg')

# Vitesse de rafraîchissement
horloge = pygame.time.Clock()
fps = 30

# Classe pour le joueur
class Joueur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(image_joueur, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (largeur_fenetre // 2, hauteur_fenetre - 50)
        self.vitesse_x = 0

    def update(self):
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            self.vitesse_x = -5
        elif touches[pygame.K_RIGHT]:
            self.vitesse_x = 5
        else:
            self.vitesse_x = 0
        self.rect.x += self.vitesse_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largeur_fenetre:
            self.rect.right = largeur_fenetre

# Classe pour les obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, vitesse):
        super().__init__()
        self.image = pygame.transform.scale(image_obstacle, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, largeur_fenetre - self.rect.width)
        self.rect.y = -self.rect.height
        self.vitesse_y = vitesse

    def update(self):
        self.rect.y += self.vitesse_y
        if self.rect.top > hauteur_fenetre:
            self.rect.x = random.randint(0, largeur_fenetre - self.rect.width)
            self.rect.y = -self.rect.height

# Fonction pour afficher le score
def afficher_score(score):
    police = pygame.font.SysFont(None, 36)
    texte = police.render(f'Score : {score}', True, BLANC)
    fenetre.blit(texte, (10, 10))

# Création des groupes de sprites
tous_les_sprites = pygame.sprite.Group()
groupe_obstacles = pygame.sprite.Group()

# Création du joueur
joueur = Joueur()
tous_les_sprites.add(joueur)

# Variables de jeu
score = 0
vitesse_obstacle = 5
intervalle_obstacle = 2000  # Intervalle en millisecondes
dernier_temps_obstacle = pygame.time.get_ticks()

# Boucle principale du jeu
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ajouter des obstacles à intervalles réguliers
    temps_actuel = pygame.time.get_ticks()
    if temps_actuel - dernier_temps_obstacle > intervalle_obstacle:
        obstacle = Obstacle(vitesse_obstacle)
        tous_les_sprites.add(obstacle)
        groupe_obstacles.add(obstacle)
        dernier_temps_obstacle = temps_actuel

        # Augmenter la difficulté toutes les 10 secondes
        if temps_actuel // 10000 > score // 10:
            vitesse_obstacle += 1

    # Mise à jour des sprites
    tous_les_sprites.update()

    # Vérification des collisions
    if pygame.sprite.spritecollideany(joueur, groupe_obstacles):
        son_collision.play()
        print("Collision détectée ! Fin du jeu.")
        pygame.quit()
        sys.exit()

    # Mise à jour du score
    score = temps_actuel // 1000

    # Dessin des éléments à l'écran
    fenetre.fill(BLANC)
    tous_les_sprites.draw(fenetre)
    afficher_score(score)
    pygame.display.flip()

    # Contrôle de la vitesse de rafraîchissement
    horloge.tick(fps)
