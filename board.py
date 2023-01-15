import pygame.sprite


class Boat(pygame.sprite.Sprite):
    def __init__(self):
        super(Boat, self).__init__()
        self.name = str()
        self.is_touched = False
        self.is_dead = False

    def initialize(self):
        if self.name == "Airport":
            print("Creating Aiport")
            self.size_x, self.size_y = 300, 40
            color = [50, 30, 30]
        else:
            print("Creating BASIC")
            self.size_x, self.size_y = 80, 30
            color = [30, 30, 50]
        self.image = pygame.Surface([self.size_x, self.size_y])
        self.rect = self.rect = pygame.draw.rect(self.image,  # image
                                                     color,  # color
                                                     pygame.Rect(0, 0, self.size_x, self.size_y))
        self.rect.x = 0
        self.rect.y = 0
        print("BOAT CREATED")


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tileSize, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([tileSize, tileSize])
        self.color = color
        self.rect = pygame.draw.rect(self.image,  # image
                                     self.color,  # color
                                     pygame.Rect(0, 0, tileSize, tileSize))
        self.size_x, self.size_y = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.is_boat_on = False


class Board(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Board, self).__init__()
        self.game = game
        print("----")
        print(self.game.resolution)
        print("----")
        self.size = 7
        self.all_tiles = pygame.sprite.Group()
        self.all_boats = pygame.sprite.Group()
        self.initialization()

    def initialization(self):
        tileSize = round((self.game.resolution[1] - 48) / self.size)

        for y in range(0, self.size):
            #print("------")
            for i in range(0, self.size):

                color = [0,0,255]
                calcul = min(((self.size-1)/2 - abs(y - (self.size-1)/2)), ((self.size-1)/2 - abs(i - (self.size-1)/2)))
                color[2] = color[2] - (min(150,self.size*5)/self.size) * calcul*2.5

                x = i * tileSize + (self.game.resolution[0] / 2 - self.size * tileSize / 2)
                #print(x, color)
                tile = Tile(x
                            , y * tileSize, tileSize, color)
                self.all_tiles.add(tile)
