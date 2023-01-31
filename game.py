import random
import pygame.sprite

from board import Board, Boat, Cross
from UI import UI
from computer import Computer
from menu import Option

black_color = [0, 0, 0]  # pas super utile mais existe

class Sound():

    def __init__(self):
        self.flop = pygame.mixer.Sound("SFX/Plouf.wav")
        self.flop.set_volume(0.2)
        self.bomb = pygame.mixer.Sound("SFX/Bombe3.wav")
        self.bomb.set_volume(0.2)
        self.putboat = pygame.mixer.Sound("SFX/Bateau posé.wav")
        self.putboat.set_volume(0.2)
        self.fuseBomb = pygame.mixer.Sound("SFX/WW_Bomb_Fuse.wav")
        self.fuseBomb.set_volume(0.2)
        self.lightBomb = pygame.mixer.Sound("SFX/WW_Bomb_Light.wav")
        self.lightBomb.set_volume(0.2)

class Game():

    def __init__(self, resolution, screen):
        super().__init__()

        self.screen = screen  # pas super utile mais existe
        self.resolution = resolution  # pas super utile mais existe

        self.boat = Boat()
        self.board = Board(self)
        self.sound = Sound()
        self.option = Option(self)

        self.ui = UI(self)
        self.stateBoard = "player"
        self.status = "positionning"
        self.timer = 120
        self.turn = 0

        self.is_running = True
        self.is_playing = False
        self.is_option = False

        # curseur cible
        self.cible_image = pygame.image.load("assets/cible.png")
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_image = pygame.transform.smoothscale(self.cible_image,
                                                        (round(self.cible_size_x / 8), round(self.cible_size_y / 8)))
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_rect = self.cible_image.get_rect()

    def initialisation(self):
        self.player_board = Board(self)  # crée le plateau du joueur
        self.computer_board = Board(self)  # crée le plateau de l'ordi
        self.player_board.size = self.option.options["sizeBoard"]["value"]
        self.computer_board.size = self.option.options["sizeBoard"]["value"]
        print(self.option.options["sizeBoard"]["value"])
        self.player_board.initialization()
        self.computer_board.initialization()

        self.computer = Computer(self)
        self.computer.putBoat(self.computer_board)
        self.computer_board.name = "computer"
        print("Nombre de bateaux Ordinateur :", str(len(self.computer_board.all_boats)))

        self.all_Tiles = self.player_board.all_tiles  # pas super utile mais existe

    def emptying(self):
        self.all_Tiles.empty()
        self.player_board.all_boats.empty()
        self.player_board.allCross.empty()
        self.player_board.all_tiles.empty()
        self.computer_board.all_boats.empty()
        self.computer_board.allCross.empty()
        self.computer_board.all_tiles.empty()
        self.status = "positionning"

    def watching(self, event):
        if event.type == pygame.KEYUP:  # Si touche relaché
            if event.key == pygame.K_j:  # si la touche est j
                self.switch_Board()  # appelle la fonction switch_Board
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.status == "hit":
                self.hitCase(event.pos, self.player_board, self.computer_board, "player")


        if len(self.player_board.all_boats) == self.player_board.maxBoat and not self.ui.is_positioning and self.status == "positionning":
            self.status = "playing"
            self.timer = 60
        elif self.status == "playing":
            self.timer -= 1
            if self.timer == 0:
                self.status = random.choice(["hit", "computerHit"])
        if self.status == "computerHit":
            tileSize = round((self.resolution[1] - 48) / self.computer_board.size)
            rangeX = (self.resolution[0] / 2 - self.computer_board.size * tileSize / 2)
            x = random.randint(rangeX, rangeX + tileSize * (self.computer_board.size - 1))
            y = random.randint(0, tileSize * (self.computer_board.size - 1))
            result = self.hitCase((x, y), self.computer_board, self.player_board, "computer")
            while not result:
                tileSize = round((self.resolution[1] - 48) / self.computer_board.size)
                rangeX = (self.resolution[0] / 2 - self.computer_board.size * tileSize / 2)
                x = random.randint(rangeX, rangeX + tileSize * (self.computer_board.size - 1))
                y = random.randint(0, tileSize * (self.computer_board.size - 1))
                result = self.hitCase((x, y), self.computer_board, self.player_board, "computer")

    def hitCase(self, mousePos, selfBoard, hittingBoard, tag):
        for tile in hittingBoard.all_tiles:
            if tile.rect.collidepoint(mousePos):

                pygame.mixer.Channel(2).play(self.sound.fuseBomb)
                pygame.mixer.Channel(2).play(self.sound.lightBomb)
                if tile.is_boat_on:
                    image = selfBoard.gridHitImage
                    status = 2
                    hittingBoard.life -= 1
                    print(hittingBoard.name,"got hit, life :", str(hittingBoard.life))
                    if tag == "player":
                        pygame.mixer.Channel(3).play(self.sound.bomb)
                else:
                    status = 1
                    image = selfBoard.gridFlopImage
                    if tag == "player":
                        pygame.mixer.Channel(3).play(self.sound.flop)


                if tile.is_cross_on:
                    return False
                tile.is_cross_on = True
                cross = Cross(status, image)
                cross.rect = image.get_rect()
                cross.rect.x = tile.coordonnee[0] * selfBoard.tileSize + (self.resolution[0] / 2 - selfBoard.size * selfBoard.tileSize / 2)
                cross.rect.y = tile.coordonnee[1] * selfBoard.tileSize
                cross.tag = tag
                selfBoard.allCross.add(cross)
                if self.status == "hit":
                    #print("Player Hit")
                    self.status = "computerHit"
                else:
                    #print("Computer Hit at :", str(mousePos))
                    self.status = "hit"
                if self.player_board.life == 0:
                    print("L'ordinateur a gagné !")
                    self.emptying()
                    self.is_playing = False
                elif self.computer_board.life == 0:
                    print("Le joueur a gagné !")
                    self.emptying()
                    self.is_playing = False
                return True
        return False

    # fonction pour changer l'affichage du plateau (soit celui du joueur, soit de l'ordi ou sinon spécifié)
    def switch_Board(self, case=None):
        if case is not None:
            self.stateBoard = case
        elif self.stateBoard == "player":
            self.stateBoard = "computer"
        else:
            self.stateBoard = "player"

    def update(self, screen):
        #screen.fill(black_color)  # remplit l'écran avec la couleur -> black_color [0, 0, 0]

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

            if self.stateBoard == "player":
                for e in self.player_board.allCross:
                    if e.status > 0:
                        screen.blit(e.image, e.rect)
            else:
                for e in self.computer_board.allCross:
                    if e.status > 0:
                        screen.blit(e.image, e.rect)
