import math
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import config
import random

fBounce = 1
unit_scale = 0.1
screen_size = config.screen_size
delta = config.delta_time

class Ball:
    def __init__(self, centerX, centerY, radius, resolution=64, color={'R':0.0,'G':0.0,'B':0.0,'A':100.0}):

        self.position = [0, 0]
        self.velocity = [0, 0]

        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        self.resolution = resolution
        self.color = color

    def Draw(self):

        GL.glBegin(GL.GL_TRIANGLE_FAN)
        GL.glColor3f(self.color['R'], self.color['G'], self.color['B'])
        GL.glVertex2d(self.position[0], self.position[1])

        for i in range(self.resolution + 1):
            angle = 2.0 * math.pi * (i / self.resolution)
            x = self.position[0] + math.cos(angle) * self.radius
            y = self.position[1] + math.sin(angle) * self.radius

            GL.glVertex2d(x, y)

        GL.glEnd()

    def ApplyAcceleration(self, x, y):
        self.velocity[0] = self.velocity[0] + x
        self.velocity[1] = self.velocity[1] + y

    def ApplyDefaultForces(self):

        self.position[0] = self.position[0] + self.velocity[0]
        self.position[1] = self.position[1] + self.velocity[1]

        # Gravity Force
        # self.velocity[1] = self.velocity[1] -9.81 / 20

        fBounce = 0.95

        # Border Collision Force
        # X
        if self.position[0] - self.radius < 0:
            self.position[0] = self.radius
            self.velocity[0] = abs(self.velocity[0]) * fBounce
        elif self.position[0] + self.radius > screen_size[0]:
            self.position[0] = screen_size[0] - self.radius
            self.velocity[0] = -abs(self.velocity[0]) * fBounce

        # Y
        if self.position[1] - self.radius < 0:
            self.position[1] = self.radius
            self.velocity[1] = abs(self.velocity[1]) * fBounce
        elif self.position[1] + self.radius > screen_size[1]:
            self.position[1] = screen_size[1] - self.radius
            self.velocity[1] = -abs(self.velocity[1]) * fBounce

    def InitConditions(self, init_position, init_velocity):

        self.position = init_position
        self.velocity = init_velocity

    def DrawVector(self):
        x, y = self.position
        w, h = self.position[0] + self.velocity[0], self.position[1] + self.velocity[1]

        GL.glBegin(GL.GL_LINE_STRIP)
        GL.glColor3f(0, 255, 0)
        GL.glVertex2d(x,y)
        GL.glVertex2d(w,h)
        GL.glEnd()

    def DrawInterceptPt(self,pt):
        for i in range(64 + 1):
            angle = 2.0 * math.pi * (i / 64)
            a = pt[0] + math.cos(angle) * 2
            b = pt[1] + math.sin(angle) * 2

            GL.glVertex2d(a, b)

        GL.glEnd()

    def CalculateInterceptPt(self,bars):
        if self.velocity[0] < 0: barpos = bars[0]
        else: barpos = bars[1]

        x = barpos[0]
        y = self.position[1] + (self.velocity[1] / self.velocity[0]) * (barpos[0] - self.position[0])
        
        return (x,y)


class Force:
    def __init__(self):
        self.unit_scale = 1
        self.dist_scale = 1

    def Kinetic(objects,delta):
        for obj in objects:
            obj.position[0] = obj.position[0] + obj.velocity[0] * delta
            obj.position[1] = obj.position[1] + obj.velocity[1] * delta

    def WallBounce(objects):
        for obj in objects:
            if obj.position[0] - obj.radius < 0:
                obj.position[0] = obj.radius
                obj.velocity[0] = abs(obj.velocity[0]) * fBounce
            elif obj.position[0] + obj.radius > screen_size[0]:
                obj.position[0] = screen_size[0] - obj.radius
                obj.velocity[0] = -abs(obj.velocity[0]) * fBounce

        # Y
            if obj.position[1] - obj.radius < 0:
                obj.position[1] = obj.radius
                obj.velocity[1] = abs(obj.velocity[1]) * fBounce
            elif obj.position[1] + obj.radius > screen_size[1]:
                obj.position[1] = screen_size[1] - obj.radius
                obj.velocity[1] = -abs(obj.velocity[1]) * fBounce

    def BarCollision(ball,lbar):
        for obj in lbar:
            if abs(ball.position[0] - (obj.position[0] + obj.lengthx / 2)) <= ball.radius:
                if obj.position[1] <= ball.position[1] <= obj.position[1] + obj.lengthy:
                    ball.velocity[0] *= -1 * fBounce #* -math.cos(random.randint(-45,45) * math.pi)
                    #ball.velocity[1] *= -1 * fBounce