"""
Activity 5: Hardware-Accelerated 3D Pipeline using PyOpenGL
"""

import sys
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# 1. MESH DEFINITION DATA
vertices = [
    ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
    ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
]

colors = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
    (1, 0, 1), (0, 1, 1), (1, 1, 1), (0.5, 0.5, 0.5)
]

surfaces = [
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
]

edges = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]


def draw_colored_cube():
    """Renders a solid cube using colored quads with per-vertex color interpolation."""
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex_idx in surface:
            glColor3fv(colors[vertex_idx])
            glVertex3fv(vertices[vertex_idx])
    glEnd()

    # Optional outline wireframe overlay for visual clarity
    glColor3f(0, 0, 0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_transparent_pyramid():
    """Renders a semi-transparent pyramid demonstrating alpha blending."""
    glBegin(GL_TRIANGLES)
    # Front Face (Red, 50% Alpha)
    glColor4f(1.0, 0.0, 0.0, 0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)

    # Right Face (Green, 50% Alpha)
    glColor4f(0.0, 1.0, 0.0, 0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)

    # Back Face (Blue, 50% Alpha)
    glColor4f(0.0, 0.0, 1.0, 0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)

    # Left Face (Yellow, 50% Alpha)
    glColor4f(1.0, 1.0, 0.0, 0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Activity 5: Hardware-Accelerated 3D Pipeline (PyOpenGL)')
    clock = pygame.time.Clock()

    # 2. OPENGL PIPELINE STATE INITIALIZATION
    # Set background color (dark blue-gray)
    glClearColor(0.08, 0.10, 0.14, 1.0)

    # Perspective Projection Matrix Setup
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, (display[0] / display[1]), 0.1, 50.0)

    # Modelview Matrix Setup
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Enable Depth Testing (Z-Buffering) for Hidden Surface Removal
    depth_test_enabled = True
    glEnable(GL_DEPTH_TEST)

    # Enable Alpha Blending for Transparency
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Scene rotation angles
    rot_x, rot_y = 0.0, 0.0

    running = True
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_z:
                    # Toggle Z-Buffering to observe hidden surface removal behavior
                    depth_test_enabled = not depth_test_enabled
                    if depth_test_enabled:
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)

        # Interactive Rotation Controls
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rot_y -= 1.5
        if keys[K_RIGHT]:
            rot_y += 1.5
        if keys[K_UP]:
            rot_x -= 1.5
        if keys[K_DOWN]:
            rot_x += 1.5

        # 3. RENDER FRAME
        # Clear Color Buffer and Depth Buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Reset Modelview Matrix
        glLoadIdentity()

        # Camera positioning (Move back along Z-axis)
        glTranslatef(0.0, 0.0, -7.0)

        # Global Scene Rotation
        glRotatef(rot_x, 1, 0, 0)
        glRotatef(rot_y, 0, 1, 0)

        # --- Object 1: Primary Opaque Cube ---
        glPushMatrix()  # Push local transform matrix
        glTranslatef(-1.5, 0.0, 0.0)
        glRotatef(pygame.time.get_ticks() * 0.05, 0, 1, 0)
        draw_colored_cube()
        glPopMatrix()   # Pop matrix back to global state

        # --- Object 2: Transparent Pyramid (Hierarchical Transform) ---
        glPushMatrix()  # Push local transform matrix
        glTranslatef(1.5, 0.0, 0.0)
        glRotatef(pygame.time.get_ticks() * 0.08, 1, 1, 0)
        draw_transparent_pyramid()
        glPopMatrix()   # Pop matrix back to global state

        # Swap Double Buffer
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()