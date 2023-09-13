import pygame
import random

from Fluid import *


DENSITY = 0.2
DIFFUSION = 0
VISCOSITY = 0

WIDTH, HEIGHT = 512, 512

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FluidSim")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE = (173, 216, 230)

FPS = 24


fluid = Fluid(DENSITY, DIFFUSION, VISCOSITY)

def draw_window():
    WIN.fill(BLUE)

    cx = int((0.5*WIDTH) / SCALE)
    cy = int((0.5*HEIGHT) / SCALE)

    for i in range(-1,2):
        for j in range(-1,2):
            fluid.addDensity(cx + i, cy + j, random.randint(50,150))

    for i in range(2):
        v = pygame.math.Vector2(random.random() * math.pi * 2)
        fluid.addVelocity(cx, cy, v.x * 0.2, v.y * 0.2)

    fluid.step()
    fluid.renderD(WIN) # figure out the correct order
    # fluid.renderV(WIN) # why
    # fluid.fadeD() # necessary to call all these functions?
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window()
    pygame.quit()
    
if __name__ == "__main__":
    main()