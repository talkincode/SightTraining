import pygame
import math

# 初始化 pygame
pygame.init()

# 定义颜色
class Colors:
    blue = (0, 0, 255)
    orange = (255, 165, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    
class ProgressRect(pygame.sprite.Sprite):
    def __init__(self, width, height, x, y):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.current_points = 0
        self.total_points = 100  # 可以根据需要修改

    def update(self, current_points, total_points):
        self.current_points = current_points
        self.total_points = total_points
        
        # Clear the previous drawing
        self.image.fill(Colors.black)

        # 绘制背景长方形（灰色）
        pygame.draw.rect(self.image, Colors.blue, (0, 0, self.rect.width, self.rect.height))

        # 计算当前进度并绘制前景长方形（橘色）
        percentage = self.current_points / self.total_points if self.total_points > 0 else 0
        foreground_width = int(self.rect.width * percentage)
        pygame.draw.rect(self.image, Colors.orange, (0, 0, foreground_width, self.rect.height))

        # 在长方形上显示整数百分比
        font = pygame.font.Font(None, 24)
        text_surf = font.render(f"{int(percentage * 100)}%", True, Colors.white)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surf, text_rect)

# 创建窗口
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Progress Rect Display")

# 创建进度条精灵和精灵组
progress_rect = ProgressRect(300, 50, 250, 275)  # 长方形位置和大小
sprite_group = pygame.sprite.Group(progress_rect)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 更新精灵状态
    progress_rect.update(45, 100)  # 假设这是当前进度

    # 绘制
    screen.fill(Colors.black)  # 用黑色填充屏幕以清除旧图像
    sprite_group.draw(screen)  # 绘制精灵组中的所有精灵到屏幕上
    pygame.display.flip()  # 更新整个待显示的 Surface 对象到屏幕上

pygame.quit()
