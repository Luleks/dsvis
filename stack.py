import pygame
import os
from button import Button
from input_form import InputForm
from Stack_ import Stack

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
TITLE_FONT = pygame.font.SysFont("erasict", 50)
TEXT_BOX_FONT = pygame.font.SysFont("erasict", 25)
BACKGROUND_IMAGE = pygame.image.load("stack_folder/stack_background.jpg")


def clear_effects(key_val):
    for key, value in key_val.items():
        if isinstance(value, InputForm):
            value.error_rect = False


def draw(win, settings_buttons, button_and_pair, text_box_message, stack_structure):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    title = TITLE_FONT.render("STACK", True, WHITE)
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

    stack_structure.draw(win)

    pygame.display.update()


def stack(win):
    clock = pygame.time.Clock()

    static_button = Button(30, 260, 240, 60, GREY, "Static", BLACK, True)
    dynamic_button = Button(30, 320, 240, 60, GREY, "Dynamic", BLACK)
    help_button = Button(30, 380, 240, 60, GREY, "help", BLACK)
    settings_buttons = [static_button, dynamic_button, help_button]

    push = Button(930, 100, 240, 60, GREY, "PUSH", BLACK)
    pop = Button(930, 250, 240, 60, GREY, "POP", BLACK)
    pop_value = Button(930, 400, 240, 60, GREY, "POP value", BLACK)
    top = Button(930, 550, 240, 60, GREY, "TOP", BLACK)

    push_value_ev = InputForm(930, 460, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    pop_ret = Button(930, 610, 240, 60, GREY, "returned value", BLACK)
    pop_value_ev = InputForm(930, 160, 240, 60, GREY, BLACK, 3, False, "Enter int value")
    top_ret = Button(930, 310, 240, 60, GREY, "returned value", BLACK)

    button_and_pair = {push: push_value_ev, pop: pop_ret, pop_value: pop_value_ev, top: top_ret}

    text_box_message = ""

    stack_structure = Stack(430, 220, 400, 420)

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

                pop_ret.text = "returned value"
                top_ret.text = "returned value"

                for button in settings_buttons:
                    if button.is_over(pos):

                        if button.text == "help":
                            path = os.path.abspath('stack_folder/stack_help.pdf')
                            os.startfile(path)
                            button.active = False

                for button, pair in button_and_pair.items():
                    if button.is_over(pos):
                        print(button.text)
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

        draw(win, settings_buttons, button_and_pair, text_box_message, stack_structure)
