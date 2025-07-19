import pygame
import numpy as np
import math

pygame.init()
view_w, view_h = 800, 600
screen = pygame.display.set_mode((view_w, view_h))
pygame.display.set_caption("Equirectangular to Regular View")

# Load equirectangular image
image = pygame.image.load("nishioi.jpg")
img_width, img_height = image.get_width(), image.get_height()
panorama_pixels = pygame.surfarray.array3d(image)

# View settings
yaw = 0    # camera yaw (degrees)
pitch = 0  # camera pitch (degrees)
fov = 90   # horizontal field of view in degrees

clock = pygame.time.Clock()
running = True

dragging = False
last_mouse_x, last_mouse_y = 0, 0
sensitivity = 0.3

while running:
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
            pitch = max(-89, min(89, pitch))
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

    viewport_surface = pygame.Surface((view_w, view_h))
    viewport_pixels = pygame.surfarray.pixels3d(viewport_surface)

    # Calculate vertical FOV from aspect ratio
    aspect_ratio = view_h / view_w
    fov_v = fov * aspect_ratio

    for px in range(view_w):
        for py in range(view_h):
            # Normalized device coordinates [-1,1]
            nx = (2 * (px + 0.5) / view_w) - 1
            ny = 1 - (2 * (py + 0.5) / view_h)

            # Calculate corresponding direction vector in camera space
            x_cam = math.tan(math.radians(fov / 2)) * nx
            y_cam = math.tan(math.radians(fov_v / 2)) * ny
            z_cam = 1  # camera looks along +Z

            # Normalize direction vector
            length = math.sqrt(x_cam*x_cam + y_cam*y_cam + z_cam*z_cam)
            x_cam /= length
            y_cam /= length
            z_cam /= length

            # Rotate vector by camera yaw and pitch
            # Convert yaw/pitch to radians
            yaw_rad = math.radians(yaw)
            pitch_rad = math.radians(pitch)

            # Rotation matrix components for yaw (around y-axis)
            cos_yaw = math.cos(yaw_rad)
            sin_yaw = math.sin(yaw_rad)
            # Rotation matrix components for pitch (around x-axis)
            cos_pitch = math.cos(pitch_rad)
            sin_pitch = math.sin(pitch_rad)

            # Apply pitch rotation
            x1 = x_cam
            y1 = y_cam * cos_pitch - z_cam * sin_pitch
            z1 = y_cam * sin_pitch + z_cam * cos_pitch

            # Apply yaw rotation
            x2 = x1 * cos_yaw + z1 * sin_yaw
            y2 = y1
            z2 = -x1 * sin_yaw + z1 * cos_yaw

            # Convert direction vector to spherical coordinates (yaw_equi, pitch_equi)
            yaw_equi = (math.degrees(math.atan2(x2, z2)) + 360) % 360
            pitch_equi = math.degrees(math.asin(y2))

            # Map spherical coords to equirectangular UV
            u = yaw_equi / 360.0
            v = 0.5 - (pitch_equi / 180.0)

            # Map to pixel coords in panorama image
            src_x = int(u * img_width) % img_width
            src_y = int(v * img_height)
            src_y = max(0, min(img_height - 1, src_y))

            viewport_pixels[px, py] = panorama_pixels[src_x, src_y]

    del viewport_pixels
    screen.blit(viewport_surface, (0, 0))
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
