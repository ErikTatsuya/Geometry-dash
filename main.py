import pygame
from settings import *
from scene_manager import SceneManager
from scenes.main_menu import MainMenuScene

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Dash Clone")

clock = pygame.time.Clock()

manager = SceneManager()
manager.set_scene(MainMenuScene(manager))

running = True
while running:

    clock.tick(FPS)

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # INPUT
    manager.handle_events(events)

    # UPDATE
    manager.update()

    # DRAW
    manager.draw(screen)

    pygame.display.flip()

pygame.quit()