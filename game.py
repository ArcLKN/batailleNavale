import pygame.sprite

from board import Board, Boat
from UI import UI


black_color = [0,0,0]  # pas super utile mais existe

class Game():

    def __init__(self,resolution, screen):
        super().__init__()

        self.screen = screen  # pas super utile mais existe
        self.resolution = resolution  # pas super utile mais existe

        self.board = Board(self)
        self.boat = Boat()

        self.ui = UI(self)

        self.all_Tiles = self.board.all_tiles  # pas super utile mais existe

        print("Len:",str(len(self.all_Tiles)))

    def update(self, screen):
        screen.fill(black_color)  # remplit l'écran avec la couleur -> black_color [0, 0, 0]

        #self.ui.watching()

        #  affiche chaque entité de chaque groupe
        for e in self.all_Tiles:
            screen.blit(e.image,e.rect)
        for e in self.ui.all_buttons:
            screen.blit(e.image,e.rect)
        for e in self.board.all_boats:
            screen.blit(e.image,e.rect)

        #screen.blit(self., self.ui.putBoatRect)