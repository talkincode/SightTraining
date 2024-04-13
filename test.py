import pygame
import sys
from pygame.locals import *

# 初始化 Pygame
pygame.init()

# 设置屏幕参数
SCREEN_WIDTH, SCREEN_HEIGHT = 768, 1344
CENTER_X, CENTER_Y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 设置帧率
FPS = 60
clock = pygame.time.Clock()

# 定义颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 网格参数
LINE_WIDTH = 2
NUM_LINES = 100
LINE_SPACING = SCREEN_HEIGHT // NUM_LINES

# 创建一个透明的表面来绘制网格线
grid_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), SRCALPHA)

def draw_cyberpunk_grid(surface, start_y, base_color, alpha_step):
    """绘制光栅风格的动态网格"""
    spacing = LINE_SPACING  # 网格线之间的间距

    for i in range(NUM_LINES):
        alpha = max(0, 255 - (i * alpha_step))  # Ensure alpha is not negative
        current_color = (*base_color, alpha)  # Current line color with alpha
        y = start_y + (i * spacing)
        
        # 绘制横向线
        pygame.draw.line(surface, current_color, (0, y), (SCREEN_WIDTH, y), LINE_WIDTH)
        
        # 绘制从中心到屏幕边缘的线
        pygame.draw.aaline(surface, current_color, (CENTER_X, CENTER_Y), (0, y))
        pygame.draw.aaline(surface, current_color, (CENTER_X, CENTER_Y), (SCREEN_WIDTH, y))

        # 可以根据需要添加更多线，比如从中心向左下角、右下角绘制

def main():
    start_y = 0  # 网格线的起始 y 坐标

    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # 清除屏幕
        screen.fill(BLACK)

        # 绘制网格
        alpha_step = max(1, 255 // (NUM_LINES // 2))
        grid_surface.fill((0, 0, 0, 0))  # 使用透明填充来清除之前的绘制内容
        draw_cyberpunk_grid(grid_surface, start_y, WHITE, alpha_step)

        # 将网格表面绘制到主屏幕上
        screen.blit(grid_surface, (0, 0))

        # 更新屏幕
        pygame.display.flip()

        # 更新起始 y 坐标，以创建动态扩散效果
        start_y -= 4
        if abs(start_y) >= LINE_SPACING:
            start_y = 0

        # 控制帧率
        clock.tick(FPS)

if __name__ == '__main__':
    main()
