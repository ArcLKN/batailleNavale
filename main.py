# coding: utf8
import pygame  # importation des différents modules
import sys
import os

from game import Game  # Importation de game.py

pygame.init()  # initialiser le module pygame

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
print(f"width = {resolution[0]}, height = {resolution[1]}")  # affiche les valeurs (pour le debugging)
screen = pygame.display.set_mode((resolution[0], resolution[1]))  # Redimension écran

game = Game(resolution, screen)  # pour appeler les différentes fonctions situées dans la classe Game

print(pygame.display.Info())  # affiche les informations de l'écran (pour le debugging)

is_running = True

while is_running:  # tant que la boucle est vraie le jeu continue

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.

    posText = ("x: "+str(mouse_x)+", y: "+str(mouse_y))
    text_surface = my_font.render(posText, False, white_color)

    screen.blit(text_surface, (mouse_x+20, mouse_y))
    cursor_rect.x = mouse_x
    cursor_rect.y = mouse_y
    screen.blit(cursor, cursor_rect)

    # Si on appuie sur le bouton fermer de la fenêtre, quitte le jeu.
    for event in pygame.event.get():  # Pour chaque évènement inclu dans la librairie pygame
        if event.type == pygame.QUIT:  # Si l'évènement actionné par l'utilisateur est égal à celui associé à fermer la fenêtre
            is_running = False

        game.ui.watching(event, mouse_x, mouse_y, "button")  # appelle la fonction watching depuis ui passant par game
        game.ui.watching(event, mouse_x, mouse_y, "positioning")
        game.watching(event)

    if not game.is_running:
        is_running = False

    pygame.display.flip()  # Actualise l'écran

    game.update(screen)  # appelle la fonction update de game qui permet d'afficher toutes les images

    # fixer le nombre de FPS
    clock.tick(FPS)

pygame.quit()  # quitte le module pygame