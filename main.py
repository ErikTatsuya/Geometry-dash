import pygame
from scene_manager import SceneManager
from scenes.main_menu import MainMenuScene
from settings import *

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

manager = SceneManager()
manager.set_scene(MainMenuScene(manager))

running = True
while running:
    events = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        events.append(event)

    manager.handle_events(events)
    manager.update()

    screen.fill((0, 0, 0))
    manager.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()