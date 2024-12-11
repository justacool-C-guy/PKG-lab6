import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class Face:
    def __init__(self, vertices, color=(0.7, 0.7, 0.7)):
        self.vertices = vertices
        self.color = color

def draw_axes(size=5.0):
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(size, 0.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, size, 0.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, size)
    glEnd()
    glLineWidth(1.0)

    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(-5, i, 0)
        glVertex3f(5, i, 0)
        glVertex3f(i, -5, 0)
        glVertex3f(i, 5, 0)
    glEnd()

    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(-5, 0, i)
        glVertex3f(5, 0, i)
        glVertex3f(i, 0, -5)
        glVertex3f(i, 0, 5)
    glEnd()

    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_LINES)
    for i in range(-5, 6):
        glVertex3f(0, -5, i)
        glVertex3f(0, 5, i)
        glVertex3f(0, i, -5)
        glVertex3f(0, i, 5)
    glEnd()

class Object3D:
    def __init__(self):
        # Vertical bar vertices
        self.vertices = [
            # Left vertical bar - front
            Point3D(-1.0, -1.0, 0.2),  # 0
            Point3D(-0.7, -1.0, 0.2),  # 1
            Point3D(-0.7, 1.0, 0.2),  # 2
            Point3D(-1.0, 1.0, 0.2),  # 3
            # Left vertical bar - back
            Point3D(-1.0, -1.0, -0.2),  # 4
            Point3D(-0.7, -1.0, -0.2),  # 5
            Point3D(-0.7, 1.0, -0.2),  # 6
            Point3D(-1.0, 1.0, -0.2),  # 7

            # Connecting bar - front
            Point3D(-0.7, -0.2, 0.2),  # 8
            Point3D(-0.3, -0.2, 0.2),  # 9
            Point3D(-0.3, 0.2, 0.2),  # 10
            Point3D(-0.7, 0.2, 0.2),  # 11
            # Connecting bar - back
            Point3D(-0.7, -0.2, -0.2),  # 12
            Point3D(-0.3, -0.2, -0.2),  # 13
            Point3D(-0.3, 0.2, -0.2),  # 14
            Point3D(-0.7, 0.2, -0.2),  # 15
        ]

        # Add circular part vertices
        radius_outer = 1
        radius_inner = 0.7
        center_x = 0.65
        segments = 32

        # Внешний круг - передняя часть
        for i in range(segments):
            angle = 2 * np.pi * i / segments
            # Внешняя окружность - перед
            self.vertices.append(Point3D(
                center_x + radius_outer * np.cos(angle),
                radius_outer * np.sin(angle),
                0.2
            ))
            # Внешняя окружность - зад
            self.vertices.append(Point3D(
                center_x + radius_outer * np.cos(angle),
                radius_outer * np.sin(angle),
                -0.2
            ))
            # Внутренняя окружность - перед
            self.vertices.append(Point3D(
                center_x + radius_inner * np.cos(angle),
                radius_inner * np.sin(angle),
                0.2
            ))
            # Внутренняя окружность - зад
            self.vertices.append(Point3D(
                center_x + radius_inner * np.cos(angle),
                radius_inner * np.sin(angle),
                -0.2
            ))

        # Define faces
        self.faces = []

        # Left vertical bar faces
        self.faces.extend([
            Face([0, 1, 2, 3], (0.8, 0.2, 0.2)),  # Front
            Face([4, 5, 6, 7], (0.8, 0.2, 0.2)),  # Back
            Face([0, 3, 7, 4], (0.7, 0.2, 0.2)),  # Left
            Face([1, 2, 6, 5], (0.7, 0.2, 0.2)),  # Right
            Face([2, 3, 7, 6], (0.7, 0.2, 0.2)),  # Top
            Face([0, 1, 5, 4], (0.7, 0.2, 0.2))  # Bottom
        ])

        # Connecting bar faces
        self.faces.extend([
            Face([8, 9, 10, 11], (0.2, 0.8, 0.2)),  # Front
            Face([12, 13, 14, 15], (0.2, 0.8, 0.2)),  # Back
            Face([8, 11, 15, 12], (0.2, 0.7, 0.2)),  # Left
            Face([9, 10, 14, 13], (0.2, 0.7, 0.2)),  # Right
            Face([10, 11, 15, 14], (0.2, 0.7, 0.2)),  # Top
            Face([8, 9, 13, 12], (0.2, 0.7, 0.2))  # Bottom
        ])

        # Circular part faces
        for i in range(segments):
            base_idx = 16 + i * 4
            next_base_idx = 16 + ((i + 1) % segments) * 4

            # Indices for current segment
            curr_outer_front = base_idx
            curr_outer_back = base_idx + 1
            curr_inner_front = base_idx + 2
            curr_inner_back = base_idx + 3

            # Indices for next segment
            next_outer_front = next_base_idx
            next_outer_back = next_base_idx + 1
            next_inner_front = next_base_idx + 2
            next_inner_back = next_base_idx + 3

            # Front face (outer to inner)
            self.faces.append(Face(
                [curr_outer_front, next_outer_front, next_inner_front, curr_inner_front],
                (0.2, 0.2, 0.8)
            ))

            # Back face (outer to inner)
            self.faces.append(Face(
                [curr_outer_back, next_outer_back, next_inner_back, curr_inner_back],
                (0.2, 0.2, 0.8)
            ))

            # Outer face
            self.faces.append(Face(
                [curr_outer_front, next_outer_front, next_outer_back, curr_outer_back],
                (0.3, 0.3, 0.9)
            ))

            # Inner face
            self.faces.append(Face(
                [curr_inner_front, next_inner_front, next_inner_back, curr_inner_back],
                (0.3, 0.3, 0.9)
            ))

        self.reset_transform()

    def reset_transform(self):
        self.transform_matrix = np.eye(4)

    def get_rotation_matrix(self, axis, angle):
        angle = np.radians(angle)
        c, s = np.cos(angle), np.sin(angle)
        if axis == 0:
            return np.array([
                [1, 0, 0, 0],
                [0, c, -s, 0],
                [0, s, c, 0],
                [0, 0, 0, 1]
            ])
        elif axis == 1:
            return np.array([
                [c, 0, s, 0],
                [0, 1, 0, 0],
                [-s, 0, c, 0],
                [0, 0, 0, 1]
            ])
        else:
            return np.array([
                [c, -s, 0, 0],
                [s, c, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

    def get_translation_matrix(self, dx, dy, dz):
        return np.array([
            [1, 0, 0, dx],
            [0, 1, 0, dy],
            [0, 0, 1, dz],
            [0, 0, 0, 1]
        ])

    def get_scale_matrix(self, sx, sy, sz):
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def apply_translation(self, dx, dy, dz):
        translation = self.get_translation_matrix(dx, dy, dz)
        self.transform_matrix = translation @ self.transform_matrix

    def apply_rotation(self, axis, angle):
        rotation = self.get_rotation_matrix(axis, angle)
        self.transform_matrix = rotation @ self.transform_matrix

    def apply_scale(self, scale_factor):
        scale = self.get_scale_matrix(scale_factor, scale_factor, scale_factor)
        self.transform_matrix = scale @ self.transform_matrix

    def draw(self):
        glPushMatrix()
        glMultMatrixf(self.transform_matrix.T)

        glEnable(GL_POLYGON_OFFSET_FILL)
        glPolygonOffset(1.0, 1.0)

        for face in self.faces:
            glBegin(GL_QUADS)
            glColor3f(*face.color)
            for vertex_idx in face.vertices:
                vertex = self.vertices[vertex_idx]
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()

        glDisable(GL_POLYGON_OFFSET_FILL)

        glLineWidth(2.0)
        for face in self.faces:
            glBegin(GL_LINE_LOOP)
            glColor3f(0, 0, 0)
            for vertex_idx in face.vertices:
                vertex = self.vertices[vertex_idx]
                glVertex3f(vertex.x, vertex.y, vertex.z)
            glEnd()
        glLineWidth(1.0)

        glPopMatrix()

def setup_projection(width, height, ortho=False):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = width / height
    if ortho:
        if width > height:
            glOrtho(-5 * aspect, 5 * aspect, -5, 5, -50, 50)
        else:
            glOrtho(-5, 5, -5 / aspect, 5 / aspect, -50, 50)
    else:
        gluPerspective(45, aspect, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def setup_view(view_type='main'):
    glLoadIdentity()
    if view_type == 'main':
        glTranslatef(0, 0, -15)
        glRotatef(30, 1, 0, 0)
        glRotatef(45, 0, 1, 0)
    elif view_type == 'top':
        glTranslatef(0, 0, -15)
        glRotatef(90, 1, 0, 0)
    elif view_type == 'front':
        glTranslatef(0, 0, -15)
    elif view_type == 'side':
        glTranslatef(0, 0, -15)
        glRotatef(90, 0, 1, 0)

def main():
    pygame.init()
    display = (1600, 1000)
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL | pygame.HWSURFACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.15, 0.15, 0.15, 1)

    letter = Object3D()
    active_view = 'main'
    clock = pygame.time.Clock()

    help_text = [
        "Controls:",
        "Arrows - Move X/Y",
        "PgUp/PgDn - Move Z",
        "Q/E - Rotate X",
        "A/D - Rotate Y",
        "Z/C - Rotate Z",
        "+/- - Scale",
        "1,2,3 - Views",
        "ESC - Main view",
        "R - Reset transform",
        "H - Show this help",
        "M - Show matrix"
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    active_view = 'top'
                elif event.key == pygame.K_2:
                    active_view = 'front'
                elif event.key == pygame.K_3:
                    active_view = 'side'
                elif event.key == pygame.K_ESCAPE:
                    active_view = 'main'
                elif event.key == pygame.K_r:
                    letter.reset_transform()
                elif event.key == pygame.K_h:
                    print("\n=== HELP ===")
                    for line in help_text:
                        print(line)
                    print("============")
                elif event.key == pygame.K_m:
                    print("\n=== TRANSFORM MATRIX ===")
                    for row in letter.transform_matrix:
                        print(" ".join([f"{x:7.3f}" for x in row]))
                    print("=====================")

        keys = pygame.key.get_pressed()
        move_speed = 0.1
        rotate_speed = 2.0
        scale_speed = 0.1

        if keys[pygame.K_LEFT]: letter.apply_translation(-move_speed, 0, 0)
        if keys[pygame.K_RIGHT]: letter.apply_translation(move_speed, 0, 0)
        if keys[pygame.K_UP]: letter.apply_translation(0, move_speed, 0)
        if keys[pygame.K_DOWN]: letter.apply_translation(0, -move_speed, 0)
        if keys[pygame.K_PAGEUP]: letter.apply_translation(0, 0, move_speed)
        if keys[pygame.K_PAGEDOWN]: letter.apply_translation(0, 0, -move_speed)
        if keys[pygame.K_q]: letter.apply_rotation(0, rotate_speed)
        if keys[pygame.K_e]: letter.apply_rotation(0, -rotate_speed)
        if keys[pygame.K_a]: letter.apply_rotation(1, rotate_speed)
        if keys[pygame.K_d]: letter.apply_rotation(1, -rotate_speed)
        if keys[pygame.K_z]: letter.apply_rotation(2, rotate_speed)
        if keys[pygame.K_c]: letter.apply_rotation(2, -rotate_speed)
        if keys[pygame.K_KP_PLUS] or keys[pygame.K_PLUS]: letter.apply_scale(1 + scale_speed)
        if keys[pygame.K_KP_MINUS] or keys[pygame.K_MINUS]: letter.apply_scale(1 - scale_speed)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if active_view == 'main':
            setup_projection(800, 600)
            glViewport(400, 200, 800, 600)
            setup_view('main')
            draw_axes()
            letter.draw()

            size = 300
            views = [('top', 0), ('front', 1), ('side', 2)]
            for view, i in views:
                setup_projection(size, size, True)
                glViewport(size * i, 0, size, size)
                setup_view(view)
                draw_axes()
                letter.draw()
        else:
            setup_projection(display[0], display[1], True)
            glViewport(0, 0, display[0], display[1])
            setup_view(active_view)
            draw_axes()
            letter.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()