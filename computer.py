import pygame.sprite
import random


class Computer(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = "computer"
        self.boatList = []

    def putBoat(self, board):
        print("Condition", str(self.game.ui.limitBoat(board)))
        while len(self.boatList) > 0:
            bateau = self.boatList[0]
            delta = False
            # Delta = faux si le bateau n'a pas pu être placé, vrai si le bateau a pu être placé
            while delta == False:
                delta = self.game.ui.putBoat(bateau, board, "computer")
            self.boatList.pop(0)
        print(board.all_boats)
