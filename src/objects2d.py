#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders


# In[1]:


def draw_points(first, count = 1):
    glDrawArrays(GL_POINTS, first, count)

def draw_lines(first, count = 2, strip = False, loop = False):
    if strip:
        glDrawArrays(GL_LINE_STRIP, first, count)
    elif loop:
        glDrawArrays(GL_LINE_LOOP, first, count)
    else:
        glDrawArrays(GL_LINES, first, count)

def draw_triangles(first, count = 3, strip = False):
    if strip:
        glDrawArrays(GL_TRIANGLE_STRIP, first, count)
    else:
        glDrawArrays(GL_TRIANGLES, first, count)

def draw_squares(first, count = 4):
    for x in range(0, count, 4):
        glDrawArrays(GL_TRIANGLE_STRIP, first+x, 4)

def draw_circles(first, count):
    glDrawArrays(GL_TRIANGLE_FAN, first, count)

