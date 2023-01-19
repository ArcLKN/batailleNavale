import pygame.sprite


class Boat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = str()
        self.size_x = 0
        self.size_y = 0
        self.taille = 1
        self.positioning = True
        self.is_touched = False
        self.is_dead = False


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tileSize, color):
        pygame.sprite.Sprite.__init__(self)
        self.tileSize = tileSize
        self.image = pygame.Surface([self.tileSize, self.tileSize])
        self.color = color
        self.rect = pygame.draw.rect(self.image,  # image
                                     self.color,  # color
                                     pygame.Rect(0, 0, self.tileSize, self.tileSize))
        self.size_x, self.size_y = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.coordonnee = [0, 0]
        self.is_boat_on = False


class Board(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Board, self).__init__()
        self.game = game
        print("----")
        print(self.game.resolution)  # debugging
        print("----")
        self.size = 10  # définit la taille du plateau
        self.name = "player" # définit si le plateau est celui du joueur ou de l'ordi
        self.maxBoat = 10  # définit le nombre maximum de bateau qu'il peut y avoir sur le plateau
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
                tile.coordonnee = [i,y]
                self.all_tiles.add(tile)
