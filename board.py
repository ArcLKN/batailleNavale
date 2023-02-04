import pygame.sprite
import random



# crée la classe bateau
# avec un nom (id) -> pour savoir quels paramètres on donne au bateau
# une taille -> pour savoir combien de cases il occupe lors du placement.
# des coordonnées pour savoir ou il se trouve
# une appartenance, pour savoir si le bateau est au joueur ou bien à l'ordinateur
# s'il est en train d'être positionné, pour qu'il obéisse à des règles spéciales, etc.
# s'il est touché.
class Boat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.name = str()
        self.size_x = 0
        self.size_y = 0
        self.width = 1
        self.height = 1
        self.rotation = False
        self.positioning = True
        self.user = "player"
        self.is_touched = [0]
        self.coordonnee = [-1, -1]
        self.is_dead = False


# une class Case
# avec des coordonnées, pour les comparer à celle des bateaux et aussi pour distinguer les cases les unes des autres.
# un utilisateur, pour différencier les cases du joueur et de l'ordinateur (elles auront les mêmes coordonnées).
# une variable pour savoir si la case a un bateau dessus, pour ne pas poser d'autres bateaux dessus.
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, tileSize, color):
        pygame.sprite.Sprite.__init__(self)
        self.tileSize = tileSize
        #self.image = pygame.Surface([self.tileSize, self.tileSize])
        self.image = pygame.image.load("assets/tile1.jpg")
        self.image = pygame.transform.smoothscale(self.image, (self.tileSize, self.tileSize))
        self.color = color
        #self.rect = pygame.draw.rect(self.image,self.color,pygame.Rect(0, 0, self.tileSize, self.tileSize))
        self.rect = self.image.get_rect()
        self.size_x, self.size_y = self.image.get_size()
        self.rect.x = x
        self.rect.y = y
        self.user = "player"
        self.coordonnee = [0, 0]
        self.is_boat_on = False
        self.is_cross_on = False

class Cross(pygame.sprite.Sprite):
    def __init__(self, status, image):
        pygame.sprite.Sprite.__init__(self)
        self.status = status
        self.tag = "player"
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

class Letter(pygame.sprite.Sprite):
    def __init__(self, font, value):
        super(Letter, self).__init__()
        self.font = font
        self.color = [255, 255, 255]
        self.value = value
        self.axis = str()
        self.rect = [0, 0]
        self.text_surface = self.font.render(str(self.value), False, self.color)


# Une class Plateau
# avec un nom pour savoir si c'est le plateau du joueur ou bien de l'ordinateur
# une taille pour savoir combien de cases a le plateau
# un nombre maximum de bateaux, peut être différent pour le joueur et l'ordinateur.
# Un groupe pour toutes les cases que contient le plateau
# un groupe pour tous les bateaux que contient le plateau
class Board(pygame.sprite.Sprite):
    def __init__(self, game):
        super(Board, self).__init__()
        self.game = game
        #print("----")
        #print(self.game.resolution)  # debugging
        #print("----")
        self.size = 10  # définit la taille du plateau
        self.name = "player"  # définit si le plateau est celui du joueur ou de l'ordi
        self.allCross = pygame.sprite.Group()
        self.gridHitImage = pygame.image.load("assets/gridHitImage.png")
        self.gridFlopImage = pygame.image.load("assets/gridFlopImage.png")

        self.tileImages = ["assets/tile1.jpg", "assets/tile2.jpg", "assets/tile3.jpg", "assets/tile4.jpg"]

        self.maxBoat = 3  # définit le nombre maximum de bateau qu'il peut y avoir sur le plateau
        self.all_tiles = pygame.sprite.Group()
        self.all_boats = pygame.sprite.Group()
        self.allLetters = pygame.sprite.Group()
        self.life = 0

# crée les cases du plateau
    def initialization(self):
        self.tileSize = round((self.game.resolution[1] - self.game.resolution[3]) / self.size)
        self.gridHitImage = pygame.transform.smoothscale(self.gridHitImage, (self.tileSize, self.tileSize))
        self.gridFlopImage = pygame.transform.smoothscale(self.gridFlopImage, (self.tileSize, self.tileSize))

        font = pygame.font.SysFont('Comic Sans MS', round(self.tileSize / 2))
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

        for y in range(0, self.size):

            # créations des lettres sur les côtés
            letter = Letter(font, str(y+1))
            letter.axis = "y"
            letter.rect[0] = 0 * self.tileSize + (self.game.resolution[0] / 2 - self.size * self.tileSize / 2)
            letter.rect[0] -= (self.tileSize + len(str(y+1))*7)  # pour l'écarter un peu du terrain
            letter.rect[1] = y * self.tileSize + self.game.resolution[3] / 2
            self.allLetters.add(letter)
            # créations des lettres sur les côtés bis
            letter = Letter(font, alphabet[y])
            letter.axis = "x"
            letter.rect[0] = y * self.tileSize + (self.game.resolution[0] / 2 - self.size * self.tileSize / 2) + self.tileSize / 2
            letter.rect[1] = self.game.resolution[3] / 2 - self.tileSize
            self.allLetters.add(letter)

            for i in range(0, self.size):
                # calcule la couleur de la case (inutile tbh)
                color = [0, 0, 255]
                calcul = min(((self.size-1)/2 - abs(y - (self.size-1)/2)), ((self.size-1)/2 - abs(i - (self.size-1)/2)))
                color[2] = color[2] - (min(150, self.size*5)/self.size) * calcul * 2.5

                x = i * self.tileSize + (self.game.resolution[0] / 2 - self.size * self.tileSize / 2)
                tile = Tile(x, y * self.tileSize + self.game.resolution[3] / 2, self.tileSize, color)
                tile.coordonnee = [i, y]
                tile.image = pygame.image.load(random.choice(self.tileImages))
                tile.image = pygame.transform.smoothscale(tile.image, (self.tileSize, self.tileSize))
                self.all_tiles.add(tile)
