import pygame.sprite
from random import randint
from board import Boat


# classe pour les boutons, le nom permet de donner au bouton des actions / caractéristiques différentes, c'est son id enfaite.
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 100])  # provisoire
        pygame.draw.rect(self.image,  # image
                         [200 + (randint(0, 70) - 35), 70, 70],  # color
                         pygame.Rect(0, 0, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name  # id du bouton
        self.clicked = False  # s'il a été cliqué


class UI(pygame.sprite.Sprite):
    def __init__(self, game):
        super(UI, self).__init__()
        self.game = game  # pour avoir les fonctions dans game
        self.all_buttons = pygame.sprite.Group()  # crée un groupe pour les boutons
        self.addButton(0, 0, "Airport")
        self.addButton(100, 0, "Ship")
        self.addButton(200, 0, "Ship")
        self.is_positioning = False

    def putBoat(self, name, board, user="player"):
        boat = Boat()
        if name == "Airport":
            print("Creating Aiport")
            boat.size_x, boat.size_y = 330, 40
            color = [50, 30, 30]
            boat.width = 4
        else:
            print("Creating BASIC")
            boat.size_x, boat.size_y = 80, 30
            color = [30, 30, 50]
            boat.width = 2
        boat.size_x, boat.size_y = (boat.size_x * 7) / board.size, (boat.size_y * 7) / board.size
        boat.image = pygame.Surface([boat.size_x, boat.size_y])
        boat.rect = boat.rect = pygame.draw.rect(boat.image,  # image
                                                 color,  # color
                                                 pygame.Rect(0, 0, boat.size_x, boat.size_y))
        if user == "player":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            boat.rect.x = mouse_x
            boat.rect.y = mouse_y
            self.is_positioning = True
            board.all_boats.add(boat)
        else:
            range = round(self.game.resolution[0] / 2 - self.game.computer_board.size * self.game.computer_board.tileSize / 2)
            boat.rect.x = randint(range, range + self.game.computer_board.tileSize * (self.game.computer_board.size-1))
            boat.rect.y = randint(0, self.game.computer_board.tileSize * (self.game.computer_board.size)-1)
            print(boat.rect.x, boat.rect.y)
            board.all_boats.add(boat)
            self.checkPlacementBoat(boat, board)



    def returnBoard(self, id: str):
        if id == "player":
            board = self.game.player_board
        else:
            board = self.game.computer_board
        return board

    def limitBoat(self, plateau):  # vérifie que la limite de bateau n'est pas atteinte
        board = self.returnBoard(plateau)
        if len(board.all_boats) < board.maxBoat:
            return True
        else:
            return False

    # Fonction pour vérifier que le placement du bateau se fait correctement
    # Pas mettre deux bateaux au même endroit, pas en dehors du terrain, etc.
    def checkPlacementBoat(self, e, board):
        for t in board.all_tiles:  # pour chaque case du plateau
            if t.rect.collidepoint(e.rect.x, e.rect.y):  # si la souris est sur la case
                is_placeable = True  # par défaut c'est bon
                # vérifie qu'il y assez de case pour mettre le bateau
                if board.size - t.coordonnee[0] >= e.width and board.size - t.coordonnee[1] >= e.height:
                    for t2 in board.all_tiles:  # pour chaque case du plateau
                        # si la case est sur la meme ligne que celle choisie
                        #pour les abscisses
                        if t2.coordonnee[1] == t.coordonnee[1]:
                            # si la case fait partie de celles où sera le bateau
                            if t.coordonnee[0] + e.width > t2.coordonnee[0] >= t.coordonnee[0]:
                                # si la case a déjà un bateau
                                if t2.is_boat_on:
                                    e.kill()
                                    self.is_positioning = False
                                    # arrête de regarder pour les autres cases
                                    # parce que si une case est mauvaise tout le reste est mauvais.
                                    return
                        # pour les ordonnées
                        if t2.coordonnee[0] == t.coordonnee[0]:
                            # si la case fait partie de celles où sera le bateau
                            if t.coordonnee[1] + e.height > t2.coordonnee[1] >= t.coordonnee[1]:
                                # si la case a déjà un bateau
                                if t2.is_boat_on:
                                    e.kill()
                                    self.is_positioning = False
                                    # arrête de regarder pour les autres cases
                                    # parce que si une case est mauvaise tout le reste est mauvais.
                                    return
                else:  # s'il n'y a pas assez de case, empêche qu'un bateau soit posé
                    self.is_positioning = False
                    e.kill()
                    return  # arrête de regarder les autres cases
                if is_placeable:  # si le bateau n'est pas pas placable (donc est placable)
                    for t2 in board.all_tiles:  # pour chaque case où est le bateau
                        if t2.coordonnee[1] == t.coordonnee[1]:
                            if t.coordonnee[0] + e.width > t2.coordonnee[0] >= t.coordonnee[0]:
                                # change la valeur de la case pour dire qu'il y a un bateau dessus
                                t2.is_boat_on = True
                    e.rect.x = t.rect.x + t.size_x / 2
                    e.rect.y = t.rect.y + t.size_y / 2 - e.size_y / 2
                    e.positioning = False  # fin du positionnement
                    self.is_positioning = False
                    board.life += e.width
                    print("Name :", board.name, "/ added", str(e.width), "lives ! Now", board.life, "lives.")
                    if board.name == "player":
                        pygame.mixer.Channel(3).play(self.game.sound.putboat)
                    break

    # vérifie chaque action en rapport avec des inputs de l'utilisateur
    def watching(self, event, mouse_x, mouse_y, check):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # si l'évènement est "Bouton Gauche de la souris pressé"
            if check == "button":
                for e in self.all_buttons:
                    if e.rect.collidepoint((mouse_x, mouse_y)):
                        e.clicked = True  # met le bouton en mode cliqué
                    else:
                        e.clicked = False  # pas très utile, mais évite des problèmes
            if check == "positioning" and self.is_positioning:  # si on est train de positionner un bateau
                for e in self.game.player_board.all_boats:  # pour chaque bateau
                    if e.positioning:
                        self.checkPlacementBoat(e, self.returnBoard(
                            "player"))  # vérifie que le placement du bateau est correct

        if check == "positioning" and self.is_positioning:
            for e in self.game.player_board.all_boats:
                if e.positioning:
                    e.rect[0] = mouse_x
                    e.rect[1] = mouse_y
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_r:
                            e.image = pygame.transform.rotate(e.image, 90)
                            foo = e.width
                            e.width = e.height
                            e.height = foo
                            if not e.rotation:
                                e.rotation = True
                            else:
                                e.rotation = False
                            e.rect = e.image.get_rect()
                            e.rect[0] = mouse_x
                            e.rect[1] = mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            if check == "button":
                # pour chaque bouton
                for e in self.all_buttons:
                    # vérifie s'il y a collision entre la souris et le bouton, et si le bouton a été cliqué
                    if e.rect.collidepoint(event.pos) and e.clicked:
                        e.clicked = False  # remet le bouton cliqué en non cliqué
                        if self.limitBoat("player"):  # vérifie si la limite de bateau n'est pas atteinte
                            if not self.is_positioning:
                                self.putBoat(e.name, self.game.player_board)
                    else:
                        e.clicked = False

    def addButton(self, x, y, name):
        button = Button(x, y, name)
        self.all_buttons.add(button)

    def initialize(self, number):
        pass
