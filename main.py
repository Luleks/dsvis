import pygame
from main_menu import main_menu
from linked_list import linked_list
from stack import stack

pygame.init()

WIDTH, HEIGHT = 1200, 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DataStructures visualiser")

game_run = True
main_menu_run = False
linked_list_run = False
stack_run = True
while game_run:
    if main_menu_run:
        running = main_menu(WINDOW, WIDTH, HEIGHT)
        if running == "quit":
            game_run = False
        elif running == "Linked List":
            main_menu_run = False
            linked_list_run = True
        elif running == "Stack":
            main_menu_run = False
            stack_run = True
        else:
            print(running)

    elif linked_list_run:
        running = linked_list(WINDOW)
        if running == "quit":
            game_run = False
        elif running == "main_menu":
            linked_list_run = False
            main_menu_run = True

    elif stack_run:
        running = stack(WINDOW)
        if running == "quit":
            game_run = False
        elif running == "main_menu":
            stack_run = False
            main_menu_run = True
