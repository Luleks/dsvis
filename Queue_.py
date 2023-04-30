import pygame


class Queue:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.capacity = 8
        self.dynamic = False
        self.line_color = (0, 0, 0)
        self.free_space = 50
        self.elements = []
        self.front = 0
        self.back = 0
        self.font = pygame.font.SysFont("comicsans", 20)

    def switch_to_dynamic(self):
        self.dynamic = True

    def switch_to_static(self):
        if len(self.elements) > self.capacity:
            self.elements = self.elements[0:self.capacity]
        self.dynamic = False

    def draw_back(self, win):
        back_y = (self.y + self.height + self.free_space // 2) - (self.back + 1) * self.free_space
        back_width = 60
        back_x = 330 + (100 - back_width) // 2
        pygame.draw.line(win, self.line_color, (back_x, back_y), (back_x + back_width, back_y), 3)
        pygame.draw.line(win, self.line_color, (back_x + back_width, back_y), (back_x + back_width - 10, back_y - 10),
                         3)
        pygame.draw.line(win, self.line_color, (back_x + back_width, back_y), (back_x + back_width - 10, back_y + 10),
                         3)
        back_text = self.font.render("back", True, self.line_color)
        win.blit(back_text, (back_x + (back_width - 10 - back_text.get_width()) // 2, back_y - back_text.get_height()))

    def draw_front(self, win):
        front_y = (self.y + self.height + self.free_space // 2) - self.front * self.free_space
        front_width = 60
        front_x = 330 + (100 - front_width) // 2
        pygame.draw.line(win, self.line_color, (front_x, front_y), (front_x + front_width, front_y), 3)
        pygame.draw.line(win, self.line_color, (front_x + front_width, front_y), (front_x + front_width - 10, front_y - 10),
                         3)
        pygame.draw.line(win, self.line_color, (front_x + front_width, front_y), (front_x + front_width - 10, front_y + 10),
                         3)
        back_text = self.font.render("front", True, self.line_color)
        win.blit(back_text, (front_x + (front_width - 10 - back_text.get_width()) // 2, front_y - back_text.get_height()))

    def draw(self, win):
        pygame.draw.line(win, self.line_color, (self.x, self.y), (self.x, self.y + self.height), 5)
        pygame.draw.line(win, self.line_color, (self.x + self.width, self.y), (self.x + self.width,
                                                                               self.y + self.height), 5)
        
        self.draw_back(win)
        self.draw_front(win)
        