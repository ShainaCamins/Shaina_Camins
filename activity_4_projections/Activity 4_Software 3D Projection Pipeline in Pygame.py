"""
Activity 4: Software 3D Projection Pipeline in Pygame
"""

import math
import sys
import pygame

"""
1. MESH DATA DEFINITION
"""
cube_vertices = [
    [-100, -100, -100], [ 100, -100, -100], [ 100,  100, -100], [-100,  100, -100],
    [-100, -100,  100], [ 100, -100,  100], [ 100,  100,  100], [-100,  100,  100]
]

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]


"""
2. PROJECTION MATHEMATICAL FUNCTIONS
"""
def project_orthographic(x, y, z, offset_x=400, offset_y=300):
    """
    Orthographic Projection:
    Drops the Z-coordinate directly. Lines remain parallel.
    """
    xp = x
    yp = y
    return int(xp + offset_x), int(yp + offset_y)


def project_oblique(x, y, z, mode='cavalier', phi_deg=30, offset_x=400, offset_y=300):
    """
    Oblique Parallel Projection:
    xp = x + z * L1 * cos(phi)
    yp = y + z * L1 * sin(phi)
    - Cavalier: L1 = 1.0 (no depth foreshortening, DOP at 45 deg)
    - Cabinet:  L1 = 0.5 (50% depth foreshortening, DOP at 63.4 deg)
    """
    phi = math.radians(phi_deg)
    l1 = 1.0 if mode == 'cavalier' else 0.5
    xp = x + z * l1 * math.cos(phi)
    yp = y + z * l1 * math.sin(phi)
    return int(xp + offset_x), int(yp + offset_y)


def project_perspective(x, y, z, d=400, offset_x=400, offset_y=300):
    """
    Perspective Projection:
    xp = (x * D) / (z + D)
    yp = (y * D) / (z + D)
    Lines converge toward a vanishing point.
    """
    distance = z + d
    if distance == 0:
        distance = 0.001
    xp = (x * d) / distance
    yp = (y * d) / distance
    return int(xp + offset_x), int(yp + offset_y)


"""
3. 3D ROTATION TRANSFORMATIONS
"""
def rotate_x(x, y, z, angle_rad):
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a


def rotate_y(x, y, z, angle_rad):
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a


def rotate_z(x, y, z, angle_rad):
    cos_a, sin_a = math.cos(angle_rad), math.sin(angle_rad)
    return x * cos_a - y * sin_a, x * sin_a + y * cos_a, z


"""
4. MAIN PYGAME RENDERING LOOP
"""
def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Camins_Activity 4: 3D Projection Engine")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 18)
    title_font = pygame.font.SysFont("Arial", 22, bold=True)

    mode = "perspective"
    angle_x = math.radians(20)
    angle_y = math.radians(30)
    angle_z = 0.0

    center_x = screen_width // 2
    center_y = screen_height // 2

    running = True
    while running:
        clock.tick(60)
        screen.fill((20, 24, 33))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "orthographic"
                elif event.key == pygame.K_2:
                    mode = "cavalier"
                elif event.key == pygame.K_3:
                    mode = "cabinet"
                elif event.key == pygame.K_4:
                    mode = "perspective"
                elif event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle_y -= 0.03
        if keys[pygame.K_RIGHT]:
            angle_y += 0.03
        if keys[pygame.K_UP]:
            angle_x -= 0.03
        if keys[pygame.K_DOWN]:
            angle_x += 0.03
        if keys[pygame.K_a]:
            angle_z -= 0.03
        if keys[pygame.K_d]:
            angle_z += 0.03

        projected_points = []
        for v in cube_vertices:
            rx, ry, rz = rotate_x(v[0], v[1], v[2], angle_x)
            rx, ry, rz = rotate_y(rx, ry, rz, angle_y)
            rx, ry, rz = rotate_z(rx, ry, rz, angle_z)

            if mode == "orthographic":
                pt = project_orthographic(rx, ry, rz, center_x, center_y)
            elif mode == "cavalier":
                pt = project_oblique(rx, ry, rz, mode="cavalier", phi_deg=30, offset_x=center_x, offset_y=center_y)
            elif mode == "cabinet":
                pt = project_oblique(rx, ry, rz, mode="cabinet", phi_deg=30, offset_x=center_x, offset_y=center_y)
            elif mode == "perspective":
                pt = project_perspective(rx, ry, rz, d=400, offset_x=center_x, offset_y=center_y)

            projected_points.append(pt)

        for edge in cube_edges:
            p1 = projected_points[edge[0]]
            p2 = projected_points[edge[1]]
            pygame.draw.line(screen, (0, 225, 255), p1, p2, 2)

        for pt in projected_points:
            pygame.draw.circle(screen, (255, 100, 100), pt, 4)

        title_text = title_font.render(f"CURRENT PROJECTION: {mode.upper()}", True, (255, 255, 255))
        screen.blit(title_text, (20, 20))

        controls_lines = [
            "Keys [1-4]: Switch Projection Mode :3",
            "  1: Orthographic",
            "  2: Cavalier Oblique (L1 = 1.0)",
            "  3: Cabinet Oblique  (L1 = 0.5)",
            "  4: Perspective      (D = 400)",
            "Arrow Keys: Rotate X / Y Axis",
            "A / D Keys: Rotate Z Axis"
        ]

        y_offset = 60
        for line in controls_lines:
            txt = font.render(line, True, (180, 190, 200))
            screen.blit(txt, (20, y_offset))
            y_offset += 22

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
