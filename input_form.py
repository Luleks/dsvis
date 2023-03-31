import pygame
from button import Button
pygame.font.init()


class InputForm:

    def __init__(self, x, y, width, height, color, text_color=(0, 0, 0), max_len=191, hide=False,
                 text_to_display="", font=pygame.font.SysFont("comicsans", 25), error_rect=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.light_color = self.color
        self.dark_color = Button.color_correction((self.color[0] - 20, self.color[1] - 20, self.color[2] - 20))
        self.text_color = text_color
        self.font = font
        self.text = ""
        self.state = False
        self.max_len = max_len
        self.hide = hide
        self.text_to_display = text_to_display
        self.error_rect = error_rect

    def draw(self, win: pygame.surface):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))

        if self.error_rect:
            pygame.draw.rect(win, pygame.Color("red"), (self.x, self.y, self.width, self.height), 2)

        if self.text == "":
            text = self.font.render(self.text_to_display, True, self.text_color)
        elif self.hide:
            text_to_display = self.text
            while self.font.render(text_to_display, True, self.text_color).get_width() > self.width:
                text_to_display = text_to_display[:-1]
            text = self.font.render("*"*len(text_to_display), True, self.text_color)
        else:
            text_to_display = self.text
            while self.font.render(text_to_display, True, self.text_color).get_width() > self.width:
                text_to_display = text_to_display[:-1]
            text = self.font.render(text_to_display, True, self.text_color)

        text_x = self.x + (self.width - text.get_width()) // 2
        text_y = self.y + (self.height - text.get_height()) // 2
        win.blit(text, (text_x, text_y))

    def is_over(self, pos: tuple):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height

    def __lighten(self):
        self.color = self.light_color

    def __darken(self):
        self.color = self.dark_color

    def shift_color(self, pos: tuple):
        if self.is_over(pos) or self.state:
            self.__darken()
        else:
            self.__lighten()

    def state_change(self, pos: tuple):
        if self.is_over(pos) and not self.state:
            self.state = True
        else:
            self.state = False

    def add_text(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = False
            elif self.state and event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif self.state and event.key == pygame.K_SPACE:
                self.text += " "
            elif self.state and event.unicode != " " and len(self.text) < self.max_len:
                self.text += event.unicode

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
