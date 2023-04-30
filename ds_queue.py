import pygame
import os
from button import Button
from input_form import InputForm
from Queue_ import Queue

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TITLE_FONT = pygame.font.SysFont("erasict", 50)
TEXT_BOX_FONT = pygame.font.SysFont("erasict", 25)
BACKGROUND_IMAGE = pygame.image.load("queue_folder/queue_background.jpg")


def clear_effects(key_val):
    for key, value in key_val.items():
        if isinstance(value, InputForm):
            value.error_rect = False


def draw(win, settings_buttons, button_and_pair, queue_structure, text_box_message):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    title = TITLE_FONT.render("QUEUE", True, WHITE)
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

    queue_structure.draw(win)

    pygame.display.update()


def queue(win):
    clock = pygame.time.Clock()

    static_button = Button(30, 260, 240, 60, GREY, "Static", BLACK, True)
    dynamic_button = Button(30, 320, 240, 60, GREY, "Dynamic", BLACK)
    help_button = Button(30, 380, 240, 60, GREY, "help", BLACK)
    settings_buttons = [static_button, dynamic_button, help_button]

    enqueue = Button(930, 100, 240, 60, GREY, "ENQUEUE", BLACK)
    dequeue = Button(930, 250, 240, 60, GREY, "DEQUEUE", BLACK)
    dequeue_value = Button(930, 400, 240, 60, GREY, "DEQUEUE value", BLACK)
    front = Button(930, 550, 240, 60, GREY, "FRONT", BLACK)

    enqueue_value_ev = InputForm(930, 160, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    dequeue_ret = Button(930, 310, 240, 60, GREY, "returned value", BLACK)
    dequeue_value_ev = InputForm(930, 460, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    front_ret = Button(930, 610, 240, 60, GREY, "returned value", BLACK)

    button_and_pair = {enqueue: enqueue_value_ev, dequeue: dequeue_ret, dequeue_value: dequeue_value_ev,
                       front: front_ret}

    text_box_message = ""
    queue_structure = Queue(430, 220, 400, 420)

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

                dequeue_ret.text = "returned value"
                front_ret.text = "returned value"

                for button in settings_buttons:
                    if button.is_over(pos):

                        if button.text == "help":
                            path = os.path.abspath('queue_folder/queue_help.pdf')
                            os.startfile(path)
                            button.active = False

                        elif button.text == "Static" and not button.active:
                            settings_buttons[1].active = False
                            button.active = True
                            queue_structure.switch_to_static()

                        elif button.text == "Dynamic" and not button.active:
                            settings_buttons[0].active = False
                            button.active = True
                            queue_structure.switch_to_dynamic()

                for button, pair in button_and_pair.items():
                    if button.is_over(pos):

                        if button.text == "ENQUEUE":
                            if pair.text == "":
                                pair.error_rect = True
                                text_box_message = "Input integer value between 0 and 999"
                            elif not pair.text.isdigit():
                                pair.error_rect = True
                                text_box_message = "Letters and characters other than digits not allowed"
                            else:
                                queue_structure.enqueue(pair.text, draw, win, settings_buttons, button_and_pair,
                                                        queue_structure)
                                pair.text = ""
                                clear_effects(button_and_pair)
                                text_box_message = ""

                        elif button.text == "DEQUEUE":
                            pass

                        elif button.text == "FRONT":
                            pass

                        elif button.text == "DEQUEUE VALUE":
                            pass

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

        draw(win, settings_buttons, button_and_pair, queue_structure, text_box_message)
