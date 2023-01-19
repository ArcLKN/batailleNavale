import pygame.sprite
from random import randint

from board import Boat

# classe pour les boutons, le nom permet de donner au bouton des actions / caractéristiques différentes, c'est son id enfaite.
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 100])  # provisoire
        pygame.draw.rect(self.image,  # image
                         [200+(randint(0,70)-35), 70, 70],  # color
                         pygame.Rect(0, 0, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.clicked = 0


class UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super(UI, self).__init__()
        self.game = game  # pour avoir les fonctions dans game
        self.all_buttons = pygame.sprite.Group()  # crée un groupe pour les boutons
        self.addButton(0, 0, "Airport")
        self.addButton(100, 0, "Ship")
        self.addButton(200, 0, "Ship")
        self.is_positioning = False

    def putBoat(self, name):
        boat = Boat()
        if name == "Airport":
            print("Creating Aiport")
            boat.size_x, boat.size_y = 330, 40
            color = [50, 30, 30]
            boat.taille = 4
        else:
            print("Creating BASIC")
            boat.size_x, boat.size_y = 80, 30
            color = [30, 30, 50]
            boat.taille = 2
        boat.size_x, boat.size_y = (boat.size_x*7)/self.game.board.size, (boat.size_y*7)/self.game.board.size
        boat.image = pygame.Surface([boat.size_x, boat.size_y])
        boat.rect = boat.rect = pygame.draw.rect(boat.image,  # image
                                                     color,  # color
                                                     pygame.Rect(0, 0, boat.size_x, boat.size_y))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        boat.rect.x = mouse_x
        boat.rect.y = mouse_y
        self.game.board.all_boats.add(boat)
        self.is_positioning = True

    def limitBoat(self, plateau, name):
        if len(self.game.board.all_boats) < self.game.board.maxBoat:
            if not self.is_positioning:
                self.putBoat(name)
        else:
            print("MAX BATEAU")

    # vérifie chaque action en rapport avec des inputs de l'utilisateur
    def watching(self, event, mouse_x, mouse_y, check):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if check == "button":
                for e in self.all_buttons:
                    if e.rect.collidepoint((mouse_x, mouse_y)):
                        e.clicked = 1
                        print("DOWN")
                    else:
                        e.clicked = 0
            if check == "positioning" and self.is_positioning:  # si on est train de positionner un bateau
                for e in self.game.board.all_boats:  # pour chaque bateau
                    for t in self.game.all_Tiles: # pour chaque case du plateau
                        if t.rect.collidepoint(e.rect.x, e.rect.y): # si la souris est sur la case
                            is_placeable = True
                            if self.game.board.size - t.coordonnee[0] >= e.taille: # vérifie qu'il y assez de case pour mettre le bateau
                                for t2 in self.game.board.all_tiles:  # pour chaque case du plateau
                                    if t2.coordonnee[1] == t.coordonnee[1]:  # si la case est sur la meme ligne que celle choisie
                                        # si la case fait partie de celles où sera le bateau
                                        if t2.coordonnee[0] < t.coordonnee[0]+e.taille and t2.coordonnee[0] >= t.coordonnee[0]:
                                            # si la case a déjà un bateau
                                            if t2.is_boat_on:
                                                is_placeable = False # empêche qu'un bateau soit posé
                                                break  # arrête de regarder pour les autres cases, parce que si une case est mauvaise c'est mauvais
                            else:
                                is_placeable = False
                            if is_placeable:
                                print(t.coordonnee)
                                for t2 in self.game.board.all_tiles:
                                    if t2.coordonnee[1] == t.coordonnee[1]:
                                        if t2.coordonnee[0] < t.coordonnee[0]+e.taille:
                                            t2.is_boat_on = True
                                e.rect.x = t.rect.x+t.size_x/2
                                e.rect.y = t.rect.y+t.size_y/2-e.size_y/2
                                e.positioning = False
                                self.is_positioning = False
        if check == "positioning" and self.is_positioning:
            for e in self.game.board.all_boats:
                if e.positioning:
                    e.rect[0] = mouse_x
                    e.rect[1] = mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if check == "button":
                for e in self.all_buttons:
                    if e.rect.collidepoint(event.pos) and e.clicked == 1:
                        e.clicked = 0
                        print("UP")
                        self.limitBoat("", e.name)
                    else:
                        e.clicked = 0

    def addButton(self, x, y, name):
        button = Button(x, y, name)
        self.all_buttons.add(button)

    def initialize(self, number):
        pass
