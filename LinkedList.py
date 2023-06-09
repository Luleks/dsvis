import pygame
import math


class Node:
    font = pygame.font.SysFont("comicsans", 20)
    width = 180
    height = 60
    color = (128, 128, 128)
    text_color = (0, 0, 0)
    hgap = 120
    vgap = 60

    link_text = font.render("Link", True, text_color)

    def __init__(self, info, dlink, x, y, reverse):
        self.info = info
        self.dlink = dlink
        self.x = x
        self.y = y
        self.reverse = reverse
        self.dir_count = 1


class LinkedList:

    def __init__(self, tail):
        self.head = None
        self.tail = tail
        self.tail_node = None
        self.count = 0

    def _calculate_after_head(self):
        # Calculating coords of nodes after new head had been inserted.
        temp = self.head
        y, i = 220, 0
        while temp is not None:
            temp.y = y
            if i % 2 == 1:
                y += (Node.height + Node.vgap)
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

    def _calculate_tail_info(self):
        if (self.count + 1) % 4 == 0 or (self.count + 2) % 4 == 0:
            node_x = 660
        else:
            node_x = 360
        if self.count % 2 == 1:
            node_y = self.tail_node.y + Node.vgap + Node.height
        else:
            node_y = self.tail_node.y
        if (self.count + 1) % 4 == 0 or self.count % 4 == 0:
            reverse = True
        else:
            reverse = False
        return node_x, node_y, reverse

    @staticmethod
    def __draw_one_of_two(temp, win, ad_rect):
        if temp.dir_count == 1:
            temp.draw(win, 0, 0, ad_rect)
        elif temp.dir_count == 2:
            temp.draw(win, 0, 0, 0, 0, ad_rect)

    def _traverse_to_tail(self, draw, win, settings_buttons, button_and_pair, llist):
        temp = self.head
        while temp.dlink is not None:
            draw(win, settings_buttons, button_and_pair, llist, "Searching for tail")
            LinkedList.__draw_one_of_two(temp, win, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink

    def _shift_right(self, new_node):
        temp = new_node.dlink
        while temp.dlink is not None:
            temp.x = temp.dlink.x
            temp.y = temp.dlink.y
            temp.reverse = temp.dlink.reverse
            temp = temp.dlink
        x, y, reverse = self._calculate_tail_info()
        temp.x, temp.y, temp.reverse = x, y, reverse

    def add_to_tail_exist(self, info, draw, win, settings_buttons, button_and_pair, llist):
        pass

    def add_to_tail_noptr(self, info, draw, win, settings_buttons, button_and_pair, llist):
        pass

    def add_to_tail(self, info, draw, win, settings_buttons, button_and_pair, llist):
        if self.tail:
            self.add_to_tail_exist(info, draw, win, settings_buttons, button_and_pair, llist)
            return
        self.add_to_tail_noptr(info, draw, win, settings_buttons, button_and_pair, llist)

    def add_after_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        index, value = tuple(info.split(","))
        index = int(index)
        if index >= self.count:
            draw(win, settings_buttons, button_and_pair, llist, "Index out of range")
            pygame.time.delay(2000)
            return None, None
        elif index == self.count - 1:
            self.add_to_tail_noptr(value, draw, win, settings_buttons, button_and_pair, llist)
            return None, None

        self.count += 1
        temp = self.head
        ind = 0
        while ind != index:
            draw(win, settings_buttons, button_and_pair, llist, f"Searching for index {index}, current:{ind}")
            LinkedList.__draw_one_of_two(temp, win, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink
            ind += 1

        draw(win, settings_buttons, button_and_pair, llist, f"Index {index} found, inserting node")
        LinkedList.__draw_one_of_two(temp, win, True)
        pygame.display.update()
        pygame.time.delay(1000)

        return temp, value

    def delete_from_head(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return -1

        draw(win, settings_buttons, button_and_pair, llist, f"Head selected, commencing deletion")
        self.__draw_one_of_two(self.head, win, True)
        pygame.display.update()
        pygame.time.delay(1000)

    def delete_from_tail_exist(self, draw, win, settings_buttons, button_and_pair, llist):
        pass

    def delete_from_tail_noptr(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return -1
        elif self.count == 1:
            return self.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)

        self._traverse_to_tail(draw, win, settings_buttons, button_and_pair, llist)

        draw(win, settings_buttons, button_and_pair, llist, "Tail found, commencing deletion")
        self.__draw_one_of_two(self.tail_node, win, True)
        pygame.display.update()
        pygame.time.delay(1000)

    def delete_from_tail(self, draw, win, settings_buttons, button_and_pair, llist):
        if self.tail:
            return self.delete_from_tail_exist(draw, win, settings_buttons, button_and_pair, llist)
        return self.delete_from_tail_noptr(draw, win, settings_buttons, button_and_pair, llist)

    def delete_value(self, info, draw, win, settings_buttons, button_and_pair, llist):
        if self.head is None:
            draw(win, settings_buttons, button_and_pair, llist, f"Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return -1

        temp = self.head
        while temp is not None and temp.info != info:
            draw(win, settings_buttons, button_and_pair, llist, "Searching for value")
            self.__draw_one_of_two(temp, win, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink

        if temp is None:
            draw(win, settings_buttons, button_and_pair, llist, f"List index out of range")
            pygame.display.update()
            pygame.time.delay(1000)
            return -1
        elif temp == self.head:
            return 1
        elif temp == self.tail_node:
            return 2
        else:
            self.count -= 1
            draw(win, settings_buttons, button_and_pair, llist, "Node found, commencing deletion")
            self.__draw_one_of_two(temp, win, True)
            pygame.display.update()
            pygame.time.delay(1000)
            return temp

    def delete_from_index(self, info, draw, win, settings_buttons, button_and_pair, llist):
        info = int(info)
        if self.count <= 0:
            draw(win, settings_buttons, button_and_pair, llist, "Error: Trying to delete from empty list")
            pygame.time.delay(2000)
            return -1
        elif info >= self.count:
            draw(win, settings_buttons, button_and_pair, llist, "List index out of range")
            pygame.time.delay(2000)
            return -1

        temp = self.head
        ind = 0
        while ind != info:
            draw(win, settings_buttons, button_and_pair, llist, f"Searching for index {info}, current:{ind}")
            self.__draw_one_of_two(temp, win, True)
            pygame.display.update()
            pygame.time.delay(1000)

            temp = temp.dlink
            ind += 1

        draw(win, settings_buttons, button_and_pair, llist, f"Index {info} found, commencing deletion")
        self.__draw_one_of_two(temp, win, True)
        pygame.display.update()
        pygame.time.delay(1000)

        if temp == self.head:
            return 1
        elif temp == self.tail_node:
            return 2
        else:
            return temp
