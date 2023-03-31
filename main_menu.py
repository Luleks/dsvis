import pygame
import pygame.display
from button import Button

BACKGROUND_IMAGE = pygame.image.load("main_menu_folder/main_menu_background.jpg")
TITLE_FONT = pygame.font.SysFont("erasict", 50)
OPTION_FONT = pygame.font.SysFont("erasict", 50)

GREY = (128, 128, 128)
BLACK = (0, 0, 0)


def draw(win, buttons):
    win.blit(BACKGROUND_IMAGE, (0, 0))

    title = TITLE_FONT.render("DATA STRUCTURES VISUALISER 1.1", True, pygame.Color("White"))
    win.blit(title, ((win.get_width() - title.get_width()) // 2, (100 - title.get_height()) // 2))

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def main_menu(window, width, height):
    available_ds = ["Array", "Linked List", "Stack", "Queue", "Hash", "Tree", "Graph"]

    gap_width = width // 17
    button_width = 3 * gap_width
    button_height = button_width
    gap_height = (height - 100 - 2 * button_height) // 3

    buttons = []
    for i, ds in enumerate(available_ds):
        b = Button(gap_width + (button_width + gap_width) * (i % 4), 100 + gap_height + (button_height + gap_height) * (i // 4),
                   button_width, button_height, GREY, available_ds[i], BLACK, False, OPTION_FONT)
        buttons.append(b)

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_over(pos):
                        return button.text

        pos = pygame.mouse.get_pos()
        for button in buttons:
            button.shift_color(pos)

        draw(window, buttons)
