import pygame.sprite
import random


class Computer(pygame.sprite.Sprite):

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.name = "computer"

    def putBoat(self, board):
        print("Condition",str(self.game.ui.limitBoat(board)))
        while self.game.ui.limitBoat(board):
            self.game.ui.putBoat(random.choice(["BASIC", "BASIC", "Airport"]), board, "computer")
        print(board.all_boats)
        print("DONE PLACING COMPUTER'S BOATS")
