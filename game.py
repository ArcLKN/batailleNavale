import pygame.sprite

from board import Board, Boat
from UI import UI
from computer import Computer

black_color = [0, 0, 0]  # pas super utile mais existe


class Game():

    def __init__(self, resolution, screen):
        super().__init__()

        self.screen = screen  # pas super utile mais existe
        self.resolution = resolution  # pas super utile mais existe
        self.player_board = Board(self)  # crée le plateau du joueur
        self.player_board.initialization()
        self.computer_board = Board(self)  # crée le plateau de l'ordi
        self.computer_board.initialization()

        self.boat = Boat()

        self.ui = UI(self)
        self.stateBoard = "player"

        self.computer = Computer(self)
        self.computer.putBoat(self.computer_board)
        print("Nombre de bateaux Ordinateur :", str(len(self.computer_board.all_boats)))

        self.all_Tiles = self.player_board.all_tiles  # pas super utile mais existe

        # print("Len:",str(len(self.all_Tiles)))

    def watching(self, event):
        if event.type == pygame.KEYUP:  # Si touche relaché
            if event.key == pygame.K_j:  # si la touche est j
                self.switch_Board()  # appelle la fonction switch_Board

    # fonction pour changer l'affichage du plateau (soit celui du joueur soit de l'ordi ou sinon spécifié)
    def switch_Board(self, case=None):
        if case is not None:
            self.stateBoard = case
        elif self.stateBoard == "player":
            self.stateBoard = "computer"
        else:
            self.stateBoard = "player"

    def update(self, screen):
        screen.fill(black_color)  # remplit l'écran avec la couleur -> black_color [0, 0, 0]

        #  affiche chaque entité de chaque groupe
        for e in self.ui.all_buttons:
            screen.blit(e.image, e.rect)
        if self.stateBoard == "player":
            for e in self.all_Tiles:
                screen.blit(e.image, e.rect)
            for e in self.player_board.all_boats:
                screen.blit(e.image, e.rect)
        elif self.stateBoard == "computer":
            for e in self.computer_board.all_tiles:
                screen.blit(e.image, e.rect)
            for e in self.computer_board.all_boats:
                screen.blit(e.image, e.rect)

        # screen.blit(self., self.ui.putBoatRect)
