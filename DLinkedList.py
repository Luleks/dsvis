import pygame
from LinkedList import Node, LinkedList
import math

BLUR = pygame.image.load("linked_list_folder/wannabe_blur.jpg")


class DLNode(Node):
    llink_text = Node.font.render("LLink", True, Node.text_color)
    dlink_text = Node.font.render("DLink", True, Node.text_color)

    def __init__(self, info, llink, dlink, x, y, reverse):
        super().__init__(info, dlink, x, y, reverse)
        self.llink = llink
        self.dir_count = 2

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


class DLinkedList(LinkedList):

    def __init__(self, tail):
        super().__init__(tail)

    def draw(self, win):
        temp = self.head
        n = 0
        k = 0
        while temp is not None:
            temp.draw(win, int(math.sin((n + 1) * math.pi / 2)), n % 2, int(math.sin((n + 2) * math.pi / 2)),
                      self.__f(k))
            temp = temp.dlink
            n = (n + 1) % 4
            k = (k + 1)

    @staticmethod
    def __f(n):
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
        super()._calculate_after_head()

    def add_to_tail_exist(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = DLNode(info, None, None, 360, 220, False)
            self.tail_node = self.head
            return

        draw(win, settings_buttons, button_and_pair, llist, "Inserting node at tail")

        node_x, node_y, reverse = self._calculate_tail_info()

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

        super()._traverse_to_tail(draw, win, settings_buttons, button_and_pair, llist)

        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        self.tail_node.draw(win, 0, 0, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        node_x, node_y, reverse = self._calculate_tail_info()
        new_node = DLNode(info, None, None, node_x, node_y, reverse)
        new_node.draw(win, 0, 0, 0, 0, False)
        pygame.display.update()
        pygame.time.delay(1000)

        new_node.llink = self.tail_node
        self.tail_node.dlink = new_node
        self.tail_node = new_node
        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        pygame.time.delay(1000)

    def add_after_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        temp, value = super().add_after_index(info, draw, win, settings_buttons, button_and_pair, llist)
        if temp is None and value is None:
            return

        new_node = DLNode(value, temp, temp.dlink, temp.dlink.x, temp.dlink.y, temp.dlink.reverse)
        temp.dlink.llink = new_node
        temp.dlink = new_node

        super()._shift_right(new_node)

    def delete_from_head(self, draw, win, settings_buttons, button_and_pair, llist):
        if super().delete_from_head(draw, win, settings_buttons, button_and_pair, llist) == -1:
            return

        self.count -= 1
        info_to_return = self.head.info
        temp1 = self.tail_node
        while temp1.llink is not None:
            temp1.x = temp1.llink.x
            temp1.y = temp1.llink.y
            temp1.reverse = temp1.llink.reverse
            temp1 = temp1.llink

        if self.head.dlink is not None:
            self.head.dlink.llink = None
        self.head = self.head.dlink
        return info_to_return

    def delete_from_tail_exist(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return
        elif self.count == 1:
            return self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)

        temp = self.tail_node
        temp_to_return = temp.info
        draw(win, settings_buttons, button_and_pair, llist, f"Tail selected, commencing deletion")
        temp.draw(win, 0, 0, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        self.tail_node.llink.dlink = None
        self.tail_node = self.tail_node.llink
        self.count -= 1
        return temp_to_return

    def delete_from_tail_noptr(self, draw, win, settings_buttons, button_and_pair, llist):
        if super().delete_from_tail_noptr(draw, win, settings_buttons, button_and_pair, llist) == -1:
            return

        temp_to_return = self.tail_node.info
        self.tail_node.llink.dlink = None
        self.tail_node = self.tail_node.llink
        self.count -= 1

        return temp_to_return

    def delete_value(self, info, draw, win, settings_buttons, button_and_pair, llist):
        temp = super().delete_value(info, draw, win, settings_buttons, button_and_pair, llist)
        if temp == -1:
            return
        elif temp == 1:
            self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)
        elif temp == 2:
            self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
        else:
            temp1 = self.tail_node
            while temp1 != temp:
                temp1.x = temp1.llink.x
                temp1.y = temp1.llink.y
                temp1.reverse = temp1.llink.reverse
                temp1 = temp1.llink

            temp.llink.dlink = temp.dlink
            temp.dlink.llink = temp.llink

    def delete_from_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        temp = super().delete_from_index(info, draw, win, settings_buttons, button_and_pair, llist)
        if temp == -1:
            return
        elif temp == 1:
            self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)
        elif temp == 2:
            self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
        else:
            temp1 = self.tail_node
            while temp1 != temp:
                temp1.x = temp1.llink.x
                temp1.y = temp1.llink.y
                temp1.reverse = temp1.llink.reverse
                temp1 = temp1.llink

            temp.llink.dlink = temp.dlink
            temp.dlink.llink = temp.llink
            self.count -= 1
