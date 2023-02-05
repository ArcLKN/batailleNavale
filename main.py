# coding: utf8
import pygame  # importation des différents modules
import os
#pygame.mixer.init(frequency=44000, size=16, channels=3, buffer=4096, devicename=None )
from game import Game  # Importation de game.py

pygame.init()  # initialiser le module pygame

pygame.mixer.init() #Initialiser le module py mixer
pygame.mixer.Channel(1).set_volume(1.0)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])

#mixer.music.load("SFX/Menu.mp3")
#mixer.music.set_volume(1)
#mixer.music.play(1)


# définir une clock
clock = pygame.time.Clock()
FPS = 60

# définir les différentes couleurs
black_color = [0, 0, 0]
white_color = [255, 255, 255]

# debugging
my_font = pygame.font.SysFont('Comic Sans MS', 30)
cursor = pygame.Surface([5, 5])  # provisoire
pygame.draw.rect(cursor, [0, 255, 0], pygame.Rect(0, 0, 5, 5))
cursor_rect = cursor.get_rect()


# Récupérer la taille d'écran de l'utilisateur.
display_w = pygame.display.Info().current_w  # Valeur de la largeur
display_h = pygame.display.Info().current_h  # Valeur de la hauteur
resolution = [display_w,display_h-72]  # pour faciliter l'utilisation
print(resolution)
#print(f"width = {resolution[0]}, height = {resolution[1]}")  # affiche les valeurs (pour le debugging)
screen = pygame.display.set_mode((resolution[0], resolution[1]))  # Redimension écran
offset_x = 100
offset_y = 200
resolution.append(offset_x)
resolution.append(offset_y)

#générer la fenêtre de notre jeu
pygame.display.set_caption("Bataille Navale")

#importer charger l'arrière plan du jeu
background = pygame.image.load('assets/fond zelda.jpg')
background = pygame.transform.smoothscale(background, (display_w, display_h))

#importer charger notre bannière
banner = pygame.image.load('assets/Logo.png')
banner = pygame.transform.scale(banner,(250,250))
banner_rect = banner.get_rect()
banner_rect.x = round(screen.get_width()/2.6)

#importer charger notre bouton pour lancer la partie
play_button = pygame.image.load('assets/start.png')
continue_button = pygame.image.load('assets/continue.png')

size_x, size_y = play_button.get_size()
width_the_button_has_to_be = 300
size_y = size_y/(size_x/width_the_button_has_to_be)
size_x = size_x/(size_x/width_the_button_has_to_be)
play_button = pygame.transform.scale(play_button, (size_x, size_y))
play_button_hover = pygame.transform.scale(play_button, (size_x*1.1, size_y*1.1))
play_button_rect = play_button.get_rect()
play_button_rect.x = round(screen.get_width()/2-size_x/2)
play_button_rect.y = round(screen.get_height()*0.9-size_y)
play_button_hover_rect = play_button_hover.get_rect()
play_button_hover_rect.x = round(screen.get_width()/2-size_x*1.1/2)
play_button_hover_rect.y = round(screen.get_height()*0.9-size_y*1.1)

continue_button = pygame.transform.scale(continue_button, (size_x, size_y))
continue_button_hover = pygame.transform.scale(continue_button, (size_x*1.1, size_y*1.1))
continue_button_rect = continue_button.get_rect()
continue_button_rect.x = round(screen.get_width()/2-size_x/2)
continue_button_rect.y = round(screen.get_height()*0.75-size_y)
continue_button_hover_rect = continue_button_hover.get_rect()
continue_button_hover_rect.x = round(screen.get_width()/2-size_x*1.1/2)
continue_button_hover_rect.y = round(screen.get_height()*0.75-size_y*1.1)

game = Game(resolution, screen)  # pour appeler les différentes fonctions situées dans la classe Game

#print(pygame.display.Info())  # affiche les informations de l'écran (pour le debugging)

is_running = True

pygame.mixer.Channel(1).play(pygame.mixer.Sound("SFX/Menu.mp3"))

while is_running:  # tant que la boucle est vraie le jeu continue

    game.sound.mixing(1)
    game.sound.mixing(2)
    game.sound.mixing(3)
    game.sound.mixing(4)

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.

    screen.fill(black_color)



    #apliquer l'arrière plan de notre jeu
    screen.blit(background, (0,0))

    #verifier si notre jeu a commencé ou non
    if game.is_playing :
        #declencher les instruction de la partie
        game.update(screen)
    elif game.is_option:
        game.option.update(mouse_x, mouse_y)
        # effet
        if play_button_rect.collidepoint((mouse_x, mouse_y)):
            screen.blit(play_button_hover, play_button_hover_rect)
        else:
            screen.blit(play_button, play_button_rect)
    #verifier si notre jeu n'a pas commencé
    else:
        #ajouter mon ecran de bienvenue
        screen.blit(banner, banner_rect)
        if play_button_rect.collidepoint((mouse_x, mouse_y)):
            screen.blit(play_button_hover, play_button_hover_rect)
        else:
            screen.blit(play_button, play_button_rect)
        if os.path.exists(rf"save.json"):
            # effet
            if continue_button_rect.collidepoint((mouse_x, mouse_y)):
                screen.blit(continue_button_hover, continue_button_hover_rect)
            else:
                screen.blit(continue_button, continue_button_rect)

    # Si on appuie sur le bouton fermer de la fenêtre, quitte le jeu.
    for event in pygame.event.get():  # Pour chaque évènement inclu dans la librairie pygame
        if event.type == pygame.QUIT:  # Si l'évènement actionné par l'utilisateur est égal à celui associé à fermer la fenêtre
            is_running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
        #verification pour savoir si la souris est sur le bouton start
            if play_button_rect.collidepoint(event.pos):
                if not game.is_playing and not game.is_option:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("SFX/WW_MainMenu_Select.wav"))
                    game.is_option = True
                elif game.is_option:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("SFX/WW_MainMenu_Select.wav"))
                    pygame.mixer.Channel(1).stop()
                    game.is_option = False
                    game.initialisation()
                    game.is_playing = True
                    game.sound.musicQueueList[0].append("SFX/Background.mp3")
            if continue_button_rect.collidepoint(event.pos):
                if not game.is_playing and not game.is_option:
                    pygame.mixer.Channel(2).play(pygame.mixer.Sound("SFX/WW_MainMenu_CopyErase_Start.wav"))
                    game.loading()
                    game.is_playing = True
                    game.status = "waiting"

        if game.is_playing:
            if not game.is_pausing:
                game.ui.watching(event, mouse_x, mouse_y, "button")  # appelle la fonction watching depuis ui passant par game
                game.ui.watching(event, mouse_x, mouse_y, "positioning")
            game.watching(event)
        elif game.is_option:
            game.option.watching(event)

    if not game.is_running:
        is_running = False

    # Affichage curseur et coordonnées
    posText = ("x: "+str(mouse_x)+", y: "+str(mouse_y))
    text_surface = my_font.render(posText, False, white_color)
    screen.blit(text_surface, (mouse_x+20, mouse_y))
    cursor_rect.x = mouse_x
    cursor_rect.y = mouse_y
    screen.blit(cursor, cursor_rect)

    pygame.display.flip()  # Actualise l'écran

    # fixer le nombre de FPS
    clock.tick(FPS)

pygame.quit()  # quitte le module pygame