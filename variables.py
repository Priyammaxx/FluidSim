import pygame


FPS = 24

T = 0


N = 100
iter = 16
SCALE = 4
t = 0


DT = 0.2
DIFFUSION = 0
# VISCOSITY = 0.0000001
VISCOSITY = 0


# WIDTH, HEIGHT = 512, 512
WIDTH, HEIGHT = 400, 400

obs_size = 50
obs_width = int(obs_size * SCALE * N / WIDTH)
obs_length = int(obs_size * SCALE * N / HEIGHT)
obstacle = pygame.Rect(99, 99, obs_width, obs_length)


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FluidSim")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
BLUE = (173, 216, 230)

