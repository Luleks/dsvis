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
        self.back = len(self.elements) - 1
        if self.front != 0:
            self.front = 1

    def switch_to_static(self):
        if len(self.elements) >= self.capacity:
            self.elements = self.elements[0:self.capacity-1]
            self.back = self.capacity - 1
        else:
            self.back += 1
        self.dynamic = False
        if self.front != 0:
            self.front = 1

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
        if not self.dynamic:
            for i, element in enumerate(self.elements):
                if i + self.front - 1 < self.capacity:
                    i = i + self.front - 1
                else:
                    i = i + self.front - 1 - self.capacity
                pygame.draw.rect(win, (128, 128, 128), (self.x, self.y + self.height - (i + 1) * self.free_space,
                                                        self.width, self.free_space))
                pygame.draw.line(win, self.line_color, (self.x, self.y + self.height - (i + 1) * self.free_space),
                                 (self.x + self.width, self.y + self.height - (i + 1) * self.free_space), 5)
                value_text = self.font.render(element, True, self.line_color)
                win.blit(value_text, (self.x + (self.width - value_text.get_width()) // 2,
                                      self.y + self.height - (i + 1) * self.free_space + (self.free_space -
                                                                                          value_text.get_height()) // 2))
            self.draw_back(win)
            self.draw_front(win)

        else:
            limit = len(self.elements) if len(self.elements) <= self.capacity else self.capacity
            for i in range(limit):
                pygame.draw.rect(win, (128, 128, 128), (self.x, self.y + self.height - (i + 1) * self.free_space,
                                                        self.width, self.free_space))
                pygame.draw.line(win, self.line_color, (self.x, self.y + self.height - (i + 1) * self.free_space),
                                 (self.x + self.width, self.y + self.height - (i + 1) * self.free_space), 5)
                value_text = self.font.render(self.elements[i], True, self.line_color)
                win.blit(value_text, (self.x + (self.width - value_text.get_width()) // 2,
                                      self.y + self.height - (i + 1) * self.free_space + (self.free_space -
                                                                                          value_text.get_height()) // 2))
            self.draw_front(win)
            if self.back < self.capacity:
                self.draw_back(win)

        pygame.draw.line(win, self.line_color, (self.x, self.y), (self.x, self.y + self.height), 5)
        pygame.draw.line(win, self.line_color, (self.x + self.width, self.y), (self.x + self.width,
                                                                               self.y + self.height), 5)

    def enqueue(self, info, draw, win, settings_buttons, button_and_pair, stack_structure, time=1000):
        if not self.dynamic and (self.back + 2) % self.capacity == self.front:
            draw(win, settings_buttons, button_and_pair, stack_structure,
                 "Reached limit for static implementation of queue")
            pygame.time.delay(1000)
            return
        if not self.front:
            self.front = 1
        draw(win, settings_buttons, button_and_pair, stack_structure, f"Enqueueing {info} to queue")
        pygame.time.delay(time)
        self.elements.append(info)
        draw(win, settings_buttons, button_and_pair, stack_structure, f"Enqueueing {info} to queue")
        pygame.time.delay(time)
        if self.dynamic:
            self.back += 1
        else:
            self.back = (self.back + 1) % self.capacity

    def dequeue(self, draw, win, settings_buttons, button_and_pair, stack_structure, time=1000):
        if len(self.elements) == 0:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Error dequeueing from empty queue")
            pygame.time.delay(1000)
            return
        draw(win, settings_buttons, button_and_pair, stack_structure, "Dequeueing from queue")
        pygame.time.delay(time)

        if not self.dynamic:
            self.front = (self.front + 1) % (self.capacity + 1)
            if self.front == 0 and len(self.elements) != 0:
                self.front = 1
        else:
            self.back -= 1
        to_return = self.elements.pop(0)
        if len(self.elements) == 0 and self.dynamic:
            self.front = 0
        elif len(self.elements) == 0 and not self.dynamic:
            self.front = self.back = 0
        draw(win, settings_buttons, button_and_pair, stack_structure, "Dequeueing from queue")
        pygame.time.delay(time)

        return to_return

    def front_(self, draw, win, settings_buttons, button_and_pair, stack_structure, time=1000):
        if len(self.elements) == 0:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Error empty queue")
            pygame.time.delay(1000)
            return
        return self.elements[0]
