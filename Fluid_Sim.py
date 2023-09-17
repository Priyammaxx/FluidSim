# handles only square grid sizes
# for incompressible fluids : density of fluid is constant

import pygame
import random
import noise

from Fluid import *
from variables import *

fluid = Fluid(DT, DIFFUSION, VISCOSITY)

def draw_window(OBSTACLE):
    global T

    WIN.fill(BLUE)

    cx = int((0.5*WIDTH) / SCALE)
    cy = int((0.5*HEIGHT) / SCALE)

    for i in range(-1,2):
        for j in range(-1,2):
            fluid.addDensity(cx + i, cy + j, random.randint(50,150))

    for i in range(2):
        angle = noise.pnoise1(T) * 3.1416 * 2
        vx = math.cos(angle)
        vy = math.sin(angle)
        T += 0.01
        fluid.addVelocity(cx, cy, vx * 0.2, vy * 0.2)

    fluid.step()
    fluid.renderD(WIN) # figure out the correct order
    # fluid.renderV(WIN) # why
    fluid.fadeD() # necessary to call all these functions?
    pygame.draw.rect(WIN, BLUE, [OBSTACLE.x, OBSTACLE.y, obs_width, obs_length], 0) # draw obstacle rectangle
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(obstacle)
    pygame.quit()
    
if __name__ == "__main__":
    main()