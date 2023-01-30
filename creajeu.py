import pygame
import math
from game import Game
pygame.init()

#générer la fenêtre de notre jeu
pygame.display.set_caption("Bataille Navale")
screen = pygame.display.set_mode((1080, 720))

#importer charger l'arrière plan du jeu
background = pygame.image.load('assets/fond zelda.jpg')
background = pygame.transform.smoothscale(background, (1080, 720))

#importer charger notre bannière
banner = pygame.image.load('assets/Logo.png')
banner = pygame.transform.scale(banner,(250,250))
banner_rect = banner.get_rect()
banner_rect.x = math.ceil(screen.get_width()/2.6)

#importer charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/start.png')
size_x, size_y = play_button.get_size()
play_button = pygame.transform.scale(play_button, (size_x/(size_x/400), size_y/(size_x/400)))
play_button_rect = play_button.get_rect()
play_button_rect.x = math.ceil(screen.get_width()/3.33)
play_button_rect.y = math.ceil(screen.get_height()-size_y/(size_x/400)/1.5)

running = True

game = Game((1080, 720), screen)

# boucle tant que cette condition running est vrai
while running:


    #apliquer l'arrière plan de notre jeu
    screen.blit (background, (0,0))

    #verifier si notre jeu a commencé ou non
    if game.is_playing :
        #declencher les instruction de la partie
        game.update(screen)
    #verifier si notre jeu n'a pas commencé
    else :
        #ajouter mon ecran de bienvenue
        screen.blit(banner, banner_rect)
        screen.blit(play_button, play_button_rect)



    #mettre a jour l'ecran
    pygame.display.flip()

    # si le joueur ferme cette fenêtre
    for event in pygame.event.get():
        # verifier que l'evenement et fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print ("Fermeture du jeu")

        elif event.type == pygame.MOUSEBUTTONDOWN:
        #verification pour savoir si la souris est sur le bouton start
            if play_button_rect.collidepoint(event.pos):
                #mettre le jeu en mode lancé
                game.is_playing = True
