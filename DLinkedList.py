import pygame
import math

BLUR = pygame.image.load("linked_list_folder/wannabe_blur.jpg")


class DLNode:
    font = pygame.font.SysFont("comicsans", 20)
    parts = 3
    width = 180
    height = 60
    color = (128, 128, 128)
    text_color = (0, 0, 0)
    hgap = 120
    vgap = 60
    llink_text = font.render("LLink", True, text_color)
    dlink_text = font.render("DLink", True, text_color)

    def __init__(self, info, llink, dlink, x, y, reverse):
        self.info = info
        self.llink = llink
        self.dlink = dlink
        self.x = x
        self.y = y
        self.reverse = reverse

    def draw(self, win, ddir_x, ddir_y, ldir_x, ldir_y, additional_rect=False):
        pygame.draw.rect(win, DLNode.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, DLNode.text_color, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.line(win, DLNode.text_color, (self.x + self.width // 3, self.y),
                         (self.x + self.width // 3, self.y + self.height), 2)
        pygame.draw.line(win, DLNode.text_color, (self.x + 2 * self.width // 3, self.y),
                         (self.x + 2 * self.width // 3, self.y + self.height), 2)
        self.draw_links(win, ddir_x, ddir_y, ldir_x, ldir_y)

        if additional_rect:
            pygame.draw.rect(win, pygame.Color("red"), (self.x, self.y, self.width, self.height), 2)

        info_text = DLNode.font.render(f"{self.info}", True, DLNode.text_color)
        if not self.reverse:
            win.blit(info_text, (self.x + self.width // 3 + (self.width // 3 - info_text.get_width()) // 2,
                                 self.y + (self.height - info_text.get_height()) // 2))
            win.blit(DLNode.llink_text, (self.x + (self.width // 3 - DLNode.llink_text.get_width()) // 2,
                                         self.y + (self.height - DLNode.llink_text.get_height()) // 2))
            win.blit(DLNode.dlink_text,
                     (self.x + 2 * self.width // 3 + (self.width // 3 - DLNode.dlink_text.get_width()) // 2,
                      self.y + (self.height - DLNode.dlink_text.get_height()) // 2))
        else:
            win.blit(info_text, (self.x + self.width // 3 + (self.width // 3 - info_text.get_width()) // 2,
                                 self.y + (self.height - info_text.get_height()) // 2))
            win.blit(DLNode.dlink_text, (self.x + (self.width // 3 - DLNode.dlink_text.get_width()) // 2,
                                         self.y + (self.height - DLNode.dlink_text.get_height()) // 2))
            win.blit(DLNode.llink_text,
                     (self.x + 2 * self.width // 3 + (self.width // 3 - DLNode.llink_text.get_width()) // 2,
                      self.y + (self.height - DLNode.llink_text.get_height()) // 2))

    def draw_links(self, win, ddir_x, ddir_y, ldir_x, ldir_y):
        if self.dlink is not None and not (ddir_x == 0 and ddir_y == 0):
            if ddir_x == 1:
                pygame.draw.line(win, pygame.Color("white"), (self.x + self.width, self.y + self.height // 3),
                                 (self.x + self.width + DLNode.hgap, self.y + self.height // 3), 2)
            elif ddir_x == -1:
                pygame.draw.line(win, pygame.Color("white"), (self.x, self.y + self.height // 3),
                                 (self.x - DLNode.hgap, self.y + self.height // 3), 2)
            elif ddir_y == 1 and not self.reverse:
                pygame.draw.line(win, pygame.Color("white"), (self.x + 8 * self.width // 9, self.y + self.height),
                                 (self.x + 8 * self.width // 9, self.y + self.height + DLNode.vgap), 2)
            else:
                pygame.draw.line(win, pygame.Color("white"), (self.x + 2 * self.width // 9, self.y + self.height),
                                 (self.x + 2 * self.width // 9, self.y + self.height + DLNode.vgap), 2)
        if self.llink is not None and not (ldir_y == 0 and ldir_x == 0):
            if ldir_x == 1:
                pygame.draw.line(win, pygame.Color("red"), (self.x + self.width, self.y + 2 * self.height // 3),
                                 (self.x + self.width + DLNode.hgap, self.y + 2 * self.height // 3), 2)
            elif ldir_x == -1:
                pygame.draw.line(win, pygame.Color("red"), (self.x, self.y + 2 * self.height // 3),
                                 (self.x - DLNode.hgap, self.y + 2 * self.height // 3), 2)
            elif ldir_y == -1 and not self.reverse:
                pygame.draw.line(win, pygame.Color("red"), (self.x + self.width // 9, self.y),
                                 (self.x + self.width // 9, self.y - DLNode.vgap), 2)
            else:
                pygame.draw.line(win, pygame.Color("red"), (self.x + 7 * self.width // 9, self.y),
                                 (self.x + 7 * self.width // 9, self.y - DLNode.vgap), 2)


class DLinkedList:

    def __init__(self, tail):
        self.head = None
        self.tail = tail
        self.tail_node = None
        self.count = 0

    def draw(self, win):
        temp = self.head
        n = 0
        k = 0
        while temp is not None:
            temp.draw(win, int(math.sin((n + 1) * math.pi / 2)), n % 2, int(math.sin((n + 2) * math.pi / 2)),
                      self.__f(k))
            if self.count >= 7:
                print(int(math.sin((n + 2) * math.pi / 2)), self.__f(k), k)
            temp = temp.dlink
            n = (n + 1) % 4
            k = (k + 1)

    def __f(self, n):
        if n in {2, 4, 6}:
            return -1
        return 0

    def add_to_head(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = DLNode(info, None, None, 360, 220, False)
            self.tail_node = self.head
            return

        draw(win, settings_buttons, button_and_pair, llist, "Inserting node to head")

        win.blit(BLUR, (0, 0))
        pygame.display.update()
        pygame.time.delay(1000)

        temp_node = DLNode(info, None, None, 60, 220, False)
        temp_node.draw(win, 0, 0, 0, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        temp_node.dlink = self.head
        self.head.llink = temp_node
        temp_node.draw(win, 1, 0, 0, 0)
        self.head.draw(win, 1, 0, -1, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        self.head = temp_node
        temp = self.head
        y, i = 220, 0
        while temp is not None:
            temp.y = y
            if i % 2 == 1:
                y += (DLNode.height + DLNode.vgap)
            if (i + 1) % 4 == 0 or (i + 2) % 4 == 0:
                temp.reverse = True
            else:
                temp.reverse = False
            if (i - 1) % 4 == 0 or (i + 2) % 4 == 0:
                temp.x = 660
            else:
                temp.x = 360
            i += 1
            temp = temp.dlink

    def add_to_tail(self, info, draw, win, settings_buttons, button_and_pair, llist):
        if self.tail:
            self.add_to_tail_exist(info, draw, win, settings_buttons, button_and_pair, llist)
            return
        self.add_to_tail_noptr(info, draw, win, settings_buttons, button_and_pair, llist)

    def __calculate_tail_info(self):
        if (self.count + 1) % 4 == 0 or (self.count + 2) % 4 == 0:
            node_x = 660
        else:
            node_x = 360
        if self.count % 2 == 1:
            node_y = self.tail_node.y + DLNode.vgap + DLNode.height
        else:
            node_y = self.tail_node.y
        if (self.count + 1) % 4 == 0 or self.count % 4 == 0:
            reverse = True
        else:
            reverse = False
        return node_x, node_y, reverse

    def add_to_tail_exist(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = DLNode(info, None, None, 360, 220, False)
            self.tail_node = self.head
            return

        draw(win, settings_buttons, button_and_pair, llist, "Inserting node at tail")

        node_x, node_y, reverse = self.__calculate_tail_info()

        new_node = DLNode(info, None, None, node_x, node_y, reverse)
        new_node.draw(win, 0, 0, 0, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        new_node.llink = self.tail_node
        self.tail_node.dlink = new_node
        self.tail_node = new_node

    def add_to_tail_noptr(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = DLNode(info, None, None, 360, 220, False)
            self.tail_node = self.head
            return

        temp = self.head
        while temp.dlink is not None:
            draw(win, settings_buttons, button_and_pair, llist, "Searching for tail")
            temp.draw(win, 0, 0, 0, 0, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink

        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        temp.draw(win, 0, 0, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        node_x, node_y, reverse = self.__calculate_tail_info()
        new_node = DLNode(info, None, None, node_x, node_y, reverse)
        new_node.draw(win, 0, 0, 0, 0, False)
        pygame.display.update()
        pygame.time.delay(1000)

        new_node.llink = self.tail_node
        self.tail_node.dlink = new_node
        self.tail_node = new_node
        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        pygame.time.delay(1000)
