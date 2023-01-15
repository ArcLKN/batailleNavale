import pygame.sprite

from board import Board, Boat
from UI import UI

black_color = [0,0,0]

class Game():

    def __init__(self,resolution, screen):
        super().__init__()

        self.screen = screen
        self.resolution = resolution

        self.board = Board(self)
        self.boat = Boat()

        self.ui = UI(self)

        self.all_Tiles = self.board.all_tiles

        print("Len:",str(len(self.all_Tiles)))

    def update(self, screen):
        screen.fill(black_color)

        #self.ui.watching()

        for e in self.all_Tiles:
            screen.blit(e.image,e.rect)
        for e in self.ui.all_buttons:
            screen.blit(e.image,e.rect)
        for e in self.board.all_boats:
            screen.blit(e.image,e.rect)

        #screen.blit(self., self.ui.putBoatRect)