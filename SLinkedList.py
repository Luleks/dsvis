import pygame
from LinkedList import Node, LinkedList
import math

BLUR = pygame.image.load("linked_list_folder/wannabe_blur.jpg")


class SLNode(Node):
    dlink_text = Node.font.render("Link", True, Node.text_color)

    def __init__(self, info, link, x, y, reverse):
        super().__init__(info, link, x, y, reverse)

    def draw(self, win, dir_x, dir_y, additional_rect=False):
        pygame.draw.rect(win, SLNode.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, SLNode.text_color, (self.x, self.y, self.width, self.height), 2)
        pygame.draw.line(win, SLNode.text_color, (self.x + self.width // 2, self.y),
                         (self.x + self.width // 2, self.y + self.height), 2)
        self.draw_links(win, dir_x, dir_y)

        if additional_rect:
            pygame.draw.rect(win, pygame.Color("red"), (self.x, self.y, self.width, self.height), 2)

        info_text = SLNode.font.render(f"{self.info}", True, SLNode.text_color)
        if not self.reverse:
            win.blit(info_text, (self.x + (self.width // 2 - info_text.get_width()) // 2,
                                 self.y + (self.height - info_text.get_height()) // 2))
            win.blit(SLNode.dlink_text, (self.x + self.width // 2 + (self.width // 2 - SLNode.dlink_text.get_width()) // 2,
                                         self.y + (self.height - SLNode.dlink_text.get_height()) // 2))
        else:
            win.blit(info_text, (self.x + self.width // 2 + (self.width // 2 - info_text.get_width()) // 2,
                                 self.y + (self.height - info_text.get_height()) // 2))
            win.blit(SLNode.dlink_text, (self.x + (self.width // 2 - SLNode.dlink_text.get_width()) // 2,
                                         self.y + (self.height - SLNode.dlink_text.get_height()) // 2))

    def draw_links(self, win, dir_x, dir_y):
        if self.dlink is None:
            return
        if not dir_x and not dir_y:
            return
        if dir_x == 1:
            pygame.draw.line(win, SLNode.text_color, (self.x + self.width, self.y + self.height // 2),
                             (self.x + self.width + SLNode.hgap, self.y + self.height // 2), 2)
        elif dir_x == -1:
            pygame.draw.line(win, SLNode.text_color, (self.x, self.y + self.height // 2),
                             (self.x - SLNode.hgap, self.y + self.height // 2), 2)
        elif dir_y == 1 and not self.reverse:
            pygame.draw.line(win, SLNode.text_color, (self.x + self.width * 3 // 4, self.y + self.height),
                             (self.x + self.width * 3 // 4, self.y + self.height + SLNode.vgap), 2)
        else:
            pygame.draw.line(win, SLNode.text_color, (self.x + self.width * 1 // 4, self.y + self.height),
                             (self.x + self.width * 1 // 4, self.y + self.height + SLNode.vgap), 2)


class SLinkedList(LinkedList):

    def __init__(self, tail):
        super().__init__(tail)

    def add_to_head(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = SLNode(info, None, 360, 220, False)
            self.tail_node = self.head
            return

        draw(win, settings_buttons, button_and_pair, llist, "Inserting node to head")

        win.blit(BLUR, (0, 0))
        pygame.display.update()
        pygame.time.delay(1000)

        temp_node = SLNode(info, None, 60, 220, False)
        temp_node.draw(win, 1, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        temp_node.dlink = self.head
        temp_node.draw(win, 1, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        self.head = temp_node
        super()._calculate_after_head()

    def add_to_tail_exist(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = SLNode(info, None, 360, 220, False)
            self.tail_node = self.head
            return

        draw(win, settings_buttons, button_and_pair, llist, "Inserting node at tail")

        node_x, node_y, reverse = self._calculate_tail_info()

        new_node = SLNode(info, None, node_x, node_y, reverse)
        new_node.draw(win, 0, 0)
        pygame.display.update()
        pygame.time.delay(1000)

        self.tail_node.dlink = new_node
        self.tail_node = new_node

    def add_to_tail_noptr(self, info, draw, win, settings_buttons, button_and_pair, llist):
        self.count += 1
        if self.head is None:
            self.head = SLNode(info, None, 360, 220, False)
            self.tail_node = self.head
            return

        super()._traverse_to_tail(draw, win, settings_buttons, button_and_pair, llist)

        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        self.tail_node.draw(win, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        node_x, node_y, reverse = self._calculate_tail_info()
        new_node = SLNode(info, None, node_x, node_y, reverse)
        new_node.draw(win, 0, 0, False)
        pygame.display.update()
        pygame.time.delay(1000)

        self.tail_node.dlink = new_node
        self.tail_node = new_node
        draw(win, settings_buttons, button_and_pair, llist, "Tail found, inserting at tail")
        pygame.time.delay(1000)

    def add_after_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        temp, value = super().add_after_index(info, draw, win, settings_buttons, button_and_pair, llist)
        if temp is None and value is None:
            return

        new_node = SLNode(value, temp.dlink, temp.dlink.x, temp.dlink.y, temp.dlink.reverse)
        temp.dlink = new_node

        super()._shift_right(new_node)

    def __reverse(self):
        prev, temp, next_n = None, self.head, None
        while temp is not None:
            next_n = temp.dlink
            temp.dlink = prev
            prev = temp
            temp = next_n
        self.head = prev

    def delete_from_head(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return
        temp = self.head
        draw(win, settings_buttons, button_and_pair, llist, f"Head selected, commencing deletion")
        temp.draw(win, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        info_to_return = temp.info
        self.__reverse()
        temp1 = self.head
        while temp1.dlink is not None:
            temp1.x = temp1.dlink.x
            temp1.y = temp1.dlink.y
            temp1.reverse = temp1.dlink.reverse
            temp1 = temp1.dlink
        self.__reverse()

        self.head = temp.dlink
        self.count -= 1
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
        temp.draw(win, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        temp = self.head
        while temp.dlink != self.tail_node:
            temp = temp.dlink
        temp.dlink = None
        self.tail_node = temp
        self.count -= 1
        return temp_to_return

    def delete_from_tail_noptr(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return
        elif self.count == 1:
            return self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)

        temp = self.head
        while temp.dlink is not None:
            draw(win, settings_buttons, button_and_pair, llist, "Searching for tail")
            temp.draw(win, 0, 0, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink

        draw(win, settings_buttons, button_and_pair, llist, "Tail found, commencing deletion")
        temp.draw(win, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)
        temp_to_return = temp.info

        temp = self.head
        while temp.dlink != self.tail_node:
            temp = temp.dlink
        temp.dlink = None
        self.tail_node = temp
        self.count -= 1

        return temp_to_return

    def delete_from_tail(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.tail:
            return self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
        return self.delete_from_tail_noptr(draw, win, settings_buttons, button_and_pair, llist)

    def delete_value(self, info, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return

        prev = None
        temp = self.head
        while temp is not None and temp.info != info:
            draw(win, settings_buttons, button_and_pair, llist, "Searching for value")
            temp.draw(win, 0, 0, True)
            pygame.display.update()
            pygame.time.delay(1000)

            prev = temp
            temp = temp.dlink

        if temp is None:
            draw(win, settings_buttons, button_and_pair, llist, f"List index out of range")
            pygame.display.update()
            pygame.time.delay(1000)
        elif temp == self.head:
            self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)
        elif temp == self.tail_node:
            self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
        else:
            self.count -= 1
            draw(win, settings_buttons, button_and_pair, llist, "Node found, commencing deletion")
            temp.draw(win, 0, 0, True)
            pygame.display.update()
            pygame.time.delay(1000)

            self.__reverse()
            temp1 = self.head
            while temp1 != temp:
                temp1.x = temp1.dlink.x
                temp1.y = temp1.dlink.y
                temp1.reverse = temp1.dlink.reverse
                temp1 = temp1.dlink
            self.__reverse()

            prev.dlink = temp.dlink

    def delete_from_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        info = int(info)
        if self.count <= 0:
            draw(win, settings_buttons, button_and_pair, llist, "Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return
        elif info >= self.count:
            draw(win, settings_buttons, button_and_pair, llist, "List index out of range")
            pygame.time.delay(2000)
            return

        prev = None
        temp = self.head
        ind = 0
        while ind != info:
            draw(win, settings_buttons, button_and_pair, llist, f"Searching for index {info}, current:{ind}")
            temp.draw(win, 0, 0, True)
            pygame.display.update()
            pygame.time.delay(1000)

            prev = temp
            temp = temp.dlink
            ind += 1

        draw(win, settings_buttons, button_and_pair, llist, f"Index {info} found, commencing deletion")
        temp.draw(win, 0, 0, True)
        pygame.display.update()
        pygame.time.delay(1000)

        if temp == self.head:
            self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)
            return
        elif temp == self.tail_node:
            self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
            return

        self.__reverse()
        temp1 = self.head
        while temp1 != temp:
            temp1.x = temp1.dlink.x
            temp1.y = temp1.dlink.y
            temp1.reverse = temp1.dlink.reverse
            temp1 = temp1.dlink
        self.__reverse()

        prev.dlink = temp.dlink
        self.count -= 1

    def draw(self, win):
        temp = self.head
        n = 0
        while temp is not None:
            temp.draw(win, int(math.sin((n + 1) * math.pi / 2)), n % 2)
            temp = temp.dlink
            n = (n + 1) % 4
