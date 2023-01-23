import pygame.sprite

from board import Board, Boat, Cross
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
        self.board = Board(self)

        self.ui = UI(self)
        self.stateBoard = "player"
        self.status = "positionning"
        self.timer = 120

        self.computer = Computer(self)
        self.computer.putBoat(self.computer_board)
        print("Nombre de bateaux Ordinateur :", str(len(self.computer_board.all_boats)))

        self.all_Tiles = self.player_board.all_tiles  # pas super utile mais existe

        # curseur cible
        self.cible_image = pygame.image.load("cible.png")
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_image = pygame.transform.smoothscale(self.cible_image,
                                                        (round(self.cible_size_x / 8), round(self.cible_size_y / 8)))
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_rect = self.cible_image.get_rect()

    def watching(self, event):
        if event.type == pygame.KEYUP:  # Si touche relaché
            if event.key == pygame.K_j:  # si la touche est j
                self.switch_Board()  # appelle la fonction switch_Board
        if event.type == pygame.MOUSEBUTTONUP:
            if self.status == "hit":
                self.hitCase(event.pos)

        if len(self.player_board.all_boats) == self.player_board.maxBoat and not self.ui.is_positioning and self.status == "positionning":
            self.status = "playing"
            self.timer = 120
        if self.status == "playing":
            self.timer -= 1
            print(self.timer)
            if self.timer == 0:
                self.status = "hit"

    def hitCase(self, mousePos):
        for tile in self.computer_board.all_tiles:
            if tile.rect.collidepoint(mousePos):
                if tile.is_boat_on:
                    image = self.board.gridHitImage
                    status = 2
                else:
                    status = 1
                    image = self.board.gridFlopImage
                cross = Cross(status, image)
                cross.rect = image.get_rect()
                cross.rect.x = tile.coordonnee[0] * self.board.tileSize + (self.resolution[0] / 2 - self.board.size * self.board.tileSize / 2)
                cross.rect.y = tile.coordonnee[1] * self.board.tileSize
                self.board.allCross.add(cross)

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

        if self.status == "hit":

            mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.

            self.cible_rect.x = mouse_x - self.cible_size_x / 2
            self.cible_rect.y = mouse_y - self.cible_size_y / 2

            screen.blit(self.cible_image, self.cible_rect)

            for e in self.board.allCross:
                if e.status > 0:
                    screen.blit(e.image, e.rect)
