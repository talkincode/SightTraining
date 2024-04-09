import pygame
import sys

# 初始化 Pygame
pygame.init()

# 设置窗口大小
window_size = (640, 480)
screen = pygame.display.set_mode(window_size)

# 设置窗口标题
pygame.display.set_caption("Joystick Test")

# 初始化手柄
pygame.joystick.init()

# 尝试连接第一个手柄
if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Detected joystick: {joystick.get_name()}")
else:
    print("No joysticks detected.")
    sys.exit()

# 字体设置用于显示按键信息
font = pygame.font.Font(None, 36)

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 检测手柄按键事件
        if event.type == pygame.JOYBUTTONDOWN:
            print(f"joy {event.joy} Joystick button {event.button} pressed.")
            screen.fill((0, 0, 0))  # 清屏
            text = font.render(f"Button {event.button} pressed", True, (255, 255, 255))
            screen.blit(text, (100, 100))
            pygame.display.flip()  # 更新屏幕显示
        elif event.type == pygame.JOYAXISMOTION:
            # PS4手柄中，L2 通常映射到轴2，但可能因驱动或配置不同而有所变化
            print(f"joy {event.joy}  JOYAXISMOTION {event.axis} VALUE: {event.value:.2f}")
            
            # if event.axis == 2:
            #     print(f"L2 position: {event.value}")
            #     text_surface = font.render(f'L2 position: {event.value:.2f}', True, (255, 255, 255))
            #     screen.blit(text_surface, (50, 150))


pygame.quit()
