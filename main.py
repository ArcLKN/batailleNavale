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

# Récupérer la taille d'écran de l'utilisateur.
display_w = pygame.display.Info().current_w  # Valeur de la largeur
display_h = pygame.display.Info().current_h  # Valeur de la hauteur
resolution = [display_w,display_h]
print(f"width = {resolution[0]}, height = {resolution[1]}")
screen = pygame.display.set_mode((resolution[0], int(resolution[1] - (75 / 1080 * resolution[1]))))  # Redimension écran

game = Game(resolution, screen)

print(pygame.display.Info())

is_running = True

while is_running:

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.



    # Si on appuie sur le bouton fermer de la fenêtre, quitte le jeu.
    for event in pygame.event.get():  # Pour chaque évènement inclu dans la librairie pygame
        if event.type == pygame.QUIT:  # Si l'évènement actionné par l'utilisateur est égal à celui associé à fermer la fenêtre
            is_running = False

        game.ui.watching(event, mouse_x, mouse_y)


    pygame.display.flip()  # Actualise l'écran

    game.update(screen)

    # fixer le nombre de FPS
    clock.tick(FPS)

pygame.quit()  # quitte le module pygame