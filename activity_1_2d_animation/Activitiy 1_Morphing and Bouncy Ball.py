import pygame
import math
import sys

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 850, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Activity 1: 2D Kinematics, Morphing & Dynamics Engine')
clock = pygame.time.Clock()

BG_COLOR = (18, 22, 30)
PANEL_BG = (28, 34, 48)
TEXT_COLOR = (230, 235, 245)
START_COLOR = (255, 87, 87)    
END_COLOR = (52, 152, 219)    
MORPH_COLOR = (155, 207, 83)  
BALL_COLOR = (241, 196, 15)  
FLOOR_COLOR = (120, 130, 140)
BAR_BG = (45, 52, 68)

FONT = pygame.font.SysFont('Arial', 13)
TITLE_FONT = pygame.font.SysFont('Arial', 15, bold=True)

def lerp(val_start, val_end, t):
    """Linear Interpolation (LERP): P(t) = (1 - t) * P_start + t * P_end"""
    return (1.0 - t) * val_start + t * val_end

def lerp_point(p1, p2, t):
    """2D Point Linear Interpolation"""
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def lerp_color(c1, c2, t):
    """RGB Linear Interpolation"""
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t))
    )

def ease_in(t):
    """Quadratic Ease-In: Smooth acceleration"""
    return t * t

def ease_out(t):
    """Quadratic Ease-Out: Deceleration"""
    return t * (2.0 - t)

def ease_in_out(t):
    """Quadratic Ease-In / Ease-Out blend"""
    return 2.0 * t * t if t < 0.5 else -1.0 + (4.0 - 2.0 * t) * t

def get_eased_t(t, mode):
    if mode == "Ease-In":
        return ease_in(t)
    elif mode == "Ease-Out":
        return ease_out(t)
    elif mode == "Ease-In-Out":
        return ease_in_out(t)
    return t  # Linear default

poly_start = [(200, 100), (250, 200), (300, 300), (100, 300)]
poly_end   = [(150, 100), (350, 120), (320, 320), (120, 300)]

t_raw = 0.0
morph_speed = 0.45  
direction = 1
easing_modes = ["Linear", "Ease-In", "Ease-Out", "Ease-In-Out"]
current_easing_idx = 0

ball_x, ball_y = 620.0, 120.0
ball_radius = 20.0
ball_vel_y = 0.0
gravity = 980.0 
restitution = 0.75   
floor_y = 520.0
trajectory_history = [] 

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                current_easing_idx = (current_easing_idx + 1) % len(easing_modes)
            elif event.key == pygame.K_r:
                t_raw = 0.0
                direction = 1
                ball_y = 120.0
                ball_vel_y = 0.0
                trajectory_history.clear()

    t_raw += direction * morph_speed * dt
    if t_raw >= 1.0:
        t_raw = 1.0
        direction = -1
    elif t_raw <= 0.0:
        t_raw = 0.0
        direction = 1

    active_easing_mode = easing_modes[current_easing_idx]
    t_eased = get_eased_t(t_raw, active_easing_mode)

    morphed_poly = [lerp_point(p1, p2, t_eased) for p1, p2 in zip(poly_start, poly_end)]
    morphed_color = lerp_color(START_COLOR, END_COLOR, t_eased)

    ball_vel_y += gravity * dt
    ball_y += ball_vel_y * dt

    if ball_y + ball_radius >= floor_y:
        ball_y = floor_y - ball_radius
        ball_vel_y = -restitution * ball_vel_y

        if abs(ball_vel_y) < 15.0:
            ball_vel_y = 0.0

    if len(trajectory_history) == 0 or abs(trajectory_history[-1][1] - ball_y) > 2:
        trajectory_history.append((int(ball_x), int(ball_y)))
        if len(trajectory_history) > 60:
            trajectory_history.pop(0)

    screen.fill(BG_COLOR)

    pygame.draw.rect(screen, PANEL_BG, (20, 20, 390, 610), border_radius=8)
    pygame.draw.rect(screen, PANEL_BG, (430, 20, 400, 610), border_radius=8)

    title1 = TITLE_FONT.render("1. Polygon Morphing & LERP Engine", True, TEXT_COLOR)
    screen.blit(title1, (35, 35))

    pygame.draw.polygon(screen, START_COLOR, poly_start, 1)
    pygame.draw.polygon(screen, END_COLOR, poly_end, 1)

    pygame.draw.polygon(screen, morphed_color, morphed_poly)
    pygame.draw.polygon(screen, (255, 255, 255), morphed_poly, 2)

    for pt in morphed_poly:
        pygame.draw.circle(screen, (255, 255, 255), (int(pt[0]), int(pt[1])), 4)

    lbl_raw = FONT.render(f"Linear Progress (t_raw): {t_raw:.3f}", True, TEXT_COLOR)
    lbl_eased = FONT.render(f"Eased Progress (t_eased): {t_eased:.3f}", True, TEXT_COLOR)
    lbl_mode = FONT.render(f"Easing Curve [SPACE]: {active_easing_mode}", True, (241, 196, 15))
    screen.blit(lbl_raw, (35, 470))
    screen.blit(lbl_eased, (35, 490))
    screen.blit(lbl_mode, (35, 510))

    bar_x, bar_y, bar_w, bar_h = 35, 545, 360, 14
    pygame.draw.rect(screen, BAR_BG, (bar_x, bar_y, bar_w, bar_h), border_radius=4)
    fill_w = int(bar_w * t_eased)
    if fill_w > 0:
        pygame.draw.rect(screen, MORPH_COLOR, (bar_x, bar_y, fill_w, bar_h), border_radius=4)
    pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4)

    title2 = TITLE_FONT.render("2. Bouncing Ball Kinematics Engine", True, TEXT_COLOR)
    screen.blit(title2, (445, 35))

    pygame.draw.line(screen, FLOOR_COLOR, (445, int(floor_y)), (815, int(floor_y)), 3)

    if len(trajectory_history) > 1:
        pygame.draw.lines(screen, (100, 110, 130), False, trajectory_history, 2)

    squish_factor = max(0.65, min(1.35, 1.0 - (ball_vel_y * 0.0003)))
    rx = int(ball_radius / squish_factor)
    ry = int(ball_radius * squish_factor)

    ball_rect = pygame.Rect(int(ball_x - rx), int(ball_y - ry), rx * 2, ry * 2)
    pygame.draw.ellipse(screen, BALL_COLOR, ball_rect)
    pygame.draw.ellipse(screen, (255, 255, 255), ball_rect, 2)

    lbl_vel = FONT.render(f"Velocity (v_y): {ball_vel_y:.1f} px/s", True, TEXT_COLOR)
    lbl_pos = FONT.render(f"Position (y): {ball_y:.1f} px", True, TEXT_COLOR)
    lbl_rest = FONT.render(f"Restitution (e): {restitution}", True, TEXT_COLOR)
    lbl_reset = FONT.render("Press [R] to Reset Ball Drop & Morphing", True, (160, 170, 190))
    screen.blit(lbl_vel, (445, 470))
    screen.blit(lbl_pos, (445, 490))
    screen.blit(lbl_rest, (445, 510))
    screen.blit(lbl_reset, (445, 545))

    pygame.display.flip()

pygame.quit()
sys.exit()