import pygame
pygame.font.init()


class Button:

    def __init__(self, x, y, width, height, color, text="", text_color=(0, 0, 0), active=False,
                 font=pygame.font.SysFont("comicsans", 25)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.light_color = self.color
        self.dark_color = Button.color_correction((self.color[0] - 20, self.color[1] - 20, self.color[2] - 20))
        self.text = text
        self.text_color = text_color
        self.font = font
        self.active = active

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, self.text_color)
        text_x = self.x + (self.width - text.get_width()) // 2
        text_y = self.y + (self.height - text.get_height()) // 2
        win.blit(text, (text_x, text_y))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def __lighten(self):
        self.color = self.light_color

    def __darken(self):
        self.color = self.dark_color

    def shift_color(self, pos):
        if self.active:
            self.__darken()
            return
        if self.is_over(pos):
            self.__darken()
        else:
            self.__lighten()

    @staticmethod
    def color_correction(color):
        r, g, b = color
        if r < 0:
            r = 0
        elif r > 255:
            r = 255
        if g < 0:
            g = 0
        elif g > 255:
            g = 255
        if b < 0:
            b = 0
        elif b > 255:
            b = 255
        return r, g, b
