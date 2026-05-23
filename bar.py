import math
import config
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import keyboard

unit_scale = 0.1
screen_size = config.screen_size
move_factor = 500

class Bar:
    def __init__(self, initposx, lenx, leny, color={'R':0.0,'G':0.0,'B':0.0,'A':100.0}, inputup='w', inputdown='s'):

        self.position = [initposx, screen_size[1]//2]
        self.velocity = [0, 0]

        self.true_center = [self.position[0] + lenx, self.position[1] + leny//2]

        self.lengthx = lenx
        self.lengthy = leny
        self.color = color
        self.radius = 10

        self.inputup = inputup
        self.inputdown = inputdown

    def Move(self):
        if keyboard.is_pressed(self.inputup):
            #print(self.position[1])
            if self.position[1] + self.lengthy < screen_size[1]:
                self.position[1] += move_factor * config.delta_time
        if keyboard.is_pressed(self.inputdown):
            if self.position[1] > 0:
                self.position[1] -= move_factor * config.delta_time

        self.true_center = [self.position[0] + self.lengthx, self.position[1] + self.lengthy//2]

    def BotMove(self,pt):
        if self.true_center[1] < pt[1]:
            self.position[1] += move_factor * config.delta_time
        elif self.true_center[1] > pt[1]:
            self.position[1] -= move_factor * config.delta_time

    def Draw(self):
        GL.glColor3f(self.color['R'], self.color['G'], self.color['B'])
        GL.glBegin(GL.GL_QUADS)
        x, y = self.position
        w, h = self.lengthx, self.lengthy
        GL.glVertex2f(x, y)
        GL.glVertex2f(x + w, y)
        GL.glVertex2f(x + w, y + h)
        GL.glVertex2f(x, y + h)
        GL.glEnd()

        #debug
        '''
        GL.glColor3f(self.color['R'], 255, self.color['B'])
        GL.glBegin(GL.GL_QUADS)
        x, y = self.position
        w, h = 2, 2
        GL.glVertex2f(x, y)
        GL.glVertex2f(x + w, y)
        GL.glVertex2f(x + w, y + h)
        GL.glVertex2f(x, y + h)
        GL.glEnd()

        GL.glColor3f(self.color['R'], 255, 255)
        GL.glBegin(GL.GL_QUADS)
        x, y = self.true_center
        w, h = 2, 2
        GL.glVertex2f(x, y)
        GL.glVertex2f(x + w, y)
        GL.glVertex2f(x + w, y + h)
        GL.glVertex2f(x, y + h)
        GL.glEnd()
        '''