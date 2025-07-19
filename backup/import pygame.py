import pygame
import math

# 初始化 Pygame
pygame.init()
Imax_Screen = pygame.display.set_mode((800, 600))  # 显示窗口大小
pygame.display.set_caption('Nishioi 360 Viewer')

# 加载360度全景图
image = pygame.image.load('nishioi.jpg')

# 摄像机控制参数：视角
yaw = 0        # 左右旋转（经度）
pitch = 0      # 上下旋转（纬度）
view_width = 800   # 视口宽度
view_height = 600  # 视口高度

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # 键盘控制方向
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                yaw -= 10  # 向左看
            elif event.key == pygame.K_RIGHT:
                yaw += 10  # 向右看
            elif event.key == pygame.K_UP:
                pitch -= 10  # 向上看
            elif event.key == pygame.K_DOWN:
                pitch += 10  # 向下看

            # yaw值保持在0~360度之间，模拟环绕地球一圈
            yaw %= 360

            # pitch范围限制（不让摄像机翻到头顶或脚下）
            pitch = max(-90, min(90, pitch))

    # 把 yaw 和 pitch 转换成图像中的像素位置
    img_width, img_height = image.get_width(), image.get_height()
    center_x = int((yaw / 360.0) * img_width)
    center_y = int(((pitch + 90) / 180.0) * img_height)

    # 计算视口（窗口）左上角的位置
    left = center_x - view_width // 2
    top = center_y - view_height // 2

    # 上下不允许翻转（不循环）
    top = max(0, min(top, img_height - view_height))

    # 左右环绕处理（如果视口超出了图像宽度）
    # if left < 0 or (left + view_width > img_width):
    #     # 把视口切成两个部分：右边剩下 + 左边从头开始
    #     right_part = img_width - left
    #     wrap_width = view_width - right_part

    #     # 绘制右边部分
    #     right_rect = pygame.Rect(left % img_width, top, right_part, view_height)
    #     Imax_Screen.blit(image, (0, 0), right_rect)

    #     # 绘制左边环绕部分
    #     wrap_rect = pygame.Rect(0, top, wrap_width, view_height)
    #     Imax_Screen.blit(image, (right_part, 0), wrap_rect)
    # else:
    # 正常情况：视口在图像范围内
    view_rect = pygame.Rect(left, top, view_width, view_height)
    Imax_Screen.blit(image, (0, 0), view_rect)

    # 更新画面
    pygame.display.flip()
    # print(img_width, img_height)