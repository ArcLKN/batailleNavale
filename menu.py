import pygame
pygame.init()

#générer la fenêtre de notre jeu
pygame.display.set_caption("Fenêtre jeu")
pygame.display.set_mode((1080, 720))

running = True

# boucle tant que cette condition running est vrai
while running:

    # si le joueur ferme cette fenêtre
    for event in pygame.event.get():
        # verifier que l'evenement et fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            print ("Fermeture du jeu")
