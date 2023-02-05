import json
import os
import pygame.sprite
import random
from UI import UI
from board import Board, Boat, Cross
from computer import Computer
from menu import Option
from save import Save

black_color = [0, 0, 0]  # pas super utile mais existe

class Sound():

    def __init__(self):

        self.returnToMenu = pygame.mixer.Sound("SFX/WW_PictoBox_Erase.wav")
        self.pauseMenuOpen = pygame.mixer.Sound("SFX/WW_PauseMenu_Open.wav")
        self.pauseMenuClose = pygame.mixer.Sound("SFX/WW_PauseMenu_Close.wav")
        self.pauseMenuSave = pygame.mixer.Sound("SFX/WW_PauseMenu_Save.wav")

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

        self.musicQueueList = [[], [], [], []]

# === Fonction qui permet de s'occuper de quand un son doit être joué. ===

# En gros, ca va regarder si le salon vocal rentré en paramètre est occupé (channel).
# -> if not pygame.mixer.Channel(channelNumber).get_busy():
# * Si le salon numéro "channelNumber" est occupé ...

# Si l'un des salons vocaux n'est pas occupé alors la fonction regarde si y a des sons en attentes.
# -> if len(self.musicQueueList[channelNumber-1]) > 0:
# * Si la longueur de la file d'attente numéro "channelNumber" est supérieure à 0 ...

# Et si c'est le cas ca va les jouer.
# -> pygame.mixer.Channel(channelNumber).play(pygame.mixer.Sound(self.musicQueueList[channelNumber-1][0]))
# Joue le son numéro de la file d'attente numéro "channelNumber" dans le salon vocal numéro "channelNumber".
    def mixing(self, channelNumber):
        if not pygame.mixer.Channel(channelNumber).get_busy():
            if len(self.musicQueueList[channelNumber-1]) > 0:
                pygame.mixer.Channel(channelNumber).play(pygame.mixer.Sound(self.musicQueueList[channelNumber-1][0]))
                self.musicQueueList[channelNumber-1].pop(0)

class Game():

    def __init__(self, resolution, screen):
        super().__init__()

        self.screen = screen  # permet aux autres modules d'utiliser la variable à travers la classe Game
        self.resolution = resolution  # permet aux autres modules d'utiliser la variable à travers la classe Game

        self.computer = Computer(self)
        self.boat = Boat()
        self.board = Board(self)
        self.sound = Sound()
        self.option = Option(self)
        self.save = Save()

        self.ui = UI(self)
        self.stateBoard = "player"
        self.status = "positionning"
        self.timer = 120
        self.turn = 0

        self.is_running = True
        self.is_pausing = False
        self.is_playing = False
        self.is_option = False

        # curseur cible
        self.cible_image = pygame.image.load("assets/cible.png")
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_image = pygame.transform.smoothscale(self.cible_image,
                                                        (round(self.cible_size_x / 8), round(self.cible_size_y / 8)))
        self.cible_size_x, self.cible_size_y = self.cible_image.get_size()
        self.cible_rect = self.cible_image.get_rect()

        # PAUSE
        # Bouton pour retourner au menu
        self.homeButton = pygame.image.load("assets/quit.png")
        size_x, size_y = self.homeButton.get_size()
        width_the_button_has_to_be = 300
        size_y = size_y / (size_x / width_the_button_has_to_be)
        size_x = size_x / (size_x / width_the_button_has_to_be)
        self.homeButtonHover = pygame.transform.smoothscale(self.homeButton, (size_x*1.1, size_y*1.1))
        self.homeButton = pygame.transform.smoothscale(self.homeButton, (size_x, size_y))
        self.homeButtonRect = self.homeButton.get_rect()
        self.homeButtonRect.x = round(self.screen.get_width() / 2 - size_x / 2)
        self.homeButtonRect.y = round(self.screen.get_height() * 0.9 - size_y)
        self.homeButtonHoverRect = self.homeButtonHover.get_rect()
        self.homeButtonHoverRect.y = round(self.screen.get_height() * 0.9 - size_y * 1.1)
        self.homeButtonHoverRect.x = round(self.screen.get_width() / 2 - size_x * 1.1 / 2)
        # Bouton pour sauvegarder l'état de sa partie.
        self.saveButton = pygame.image.load("assets/save.png")
        self.saveButtonHover = pygame.transform.smoothscale(self.saveButton, (size_x * 1.1, size_y * 1.1))
        self.saveButton = pygame.transform.smoothscale(self.saveButton, (size_x, size_y))
        self.saveButtonRect = self.saveButton.get_rect()
        self.saveButtonRect.x = round(self.screen.get_width() / 2 - size_x / 2)
        self.saveButtonRect.y = round(self.screen.get_height() * 0.75 - size_y)
        self.saveButtonHoverRect = self.saveButtonHover.get_rect()
        self.saveButtonHoverRect.y = round(self.screen.get_height() * 0.75 - size_y * 1.1)
        self.saveButtonHoverRect.x = round(self.screen.get_width() / 2 - size_x * 1.1 / 2)

    def saving(self):
        data = self.save.create_files(os.getcwd())
        data["Computer"] = {
            "Crosses": [],
            "Boats": [],
            "size": self.computer_board.size,
            "life": self.computer_board.life
        }
        data["Player"] = {
            "Crosses": [],
            "Boats": [],
            "size": self.computer_board.size,
            "life": self.computer_board.life
        }

        for cross in self.computer_board.allCross:
            data["Computer"]["Crosses"].append(
                {
                    "x": cross.rect.x,
                    "y": cross.rect.y,
                    "tag": "player",
                    "status": cross.status
                }
            )
        for boat in self.computer_board.all_boats:
            data["Computer"]["Boats"].append(
                {
                    "name": boat.name,
                    "x": boat.rect.x,
                    "y": boat.rect.y,
                    "size_x": boat.size_x,
                    "size_y": boat.size_y,
                    "width": boat.width,
                    "height": boat.height,
                    "rotation": boat.rotation,
                    "positioning": boat.positioning,
                    "user": boat.user,
                    "is_touched": boat.is_touched,
                    "coordonnee": boat.coordonnee
                }
            )
        for cross in self.player_board.allCross:
            data["Player"]["Crosses"].append(
                {
                    "x": cross.rect.x,
                    "y": cross.rect.y,
                    "tag": "player",
                    "status": cross.status
                }
            )
        for boat in self.player_board.all_boats:
            data["Player"]["Boats"].append(
                {
                    "name": boat.name,
                    "x": boat.rect.x,
                    "y": boat.rect.y,
                    "size_x": boat.size_x,
                    "size_y": boat.size_y,
                    "width": boat.width,
                    "height": boat.height,
                    "rotation": boat.rotation,
                    "positioning": boat.positioning,
                    "user": boat.user,
                    "is_touched": boat.is_touched,
                    "coordonnee": boat.coordonnee
                }
            )
        self.save.save_data(data)

    def loading(self):
        data = self.save.load_data(os.getcwd())
        self.player_board = Board(self)  # crée le plateau du joueur
        self.computer_board = Board(self)  # crée le plateau de l'ordi
        self.player_board.size = data["Player"]["size"]
        self.player_board.life = data["Player"]["life"]
        self.computer_board.size = data["Computer"]["size"]
        self.computer_board.life = data["Computer"]["life"]
        self.player_board.initialization()
        self.computer_board.initialization()
        for e in data["Player"]["Boats"]:
            boat = Boat()
            boat.size_x = e['size_x']
            boat.size_y = e['size_y']
            boat.width = e['width']
            boat.height = e['height']
            boat.rotation = e['rotation']
            boat.positioning = e['positioning']
            boat.user = e['user']
            boat.is_touched = e['is_touched']
            boat.coordonnee = e['coordonnee']
            boat.name = e["name"]
            if boat.name == "Airport":
                color = [30, 30, 90]
                boat.width = 4
            elif boat.name == "Battleship":
                color = [30, 30, 70]
                boat.width = 3
            else:
                color = [30, 30, 50]
                boat.width = 2
            boat.image = pygame.Surface([boat.size_x, boat.size_y])
            boat.rect = pygame.draw.rect(boat.image,  # image
                                                     color,  # color
                                                     pygame.Rect(0, 0, boat.size_x, boat.size_y))
            boat.rect.x = e['x']
            boat.rect.y = e['y']
            self.player_board.all_boats.add(boat)
        for e in data["Player"]["Crosses"]:
            cross = Cross(e['status'], self.computer_board.gridFlopImage)
            cross.tag = e['tag']
            cross.status = e['status']
            if cross.status == 2:
                cross.image = self.player_board.gridHitImage
            elif cross.status == 1:
                cross.image = self.player_board.gridFlopImage
            cross.rect = cross.image.get_rect()
            cross.rect.x = e['x']
            cross.rect.y = e['y']
            self.player_board.allCross.add(cross)

        for e in data["Computer"]["Boats"]:
            boat = Boat()
            boat.size_x = e['size_x']
            boat.size_y = e['size_y']
            boat.width = e['width']
            boat.height = e['height']
            boat.rotation = e['rotation']
            boat.positioning = e['positioning']
            boat.user = e['user']
            boat.is_touched = e['is_touched']
            boat.coordonnee = e['coordonnee']
            boat.name = e["name"]
            if boat.name == "Airport":
                color = [30, 30, 90]
                boat.width = 4
            elif boat.name == "Battleship":
                color = [30, 30, 70]
                boat.width = 3
            else:
                color = [30, 30, 50]
                boat.width = 2
            boat.image = pygame.Surface([boat.size_x, boat.size_y])
            boat.rect = pygame.draw.rect(boat.image,  # image
                                                     color,  # color
                                                     pygame.Rect(0, 0, boat.size_x, boat.size_y))
            boat.rect.x = e['x']
            boat.rect.y = e['y']
            self.computer_board.all_boats.add(boat)

        for e in data["Computer"]["Crosses"]:
            cross = Cross(e['status'], self.computer_board.gridFlopImage)
            cross.tag = e['tag']
            if cross.status == 2:
                cross.image = self.computer_board.gridHitImage
            elif cross.status == 1:
                cross.image = self.computer_board.gridFlopImage
            cross.rect = cross.image.get_rect()
            cross.rect.x = e['x']
            cross.rect.y = e['y']
            self.computer_board.allCross.add(cross)

    def ratio(self, size_u_have, size_u_want):
        theRatio = size_u_want / max(size_u_have[0], size_u_have[1])
        return [round(theRatio * size_u_have[0]), round(theRatio * size_u_have[1])]

# Fonction qui permet d'initialiser le jeu (les cases, etc)
    def initialisation(self):
        self.player_board = Board(self)  # crée le plateau du joueur
        self.computer_board = Board(self)  # crée le plateau de l'ordi
        self.player_board.size = self.option.options["sizeBoard"]["value"]
        self.player_board.maxBoat = self.option.options["numberBoat"]["value"]
        self.computer_board.size = self.option.options["sizeBoard"]["value"]
        self.computer_board.maxBoat = self.option.options["numberBoat"]["value"]
        self.player_board.initialization()
        self.computer_board.initialization()
        self.computer = Computer(self)
        self.computer_board.name = "computer"

    def emptying(self):
        # vide chaque groupe de sprite
        self.player_board.all_boats.empty()
        self.player_board.allCross.empty()
        self.player_board.all_tiles.empty()
        self.computer_board.all_boats.empty()
        self.computer_board.allCross.empty()
        self.computer_board.all_tiles.empty()
        self.status = "positionning"

# fonction qui regarde en permanence les évènements qui se déroulent au sein du jeu et agis en conséquence
    def watching(self, event):
        # Si une touche est relachée
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:  # si la touche est j
                self.switch_Board()  # Appelle la fonction switch_Board -> Permet de changer l'affichage des plateaux.
            # Si la touche 'échap" est relâchée -> Permet de faire appel au menu pause.
            elif event.key == pygame.K_ESCAPE:
                # Si le menu pause est déjà activé le ferme.
                if self.is_pausing:
                    self.is_pausing = False
                    pygame.mixer.Channel(2).play(self.sound.pauseMenuClose)
                # Sinon l'ouvre.
                else:
                    self.is_pausing = True
                    pygame.mixer.Channel(2).play(self.sound.pauseMenuOpen)
            elif event.key == pygame.K_t:
                if self.status == "waiting":
                    self.status = "hit"
        # Si le bouton gauche de la souris est relâché
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Si le status du jeu est en mode "hit" (pour que le joueur puisse tirer sur une case)
            # et qu'il n'y a pas déjà un tir d'effectué (en vérifiant si un son de tir est en train d'être joué)
            # et que le jeu n'est pas en pause
            # alors appelle la fonction qui permet de tirer
            if self.status == "hit" and not pygame.mixer.Channel(2).get_busy() and not self.is_pausing:
                self.hitCase(event.pos, self.player_board, self.computer_board, "player")
            # si le jeu est en pause, vérifie si le joueur clique sur l'un des boutons du menu pause
            elif self.is_pausing:
                # Vérifie la colision entre le bouton et le pointeur de la souris.
                if self.homeButtonRect.collidepoint(event.pos):
                    # Arrête toutes les musiques qui sont en train d'être jouées
                    pygame.mixer.Channel(2).stop()
                    pygame.mixer.Channel(1).fadeout(10)
                    self.sound.musicQueueList = [[], [], [], []]
                    pygame.mixer.Channel(2).play(self.sound.returnToMenu)
                    self.is_pausing = False
                    self.is_playing = False
                    self.emptying()
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("SFX/Menu.mp3"))
                # Si le bouton "sauvegarder" est appuyé -> sauvegarde.
                if self.saveButtonRect.collidepoint(event.pos):
                    pygame.mixer.Channel(2).play(self.sound.pauseMenuSave)
                    self.saving()

        # Vérifie si le joueur a placé tous ses bateaux pour le mettre en mode "tir".
        if len(self.player_board.all_boats) == self.player_board.maxBoat and not self.ui.is_positioning and self.status == "positionning":
            # Positionne les bateaux de l'ordinateur en fonction des bateaux posés par l'utilisateur.
            self.computer.putBoat(self.computer_board)
            # Passe le jeu en mode "jeu" pour changer les actions et ce qui doit être affiché par le jeu.
            self.status = "playing"
            self.timer = 60
        # petit cooldown pour éviter certains bugs
        elif self.status == "playing":
            self.timer -= 1
            if self.timer == 0:
                self.status = random.choice(["waiting", "computerHit"])
        if self.status == "computerHit":
            tileSize = round(((self.resolution[1] - self.resolution[3])- 48) / self.computer_board.size)
            rangeX = (self.resolution[0] / 2 - self.computer_board.size * tileSize / 2)
            x = random.randint(rangeX, rangeX + tileSize * (self.computer_board.size - 1))
            y = random.randint(0, tileSize * (self.computer_board.size - 1))
            result = self.hitCase((x, y), self.computer_board, self.player_board, "computer")
            while not result:
                tileSize = round(((self.resolution[1] - self.resolution[3]) - 48) / self.computer_board.size)
                rangeX = (self.resolution[0] / 2 - self.computer_board.size * tileSize / 2)
                x = random.randint(rangeX, rangeX + tileSize * (self.computer_board.size - 1))
                y = random.randint(0, tileSize * (self.computer_board.size - 1))
                result = self.hitCase((x, y), self.computer_board, self.player_board, "computer")

# Fonction qui gère le tir du joueur et de l'ordinateur.
# Vérifie que le tir est effectue sur une case valide
    def hitCase(self, mousePos, selfBoard, hittingBoard, tag):
        for tile in hittingBoard.all_tiles:
            if tile.rect.collidepoint(mousePos):
                if tile.is_cross_on:
                    return False
                # Joue un son uniquement si le joueur tire.
                if tag == "player":
                    self.sound.musicQueueList[1].append(self.sound.lightBomb)
                    self.sound.musicQueueList[1].append(self.sound.fuseBomb)
                # Vérifie si un bateau est sur la case ou non.
                if tile.is_boat_on:
                    image = selfBoard.gridHitImage
                    status = 2
                    hittingBoard.life -= 1
                    print(hittingBoard.name,"got hit, life :", str(hittingBoard.life))
                    if tag == "player":
                        self.sound.musicQueueList[1].append(self.sound.bomb)
                else:
                    status = 1
                    image = selfBoard.gridFlopImage
                    if tag == "player":
                        self.sound.musicQueueList[1].append(self.sound.flop)

                # Crée un nouveau sprite croix.
                tile.is_cross_on = True
                cross = Cross(status, image)
                cross.rect = image.get_rect()
                cross.rect.x = tile.coordonnee[0] * selfBoard.tileSize + (self.resolution[0] / 2 - selfBoard.size * selfBoard.tileSize / 2)
                cross.rect.y = tile.coordonnee[1] * selfBoard.tileSize + (self.resolution[3] / 2)
                cross.tag = tag
                selfBoard.allCross.add(cross)
                # change le tour du joueur.
                if self.status == "hit":
                    self.status = "computerHit"
                else:
                    self.status = "waiting"
                # Vérifie que le tir n'amène pas à la victoire du joueur ou de l'ordinateur.
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

        #  affiche chaque entité de chaque groupe
        for e in self.ui.all_buttons:
            if e.name in ["Airport", "Battleship", "Ship"]:
                if self.status == "positionning":
                    screen.blit(e.image, e.rect)
            elif e.name == "Hit":
                if self.status in ["waiting", "hit"]:
                    screen.blit(e.image, e.rect)

        # Affichage du plateau du joueur
        if self.stateBoard == "player":
            for e in self.player_board.all_tiles:
                screen.blit(e.image, e.rect)
            for e in self.player_board.all_boats:
                screen.blit(e.image, e.rect)
            for e in self.player_board.allLetters:
                screen.blit(e.text_surface, e.rect)
            if self.status in ["waiting", "hit"]:
                for e in self.player_board.allCross:
                    if e.status > 0:
                        screen.blit(e.image, e.rect)

        # Affichage du plateau de l'ordinateur
        elif self.stateBoard == "computer":
            for e in self.computer_board.all_tiles:
                screen.blit(e.image, e.rect)
            for e in self.computer_board.all_boats:
                screen.blit(e.image, e.rect)
            for e in self.computer_board.allLetters:
                screen.blit(e.text_surface, e.rect)
            if self.status in ["waiting", "hit"]:
                for e in self.computer_board.allCross:
                    if e.status > 0:
                        screen.blit(e.image, e.rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()  # Obtenir la position (x, y) du curseur.

        # Affichage des boutons si le jeu est en pause
        if self.is_pausing:
            if self.homeButtonRect.collidepoint((mouse_x, mouse_y)):
                screen.blit(self.homeButtonHover, self.homeButtonHoverRect)
            else:
                screen.blit(self.homeButton, self.homeButtonRect)
            if self.saveButtonRect.collidepoint((mouse_x, mouse_y)):
                screen.blit(self.saveButtonHover, self.saveButtonHoverRect)
            else:
                screen.blit(self.saveButton, self.saveButtonRect)

        # Affichage du curseur si le joueur est en train de tirer.
        if self.status == "hit":
            self.cible_rect.x = mouse_x - self.cible_size_x / 2
            self.cible_rect.y = mouse_y - self.cible_size_y / 2
            screen.blit(self.cible_image, self.cible_rect)
