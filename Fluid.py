import numpy as np
import math
import pygame
# import colorsys
from variables import *




def IX(x,y):
    return x + y * N

class Fluid:
    global obstacle

    def __init__(self, dt, diffusion, viscosity):

        self.size = N
        self.dt = dt
        self.diff = diffusion
        self.visc = viscosity

        self.s = np.zeros(N*N)
        self.density = np.zeros(N*N)
        # density of color in water

        self.Vx = np.zeros(N*N)
        self.Vy = np.zeros(N*N)

        self.Vx0 = np.zeros(N*N)
        self.Vy0 = np.zeros(N*N)

    
    def addDensity(self, x, y, amount):
        self.density[IX(x,y)] += amount
    
    def addVelocity(self, x, y, amountX, amountY):
        self.Vx[IX(x,y)] += amountX
        self.Vy[IX(x,y)] += amountY

#  Function of dealing with situation with boundary cells.
#  - b : int
#  - x : float[]
  
    def set_bnd(self, b, x):
        # every velocity in the layer next to this outer layer is mirrored
        # wall gets negative velocity of that of the fluid to counter it
        for i in range(1, N-1):
            x[IX(i,0)] = -x[IX(i,1)] if b==2 else x[IX(i,1)]
            x[IX(i,N-1)] = -x[IX(i,N-2)] if b==2 else x[IX(i,N-2)]

        for j in range(1, N-1): 
            x[IX(0,j)] = -x[IX(1,j)] if b==1 else x[IX(1,j)]
            x[IX(N-1,j)] = -x[IX(N-2,j)] if b==1 else x[IX(N-2,j)]

        x[IX(0,0)] = 0.5 * (x[IX(1,0)] + x[IX(0,1)])
        x[IX(0,N-1)] = 0.5 * (x[IX(1,N-1)] + x[IX(0,N-2)])
        x[IX(N-1,0)] = 0.5 * (x[IX(N-2,1)] + x[IX(N-1,1)])
        x[IX(N-1,N-1)] = 0.5 * (x[IX(N-2,N-1)] + x[IX(N-1,N-2)])

    def lin_solve(self, b, x, x0, a, c):
        # solves linear differential equation, but how??
        cRecip = 1.0 / c
        for k in range(iter):
            for j in range(1, N-1):
                for i in range(1, N-1):
                    x[IX(i,j)] = x0[IX(i,j)] + a * (x[IX(i+1,j)] + x[IX(i-1,j)] + x[IX(i,j+1)] + x[IX(i,j-1)]) * cRecip
        self.set_bnd(b, x)
        # self.obs_collision(b, x, obstacle, obs_width, obs_length)

    def project(self, velocX, velocY, p, div): # makes divergence of each cell = 0
        for j in range(1, N-1):
            for i in range(1, N-1):
                div[IX(i,j)] = -0.5*(velocX[IX(i+1,j)]-velocX[IX(i-1,j)]+velocY[IX(i,j+1)]-velocY[IX(i,j-1)])/N
                p[IX(i,j)] = 0

        self.set_bnd(0, div) 
        self.set_bnd(0, p)

        # self.obs_collision(0, div, obstacle, obs_width, obs_length)
        # self.obs_collision(0, p, obstacle, obs_width, obs_length)

        self.lin_solve(0, p, div, 1, 6)

        for j in range(1, N-1):
            for i in range(1, N-1):
                velocX[IX(i,j)] -= 0.5 * (p[IX(i+1,j)] - p[IX(i-1,j)]) * N
                velocY[IX(i,j)] -= 0.5 * (p[IX(i,j+1)] - p[IX(i,j-1)]) * N

        self.set_bnd(1, velocX)
        self.set_bnd(2, velocY)
        # self.obs_collision(1, velocX, obstacle, obs_width, obs_length)
        # self.obs_collision(2, velocY, obstacle, obs_width, obs_length)

    def diffuse(self,b, x, x0, diff, dt):
        a = dt * diff * (N - 2) * (N - 2)
        self.lin_solve(b, x, x0, a, 1 + 6 * a)

    def advect(self, b, d, d0, velocX, velocY, dt, obstacle):
        # each cell's velocity that makes everything move
        # applies both to the dye and to the velocities
        dtx = dt * (N - 2)
        dty = dt * (N - 2)

        Nfloat = N - 2
        jfloat = 1
        for j in range(1, N-1):
            ifloat = 1
            for i in range(1, N-1):
                tmp1 = dtx * velocX[IX(i,j)]
                tmp2 = dty * velocY[IX(i,j)]
                x = ifloat - tmp1
                y = jfloat - tmp2

                if (x < 0.5): x = 0.5
                if (x > Nfloat + 0.5): x = Nfloat + 0.5
                i0 = math.floor(x)
                i1 = i0 + 1.0
                if (y < 0.5): y = 0.5
                if (y > Nfloat + 0.5): y = Nfloat + 0.5
                j0 = math.floor(y)
                j1 = j0 + 1.0

                s1 = x - i0
                s0 = 1.0 - s1
                t1 = y - j0
                t0 = 1.0 - t1

                i0i = int(i0)
                i1i = int(i1)
                j0i = int(j0)
                j1i = int(j1)

                d[IX(i,j)] = s0 * (t0 * d0[IX(i0i,j0i)]) + t1 * d0[IX(i0i,j1i)] + s1 * (t0 * d0[IX(i1i,j0i)] + t1 * d0[IX(i1i,j1i)])

                ifloat += 1

            jfloat += 1

        self.set_bnd(b, d)
        # self.obs_collision(b, d, obstacle, obs_width, obs_length)


    def step(self):
        # N = self.size
        visc = self.visc
        diff = self.diff
        dt = self.dt
        Vx = self.Vx
        Vy = self.Vy
        Vx0 = self.Vx0
        Vy0 = self.Vy0
        s = self.s
        density = self.density
        
        self.diffuse(1, Vx0, Vx, visc, dt)
        self.diffuse(2, Vy0, Vy, visc, dt)

        self.project(Vx0, Vy0, Vx, Vy)

        self.advect(1, Vx, Vx0, Vx0, Vy0, dt, obstacle)
        self.advect(2, Vy, Vy0, Vx0, Vy0, dt, obstacle)

        self.project(Vx, Vy, Vx0, Vy0)
        self.diffuse(0, s, density, diff, dt)
        self.advect(0, density, s, Vx, Vy, dt, obstacle)

    def renderD(self, WIN):
        for i in range(N):
            for j in range(N):
                x = i * SCALE
                y = j * SCALE
                d = self.density[IX(i,j)]
                # color = pygame.Color.hsv(((d + 50) % 255)/255,200/255,d/255)
                # color = colorsys.hsv_to_rgb(((d + 50) % 255)/255 * 100,200/255 * 100,d/255 * 100)
                color_ = (d%255, d%255, d%255)
                pygame.draw.rect(WIN, color_,[x, y, SCALE, SCALE],0)
                # pygame.draw.rect(WIN, (255,255,255),[x, y, SCALE, SCALE],0)
                # pygame.display.update()

    def renderV(self, WIN):
        for i in range(N):
            for j in range(N):
                x = i * SCALE
                y = j * SCALE
                vx = self.Vx[IX(i,j)]
                vy = self.Vy[IX(i,j)]
                if not (abs(vx) < 0.1 and abs(vy) <= 0.1):
                    pygame.draw.line(WIN, (255,255,255),(x, y), (x + vx * SCALE, y + vy * SCALE))
                    # pygame.display.update()

    def constrain(self, val, min_val, max_val):
        if val < min_val:
            return min_val
        elif val > max_val:
            return max_val
        else:
            return val
                
    def fadeD(self):
        for i in range(N):
            for j in range(N):
                d = self.density[IX(i,j)]
                self.density[IX(i,j)] = self.constrain(d-0.02, 0, 255)
    
    def obs_collision(self, b, x, obs, obs_width, obs_length): # obs is a pygame object 
        for i in range(obs.x , obs.x + obs_width):
            x[IX(i,obs.y)] = -x[IX(i,obs.y-1)] if b==2 else x[IX(i,obs.y-1)]
            x[IX(i,obs.y + obs_length)] = -x[IX(i,obs.y + obs_length + 1)] if b==2 else x[IX(i,obs.y + obs_length + 1)]

        for j in range(obs.y, obs.y + obs_length): 
            x[IX(obs.x,j)] = -x[IX(obs.x-1,j)] if b==1 else x[IX(obs.x-1,j)]
            x[IX(obs.x + obs_width,j)] = -x[IX(obs.x + obs_width + 1,j)] if b==1 else x[IX(obs.x + obs_width + 1,j)]

        x[IX(obs.x,obs.y)] = 0.5 * (x[IX(obs.x-1,obs.y)] + x[IX(obs.x,obs.y+1)])
        x[IX(obs.x,obs.y + obs_length)] = 0.5 * (x[IX(obs.x-1,obs.y + obs_length)] + x[IX(obs.x, obs.y + obs_length + 1)])
        x[IX(obs.x + obs_width,obs.y)] = 0.5 * (x[IX(obs.x + obs_width, obs.y - 1)] + x[IX(obs.x + obs_width + 1, obs.y)])
        x[IX(obs.x + obs_width, obs.y + obs_length)] = 0.5 * (x[IX(obs.x + obs_width + 1, obs.y + obs_length)] + x[IX(obs.x + obs_width, obs.y + obs_length + 1)])        
