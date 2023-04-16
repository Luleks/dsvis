import pygame


class Stack:

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
        self.top = -1
        self.font = pygame.font.SysFont("comicsans", 20)

    def draw(self, win):
        if not self.dynamic or len(self.elements) <= self.capacity:
            for i, element in enumerate(self.elements):
                pygame.draw.rect(win, (128, 128, 128), (self.x, self.y + self.height - (i + 1) * self.free_space,
                                                        self.width, self.free_space))
                pygame.draw.line(win, self.line_color, (self.x, self.y + self.height - (i + 1) * self.free_space),
                                 (self.x + self.width, self.y + self.height - (i + 1) * self.free_space), 5)
                value_text = self.font.render(element, True, self.line_color)
                win.blit(value_text, (self.x + (self.width - value_text.get_width()) // 2,
                                      self.y + self.height - (i + 1) * self.free_space + (self.free_space -
                                                                                          value_text.get_height()) // 2))

        else:
            for i in range(len(self.elements) - self.capacity, len(self.elements)):
                pygame.draw.rect(win, (128, 128, 128), (self.x, self.y + self.height -
                                                        (i + 1 - len(self.elements) + self.capacity) * self.free_space,
                                                        self.width, self.free_space))
                pygame.draw.line(win, self.line_color, (self.x, self.y + self.height -
                                                        (i + 1 - len(self.elements) + self.capacity) * self.free_space),
                                 (self.x + self.width, self.y + self.height -
                                  (i + 1 - len(self.elements) + self.capacity) * self.free_space), 5)
                value_text = self.font.render(self.elements[i], True, self.line_color)
                win.blit(value_text, (self.x + (self.width - value_text.get_width()) // 2,
                                      self.y + self.height - (i + 1 - len(self.elements) + self.capacity) *
                                      self.free_space + (self.free_space - value_text.get_height()) // 2))

        pygame.draw.line(win, self.line_color, (self.x, self.y), (self.x, self.y + self.height), 5)
        pygame.draw.line(win, self.line_color, (self.x + self.width, self.y), (self.x + self.width,
                                                                               self.y + self.height), 5)
        pygame.draw.line(win, self.line_color, (self.x, self.y + self.height), (self.x + self.width,
                                                                                self.y + self.height), 5)

        top_y = (self.y + self.height + self.free_space // 2) - (self.top + 1) * self.free_space
        top_width = 60
        top_x = 330 + (100 - top_width) // 2
        pygame.draw.line(win, self.line_color, (top_x, top_y), (top_x + top_width, top_y), 3)
        pygame.draw.line(win, self.line_color, (top_x + top_width, top_y), (top_x + top_width - 10, top_y - 10), 3)
        pygame.draw.line(win, self.line_color, (top_x + top_width, top_y), (top_x + top_width - 10, top_y + 10), 3)
        top_text = self.font.render("top", True, self.line_color)
        win.blit(top_text, (top_x + (top_width - 10 - top_text.get_width()) // 2, top_y - top_text.get_height()))

    def switch_to_dynamic(self):
        self.dynamic = True

    def switch_to_static(self):
        if len(self.elements) > self.capacity:
            self.elements = self.elements[0:self.capacity]
        self.dynamic = False

    def push(self, info, draw, win, settings_buttons, button_and_pair, stack_structure, time=1000):
        if not self.dynamic and len(self.elements) == self.capacity:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Reached limit for static implementation of stack")
            pygame.time.delay(1000)
            return
        draw(win, settings_buttons, button_and_pair, stack_structure, f"Pushing {info} to stack")
        pygame.time.delay(time)
        self.elements.append(info)
        draw(win, settings_buttons, button_and_pair, stack_structure, f"Pushing {info} to stack")
        pygame.time.delay(time)
        if self.top < self.capacity - 1:
            self.top += 1

    def pop(self, draw, win, settings_buttons, button_and_pair, stack_structure, time=1000):
        if len(self.elements) == 0:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Error popping from empty stack")
            pygame.time.delay(1000)
            return
        draw(win, settings_buttons, button_and_pair, stack_structure, "Popping from stack")
        pygame.time.delay(time)
        to_return = self.elements.pop()
        draw(win, settings_buttons, button_and_pair, stack_structure, "Popping from stack")
        pygame.time.delay(time)
        if len(self.elements) < self.capacity:
            self.top -= 1
        return to_return

    def top_(self, draw, win, settings_buttons, button_and_pair, stack_structure):
        if len(self.elements) == 0:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Error empty stack")
            pygame.time.delay(1000)
            return
        return self.elements[-1]

    def pop_value(self, info, draw, win, settings_buttons, button_and_pair, stack_structure):
        if len(self.elements) == 0:
            draw(win, settings_buttons, button_and_pair, stack_structure, "Error popping from empty stack")
            pygame.time.delay(1000)
            return

        alt_stack = Stack(30, 450, 240, 240)
        alt_stack.free_space = 240 * self.free_space // self.height
        alt_stack.dynamic = True
        alt_stack.draw(win)
        pygame.display.update()
        topped = self.pop(draw, win, settings_buttons, button_and_pair, stack_structure, 0)
        while len(self.elements) != 0 and topped != info:
            alt_stack.elements.append(topped)
            draw(win, settings_buttons, button_and_pair, stack_structure, f"{topped} != info")
            alt_stack.draw(win)
            pygame.display.update()
            pygame.time.delay(2000)
            topped = self.pop(draw, win, settings_buttons, button_and_pair, stack_structure, 0)

        if topped == info:
            message = f"{info} found, refilling stack"
        else:
            message = f"{info} not found, refilling stack"

        while len(alt_stack.elements) != 0:
            topped = alt_stack.pop(draw, win, settings_buttons, button_and_pair, stack_structure, 0)
            self.push(topped, draw, win, settings_buttons, button_and_pair, stack_structure, 0)
            draw(win, settings_buttons, button_and_pair, stack_structure, message)
            alt_stack.draw(win)
            pygame.display.update()
            pygame.time.delay(1000)

