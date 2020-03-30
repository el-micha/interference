import random
import pygame
from grid import World
from entity import Entity



pygame.init()

screen = pygame.display.set_mode((1920,1080))
pygame.display.set_caption("gaylord")

world = World(64, 64+32)
character = Entity()

clock = pygame.time.Clock()
stop = False
while not stop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stop = True
        print(event)
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:
        character.move(0, -4)
    if pressed[pygame.K_DOWN]:
        character.move(0, 4)
    if pressed[pygame.K_LEFT]:
        character.move(-4, 0)
    if pressed[pygame.K_RIGHT]:
        character.move(4, 0)

    screen.fill((0, 0, 0))
    #pygame.draw.rect(screen, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), pygame.Rect(random.randint(0,1920), random.randint(0,1080), random.randint(2,1000), random.randint(2,1000)))
    world.draw(screen)
    character.draw(screen)

    pygame.display.update()
    clock.tick(60)
