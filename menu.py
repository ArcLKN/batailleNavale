import pygame.sprite

class Arrow(pygame.sprite.Sprite):

    def __init__(self, image, tag):
        super(Arrow, self).__init__()
        self.image = image
        self.hover_image = pygame.transform.smoothscale(self.image, (round(self.image.get_size()[0]*1.1), round(self.image.get_size()[1]*1.1)))
        self.tag = tag
        self.orientation = str()
        self.rect = self.image.get_rect()
        self.hover_rect = self.rect

class Text(pygame.sprite.Sprite):
    def __init__(self, font, text, tag):
        super(Text, self).__init__()
        self.font = font
        self.value = "str"
        self.tag = tag
        self.text = text
        self.rect = [0, 0]


class Option:

    def __init__(self, game):
        # important
        self.game = game
        # texte
        self.optionFont = pygame.font.SysFont('ComicSans MS', 35)
        # images
        self.option_banner = pygame.image.load('assets/optionBackground.jpg')
        self.option_banner_rect = self.option_banner.get_rect()

        self.rightArrowImage = pygame.image.load("assets/Arrow.png")
        self.rightArrowImage = pygame.transform.smoothscale(self.rightArrowImage, (50, 50))
        self.leftArrowImage = pygame.transform.flip(self.rightArrowImage, True, False)

        self.returnImage = pygame.image.load("assets/return.png")
        self.returnImageHover = pygame.transform.smoothscale(self.returnImage,
                                                        self.game.ratio(self.returnImage.get_size(), 80))
        self.returnImage = pygame.transform.smoothscale(self.returnImage, self.game.ratio(self.returnImage.get_size(), 70))
        self.returnRect = self.returnImage.get_rect()
        self.returnRect.x = self.game.resolution[0] - 110
        self.returnRect.y = 40
        # sons
        self.arrowSound = pygame.mixer.Sound("SFX/Next.wav")
        self.arrowSound.set_volume(0.2)
        # groupes de sprite
        self.allArrow = pygame.sprite.Group()
        self.allText = pygame.sprite.Group()
        # autre
        self.options = {
            "sizeBoard": {
                "value": 10,
                "name": "Taille plateau"
            },
            "numberBoat": {
                "value": 3,
                "name": "Nombre de bateaux"
            }
        }
        # appel fonction
        self.groupArrow()

# ajoute les sprites des flèches dans le groupe des flèches (self.allArrow) en fonction du nombre d'options.
    def groupArrow(self):
        x = 0
        for option in self.options:
            optionTitle = Text(self.optionFont, self.options[option]["name"], tag=option)
            optionTitle.rect = (200 + 500 * round(x / 5), 140 + (x * 200))
            optionValue = Text(self.optionFont, self.options[option]["value"], tag=option)
            optionValue.rect = (300 + 500 * round(x / 5), 200 + (x * 200))
            optionValue.value = "int"
            leftArrow = Arrow(self.leftArrowImage, tag=option)
            leftArrow.orientation = "left"
            leftArrow.rect.x, leftArrow.rect.y = 200 + 500 * round(x / 5), 200 + (x * 200)
            rightArrow = Arrow(self.rightArrowImage, tag=option)
            rightArrow.orientation = "right"
            rightArrow.rect.x, rightArrow.rect.y = 400 + 500 * round(x / 5), 200 + (x * 200)
            self.allArrow.add(leftArrow)
            self.allArrow.add(rightArrow)
            self.allText.add(optionTitle)
            self.allText.add(optionValue)
            x += 1

    def watching(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for arrow in self.allArrow:
                if arrow.rect.collidepoint(event.pos):
                    pygame.mixer.Channel(2).play(self.arrowSound)
                    for txt in self.allText:
                        if txt.tag == arrow.tag and txt.value == "int":
                            if arrow.orientation == "left":
                                if arrow.tag == "sizeBoard":
                                    if self.options[txt.tag]["value"] <= 4:
                                        return
                                elif arrow.tag == "numberBoat":
                                    if self.options[txt.tag]["value"] <= 1:
                                        return
                                self.options[txt.tag]["value"] -= 1
                                self.options["numberBoat"]["value"] = min(self.options["numberBoat"]["value"],
                                                                          self.options["sizeBoard"]["value"])
                            else:
                                if arrow.tag == "sizeBoard":
                                    if self.options[txt.tag]["value"] >= 26:
                                        return
                                elif arrow.tag == "numberBoat":
                                    if self.options[txt.tag]["value"] >= self.options["sizeBoard"]["value"]:
                                        return
                                self.options[txt.tag]["value"] += 1
                            txt.text = self.options[txt.tag]["value"]
                            return
            if self.returnRect.collidepoint(event.pos):
                if self.game.is_option:
                    pygame.mixer.Channel(2).play(self.game.sound.pauseMenuClose)
                    self.game.is_option = False

# Met à jour les entités de la partie option.
    def update(self, mouse_x, mouse_y):
        self.game.screen.fill([0, 0, 0])  # remplit l'écran avec la couleur -> black_color [0, 0, 0]
        self.game.screen.blit(self.option_banner, self.option_banner_rect)

        if self.returnRect.collidepoint((mouse_x, mouse_y)):
            self.game.screen.blit(self.returnImageHover, self.returnRect)
        else:
            self.game.screen.blit(self.returnImage, self.returnRect)

        for e in self.allArrow:
            if e.rect.collidepoint((mouse_x, mouse_y)):
                self.game.screen.blit(e.hover_image, e.rect)
            else:
                self.game.screen.blit(e.image, e.rect)
        for e in self.allText:
            text_surface = e.font.render(str(e.text), False, [255, 255, 255])
            self.game.screen.blit(text_surface, e.rect)
