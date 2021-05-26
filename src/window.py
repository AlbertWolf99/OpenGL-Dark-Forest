#!/usr/bin/env python
# coding: utf-8

# In[12]:


import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np


# In[14]:


def initWindow(name, coord, key_event, mouse_event, width = 500, height = 500):
    '''
    Create a window with the given parameters
    Parameters
    ----------
        name : str
            Name of window.
        coord : list((float, float))
            List of coordinates (x, y) used to draw on window.
            0 < x,y < 1
        width : int
            Width of window. Default value = 500.
        height : int
            Height of window. Default value = 500.
    Return
    ------
        window
            window that was just initialized
        loc_color
            color variable localization
    '''
    
    glfw.init()
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE);
    window = glfw.create_window(width, height, name, None, None)
    glfw.make_context_current(window)
    
    glfw.set_key_callback(window,key_event)
    glfw.set_mouse_button_callback(window,mouse_event)

    vertex_code = """
        attribute vec2 position;
        uniform mat4 mat_transformation;
        void main(){
            gl_Position = mat_transformation * vec4(position,0.0,1.0);
        }
        """
    
    fragment_code = """
            uniform vec4 color;
            void main(){
                gl_FragColor = color;
            }
            """
    
    # Request a program and shader slots from GPU
    program  = glCreateProgram()
    vertex   = glCreateShader(GL_VERTEX_SHADER)
    fragment = glCreateShader(GL_FRAGMENT_SHADER)
    
    # Set shaders source
    glShaderSource(vertex, vertex_code)
    glShaderSource(fragment, fragment_code)
    
    # Compile shaders
    glCompileShader(vertex)
    if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(vertex).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Vertex Shader")
    
    glCompileShader(fragment)
    if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(fragment).decode()
        print(error)
        raise RuntimeError("Erro de compilacao do Fragment Shader")
    
    # Attach shader objects to the program
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    
    # Build program
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        print(glGetProgramInfoLog(program))
        raise RuntimeError('Linking error')

    # Make program the default program
    glUseProgram(program)
    
    # n vertices using 2 coordinates (x, y)
    n = len(coord)
    vertices = np.zeros(n, [("position", np.float32, 2)])
    for x in range (n):
        vertices['position'][x] = coord[x]
        
    # Request a buffer slot from GPU
    buffer = glGenBuffers(1)
    # Make this buffer the default one
    glBindBuffer(GL_ARRAY_BUFFER, buffer)

    # Upload data
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, buffer)
    
    # Bind the position attribute
    # --------------------------------------
    stride = vertices.strides[0]
    offset = ctypes.c_void_p(0)
    
    loc = glGetAttribLocation(program, "position")
    glEnableVertexAttribArray(loc)
    
    glVertexAttribPointer(loc, 2, GL_FLOAT, False, stride, offset)
    
    loc_color = glGetUniformLocation(program, "color")
    
    glfw.show_window(window)
    
    return window, program, loc_color

