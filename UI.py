import pygame.sprite
from random import randint

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([100, 100])
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
        self.game = game
        self.all_buttons = pygame.sprite.Group()
        self.addButton("Airport", 0)
        self.addButton("Ship", 100)
        self.addButton("Ship", 200)

    def putBoat(self, name):
        boat = self.game.boat
        boat.name = name
        #print("Name :",boat.name)
        self.game.board.all_boats.add(boat)
        boat.initialize()


    def watching(self, event, mouse_x, mouse_y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for e in self.all_buttons:
                if e.rect.collidepoint((mouse_x, mouse_y)):
                    e.clicked = 1
                    print("DOWN")
                else:
                    e.clicked = 0
        elif event.type == pygame.MOUSEBUTTONUP:
            for e in self.all_buttons:
                if e.rect.collidepoint(event.pos) and e.clicked == 1:
                    e.clicked = 0
                    print("UP")
                    self.putBoat(e.name)
                else:
                    e.clicked = 0

    def addButton(self, name, x):
        button = Button(x, 0, name)
        self.all_buttons.add(button)

    def initialize(self, number):
        pass
