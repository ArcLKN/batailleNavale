import pygame.sprite

class Arrow(pygame.sprite.Sprite):

    def __init__(self, image, tag):
        super(Arrow, self).__init__()
        self.image = image
        self.tag = tag
        self.orientation = str()
        self.rect = self.image.get_rect()

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
        self.game = game
        self.optionFont = pygame.font.SysFont('Comic Sans MS', 30)
        self.rightArrowImage = pygame.image.load("assets/Arrow.png")
        self.rightArrowImage = pygame.transform.smoothscale(self.rightArrowImage, (50, 50))
        self.leftArrowImage = pygame.transform.flip(self.rightArrowImage, True, False)
        self.allArrow = pygame.sprite.Group()
        self.allText = pygame.sprite.Group()
        self.options = {
            "sizeBoard": {
                "value": 10,
                "name": "Size Board"
            }
        }
        self.groupArrow()

    def groupArrow(self):
        x = 0
        for option in self.options:
            print(option)
            optionTitle = Text(self.optionFont, self.options[option]["name"], tag=option)
            optionTitle.rect = (250 + 500 * round(x/5), 160 + (x * 200))
            optionValue = Text(self.optionFont, self.options[option]["value"], tag=option)
            optionValue.rect = (300 + 500 * round(x/5), 200 + (x * 200))
            optionValue.value = "int"
            leftArrow = Arrow(self.leftArrowImage, tag=option)
            leftArrow.orientation = "left"
            leftArrow.rect.x, leftArrow.rect.y = 200 + 500 * round(x/5), 200 + (x * 200)
            rightArrow = Arrow(self.rightArrowImage, tag=option)
            rightArrow.orientation = "right"
            rightArrow.rect.x, rightArrow.rect.y = 400 + 500 * round(x / 5), 200 + (x * 200)
            self.allArrow.add(leftArrow)
            self.allArrow.add(rightArrow)
            self.allText.add(optionTitle)
            self.allText.add(optionValue)
            x += 1

    def watching(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for arrow in self.allArrow:
                if arrow.rect.collidepoint(pygame.mouse.get_pos()):
                    for txt in self.allText:
                        if txt.tag == arrow.tag and txt.value == "int":
                            if arrow.orientation == "left":
                                self.options[txt.tag]["value"] -= 1
                            else:
                                self.options[txt.tag]["value"] += 1
                            txt.text = self.options[txt.tag]["value"]
                            return

    def update(self):
        self.game.screen.fill([0, 0, 0])  # remplit l'écran avec la couleur -> black_color [0, 0, 0]

        for e in self.allArrow:
            self.game.screen.blit(e.image, e.rect)
        for e in self.allText:
            text_surface = e.font.render(str(e.text), False, [255, 255, 255])
            self.game.screen.blit(text_surface, e.rect)
