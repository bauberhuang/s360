import pygame
import numpy as np
import math

# === Setup ===
pygame.init()
view_w, view_h = 800, 600
screen = pygame.display.set_mode((view_w, view_h))
pygame.display.set_caption("Equirectangular to Regular View")

# Load image & get data
image = pygame.image.load("tokyo.jpg").convert()
img_width, img_height = image.get_width(), image.get_height()
panorama_pixels = pygame.surfarray.array3d(image)

# Precalculate pixel coordinate grid
aspect_ratio = view_h / view_w
nx, ny = np.meshgrid(
    (2 * (np.arange(view_w) + 0.5) / view_w - 1),
    (1 - 2 * (np.arange(view_h) + 0.5) / view_h)
)
nx = nx.T
ny = ny.T

# === Camera Settings ===
yaw, pitch = 0, 0
fov = 90
sensitivity = 0.3
dragging = False
clock = pygame.time.Clock()

running = True
last_mouse_x, last_mouse_y = 0, 0

while running:
    # === Input Handling ===
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            last_mouse_x, last_mouse_y = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            mouse_x, mouse_y = event.pos
            dx = mouse_x - last_mouse_x
            dy = mouse_y - last_mouse_y
            yaw += dx * sensitivity
            pitch -= dy * sensitivity
            pitch = np.clip(pitch, -89, 89)
            yaw %= 360
            last_mouse_x, last_mouse_y = mouse_x, mouse_y

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pitch -= 3
            elif event.key == pygame.K_DOWN:
                pitch += 3
            elif event.key == pygame.K_LEFT:
                yaw -= 3
            elif event.key == pygame.K_RIGHT:
                yaw += 3
        elif event.type == pygame.MOUSEWHEEL:
            fov -= event.y * 5  # scroll up = zoom in
            fov = np.clip(fov, 20, 160)  # limit zoom range

    # === Calculate direction vectors ===
    fov_v = fov * aspect_ratio
    x_cam = np.tan(np.radians(fov / 2)) * nx
    y_cam = np.tan(np.radians(fov_v / 2)) * ny
    z_cam = np.ones_like(x_cam)

    # Normalize
    norm = np.sqrt(x_cam**2 + y_cam**2 + z_cam**2)
    x_cam /= norm
    y_cam /= norm
    z_cam /= norm

    # Rotate (pitch)
    cos_pitch = math.cos(math.radians(pitch))
    sin_pitch = math.sin(math.radians(pitch))
    y1 = y_cam * cos_pitch - z_cam * sin_pitch
    z1 = y_cam * sin_pitch + z_cam * cos_pitch
    x1 = x_cam

    # Rotate (yaw)
    cos_yaw = math.cos(math.radians(yaw))
    sin_yaw = math.sin(math.radians(yaw))
    x2 = x1 * cos_yaw + z1 * sin_yaw
    z2 = -x1 * sin_yaw + z1 * cos_yaw
    y2 = y1

    # To spherical coordinates
    yaw_equi = (np.degrees(np.arctan2(x2, z2)) + 360) % 360
    pitch_equi = np.degrees(np.arcsin(np.clip(y2, -1.0, 1.0)))

    u = yaw_equi / 360.0
    v = 0.5 - (pitch_equi / 180.0)

    # Sample source pixels
    src_x = (u * img_width).astype(np.int32) % img_width
    src_y = np.clip((v * img_height).astype(np.int32), 0, img_height - 1)

    # Make and fill viewport
    viewport_surface = pygame.Surface((view_w, view_h))
    viewport_pixels = pygame.surfarray.pixels3d(viewport_surface)
    viewport_pixels[:] = panorama_pixels[src_x, src_y]
    del viewport_pixels

    # Display
    screen.blit(viewport_surface, (0, 0))
    pygame.display.set_caption(f"FPS: {clock.get_fps():.2f}")
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
