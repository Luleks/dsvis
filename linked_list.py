import os
import pygame
from button import Button
from input_form import InputForm
from SLinkedList import SLinkedList
from DLinkedList import DLinkedList

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TITLE_FONT = pygame.font.SysFont("erasict", 50)
TEXT_BOX_FONT = pygame.font.SysFont("erasict", 25)
BACKGROUND_IMAGE = pygame.image.load("linked_list_folder/linked_list_background.jpg")


def clear_effects(key_val):
    for key, value in key_val.items():
        if isinstance(value, InputForm):
            value.error_rect = False


def draw(win, settings_buttons, button_and_pair, llist, text_box_message):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    title = TITLE_FONT.render("LINKED LIST", True, WHITE)
    win.blit(title, ((win.get_width() - title.get_width()) // 2, (100 - title.get_height()) // 2))

    pygame.draw.rect(win, GREY, (330, 130, 540, 60))
    textbox_message = TEXT_BOX_FONT.render(text_box_message, True, BLACK)
    win.blit(textbox_message, (330 + (540 - textbox_message.get_width()) // 2,
                               130 + (60 - textbox_message.get_height()) // 2))

    for button in settings_buttons:
        button.draw(win)

    for button, pair in button_and_pair.items():
        button.draw(win)
        pair.draw(win)

    llist.draw(win)

    pygame.display.update()


def linked_list(win):
    clock = pygame.time.Clock()

    sll_button = Button(30, 100, 120, 60, GREY, "SLL", BLACK, True)
    dll_button = Button(150, 100, 120, 60, GREY, "DLL", BLACK)
    help_button = Button(30, 160, 120, 60, GREY, "help", BLACK)
    ptr_to_tail = Button(150, 160, 120, 60, GREY, "tail-ptr", BLACK)
    settings_buttons = [sll_button, dll_button, help_button, ptr_to_tail]

    add_to_head = Button(30, 250, 240, 60, GREY, "add to head", BLACK)
    add_to_tail = Button(30, 400, 240, 60, GREY, "add to tail", BLACK)
    add_after_index = Button(30, 550, 240, 60, GREY, "add after index", BLACK)
    delete_from_head = Button(930, 100, 240, 60, GREY, "delete from head", BLACK)
    delete_from_tail = Button(930, 250, 240, 60, GREY, "delete from tail", BLACK)
    delete_value = Button(930, 400, 240, 60, GREY, "delete value", BLACK)
    delete_from_index = Button(930, 550, 240, 60, GREY, "delete from index", BLACK)

    add_to_head_ev = InputForm(30, 310, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    add_to_tail_ev = InputForm(30, 460, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    add_after_index_ev = InputForm(30, 610, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    delete_value_ev = InputForm(930, 460, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    delete_from_index_ev = InputForm(930, 610, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    delete_from_head_ret = Button(930, 160, 240, 60, GREY, "returned value", BLACK)
    delete_from_tail_ret = Button(930, 310, 240, 60, GREY, "returned value", BLACK)

    button_and_pair = {add_to_head: add_to_head_ev, add_to_tail: add_to_tail_ev, add_after_index: add_after_index_ev,
                       delete_from_head: delete_from_head_ret, delete_from_tail: delete_from_tail_ret,
                       delete_value: delete_value_ev, delete_from_index: delete_from_index_ev}

    sll = SLinkedList(False)
    dll = DLinkedList(False)

    llist = sll

    text_box_message = ""

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                clear_effects(button_and_pair)
                text_box_message = ""
                pos = pygame.mouse.get_pos()

                delete_from_head_ret.text = "returned value"
                delete_from_tail_ret.text = "returned value"

                for button in settings_buttons:
                    if button.is_over(pos):
                        button.active = not button.active
                        if button.text == "SLL":
                            settings_buttons[1].active = not settings_buttons[2].active
                            llist = sll
                            sll.tail = dll.tail
                        elif button.text == "DLL":
                            settings_buttons[0].active = not settings_buttons[0].active
                            llist = dll
                            dll.tail = sll.tail
                        elif button.text == "tail-ptr":
                            llist.tail = not llist.tail
                        elif button.text == "help":
                            path = os.path.abspath('linked_list_folder/linked_list_help.pdf')
                            os.startfile(path)
                            button.active = False

                for button, pair in button_and_pair.items():
                    if button.is_over(pos):

                        if button.text == "add to head":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Input integer value between 0 and 999"
                            elif not pair.text.isdigit():
                                pair.error_rect = True
                                text_box_message = "Letters and characters other than digits not allowed"
                            elif llist.count == 8:
                                pair.error_rect = True
                                text_box_message = "Cannot add more than 8 nodes"
                            else:
                                llist.add_to_head(pair.text, draw, win, settings_buttons, button_and_pair, llist)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                        elif button.text == "add to tail":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Input integer value between 0 and 999"
                            elif not pair.text.isdigit():
                                pair.error_rect = True
                                text_box_message = "Letters and characters other than digits not allowed"
                            elif llist.count == 8:
                                pair.error_rect = True
                                text_box_message = "Cannot add more than 8 nodes"
                            else:
                                llist.add_to_tail(pair.text, draw, win, settings_buttons, button_and_pair, llist)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                        elif button.text == "add after index":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Input index and value both between 0 and 9 in format index,value"
                            elif not pair.text[0].isdigit() or not pair.text[1] == ',' or not pair.text[2].isdigit():
                                pair.error_rect = True
                                text_box_message = "Input format is index,value. ex. 2,3"
                            elif llist.count == 8:
                                pair.error_rect = True
                                text_box_message = "Cannot add more than 8 nodes"
                            else:
                                llist.add_after_index(pair.text, draw, win, settings_buttons, button_and_pair, llist)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                        elif button.text == "delete from head":
                            ret_value = llist.delete_from_head(draw, win, settings_buttons, button_and_pair, llist)
                            if ret_value is not None:
                                pair.text = "returned value"
                                pair.text = pair.text + f": {ret_value}"

                        elif button.text == "delete from tail":
                            ret_value = llist.delete_from_tail(draw, win, settings_buttons, button_and_pair, llist)
                            if ret_value is not None:
                                pair.text = "returned value"
                                pair.text = pair.text + f": {ret_value}"

                        elif button.text == "delete value":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Value required"
                            elif not pair.text.isdigit():
                                pair.error_rect = True
                                text_box_message = "Letters and characters other than digits not allowed"
                            else:
                                llist.delete_value(pair.text, draw, win, settings_buttons, button_and_pair, llist)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                        elif button.text == "delete from index":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Index required"
                            elif not pair.text.isdigit():
                                pair.error_rect = True
                                text_box_message = "Letters and characters other than digits not allowed"
                            else:
                                llist.delete_from_index(pair.text, draw, win, settings_buttons, button_and_pair, llist)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                    if isinstance(pair, InputForm):
                        pair.state_change(pos)

            for pair in button_and_pair.values():
                if isinstance(pair, InputForm):
                    pair.add_text(event)

        pos = pygame.mouse.get_pos()
        for button in settings_buttons:
            button.shift_color(pos)
        for button, pair in button_and_pair.items():
            button.shift_color(pos)
            if isinstance(pair, InputForm):
                pair.shift_color(pos)
        draw(win, settings_buttons, button_and_pair, llist, text_box_message)
