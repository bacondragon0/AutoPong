import math
import config
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import random

from ball import Ball
from ball import Force
from bar import Bar

# Variables
screen_size = config.screen_size
dt = config.delta_time

ball = Ball(250, 250, 10, 64, {'R':255.0,'G':0.0,'B':0.0,'A':100.0})

ball.InitConditions([screen_size[0] // 2, screen_size[1] // 2], [random.choice([-300,300]), random.randint(-50,50)])

bar1 = Bar(screen_size[0] * 1/10,10,60,{'R':255.0,'G':0.0,'B':0.0,'A':100.0})
bar2 = Bar(screen_size[0] * 9/10,10,60,{'R':255.0,'G':0.0,'B':0.0,'A':100.0},'q','e')


objects = [ball,bar1,bar2]

def display():
    GL.glClear(GL.GL_COLOR_BUFFER_BIT)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    # Draw Primitives
    for obj in objects:
        obj.Draw()

    GL.glFlush()

def update(value):

    Force.BarCollision(ball, [bar1,bar2])
    Force.Kinetic(objects, dt)
    Force.WallBounce(objects)

    interpt = ball.CalculateInterceptPt([bar1.position,bar2.position])
    #ball.DrawInterceptPt(interpt)

    bar1.Move()
    bar2.Move()
    
    if ball.velocity[0] < 0:
        bar1.BotMove(interpt)
    else:
        bar2.BotMove(interpt)

    # Advance Frame
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(16, update, 0)  # 60 FPS

def reshape(width, height):
    screen_size[0], screen_size[1] = width, height
    GL.glViewport(0, 0, width, height)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GL.glOrtho(0, width, 0, height, -1, 1)

def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_SINGLE | GLUT.GLUT_RGB)
    GLUT.glutInitWindowSize(screen_size[0], screen_size[1])
    GLUT.glutCreateWindow(b"AutoPong")
    GL.glClearColor(0.0, 0.0, 0.0, 1.0)
    GLUT.glutDisplayFunc(display)
    GLUT.glutReshapeFunc(reshape)
    GLUT.glutTimerFunc(0, update, 0)
    GLUT.glutMainLoop()

main()