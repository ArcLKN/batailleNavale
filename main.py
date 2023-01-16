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
resolution = [display_w,display_h]  # pour faciliter l'utilisation
print(f"width = {resolution[0]}, height = {resolution[1]}")  # affiche les valeurs (pour le debugging)
screen = pygame.display.set_mode((resolution[0], int(resolution[1] - (75 / 1080 * resolution[1]))))  # Redimension écran

game = Game(resolution, screen)  # pour appeler les différentes fonctions situées dans la classe Game

print(pygame.display.Info())  # affiche les informations de l'écran (pour le debugging)

is_running = True

while is_running:  # tant que la boucle est vraie le jeu continue

    mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.



    # Si on appuie sur le bouton fermer de la fenêtre, quitte le jeu.
    for event in pygame.event.get():  # Pour chaque évènement inclu dans la librairie pygame
        if event.type == pygame.QUIT:  # Si l'évènement actionné par l'utilisateur est égal à celui associé à fermer la fenêtre
            is_running = False

        game.ui.watching(event, mouse_x, mouse_y)  # appelle la fonction watching depuis ui passant par game


    pygame.display.flip()  # Actualise l'écran

    game.update(screen)  # appelle la fonction update de game qui permet d'afficher toutes les images

    # fixer le nombre de FPS
    clock.tick(FPS)

pygame.quit()  # quitte le module pygame