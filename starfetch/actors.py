import itertools
import random
import random
from typing import List
import pygame
import math
from .common import res_manager, Colors, DISPLAY_WIDTH, DISPLAY_HEIGHT


class Background(pygame.sprite.Sprite):
    def __init__(self, location, config_data=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        original_image = res_manager.load_image(
            random.choice(self.config["images"])
        )
        original_width, original_height = original_image.get_size()
        scale_factor = DISPLAY_WIDTH / original_width
        new_height = int(original_height * scale_factor)

        self.image = pygame.transform.scale(
            original_image, (DISPLAY_WIDTH, new_height)
        )
        self.rect = self.image.get_rect()


    def update(self):
        self.rect.y += 1  # Move the background down
        if self.rect.y >= self.rect.height:
            self.rect.y = 0


class Bullet(pygame.sprite.Sprite):
    """炮弹"""

    def __init__(
        self, x, y, speed=10, damage=1, direction="up", color=Colors.red, radius=5
    ):
        super().__init__()
        self.life_value = 1
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.radius = radius
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image = self.image.convert_alpha()

        # 从基础颜色到更亮的颜色创建渐变效果
        for r in range(radius, 0, -1):
            # 根据基础颜色和半径计算出渐变色
            color_lerp = tuple(min(255, max(0, c + (radius - r) * 12)) for c in color)
            pygame.draw.circle(self.image, color_lerp, (radius, radius), r)

        # 添加光亮点，假设光亮点颜色为纯白
        pygame.draw.circle(
            self.image, (255, 255, 255), (radius, radius // 2), radius // 4
        )

        self.rect = self.image.get_rect(center=(x, y))

    def hit(self, damage: int):
        pass

    def update(self):
        """更新炮弹位置"""
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed + random.choice([1, 2, 3, 4])
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()


class TraceBullet(pygame.sprite.Sprite):
    """跟踪炮弹"""

    def __init__(
        self,
        target_groups: List[pygame.sprite.Group],
        particle_group: pygame.sprite.Group,
        x,
        y,
        speed=10,
        damage=1,
        direction="up",
        color=Colors.red,
        radius=5,
        priority: str = "distance",
    ):
        super().__init__()
        self.life_value = 1
        self.damage = damage
        self.direction = direction
        self.speed = speed
        self.radius = radius
        self.target_groups = target_groups
        self.particle_group = particle_group
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.priority = priority

        # 从基础颜色到更亮的颜色创建渐变效果
        for r in range(radius, 0, -1):
            # 根据基础颜色和半径计算出渐变色
            color_lerp = tuple(min(255, max(0, c + (radius - r) * 12)) for c in color)
            pygame.draw.circle(self.image, color_lerp, (radius, radius), r)

        # 添加光亮点，假设光亮点颜色为纯白
        pygame.draw.circle(
            self.image, (255, 255, 255), (radius, radius // 2), radius // 4
        )

        self.rect = self.image.get_rect(center=(x, y))

    def _track_target(self, target_groups: List[pygame.sprite.Group]):
        """从多个精灵组中选择目标进行跟踪

        Args:
            target_groups: 精灵组的列表。
        """
        for group in target_groups:
            # 如果当前组不为空，则从该组中选择目标
            if group.sprites():
                targets = group.sprites()  # 获取当前组中的所有精灵

                # 定义一个函数来计算每个目标的权重
                def target_weight(target):
                    if isinstance(target, SuperBullet):
                        return -100000

                    distance = math.hypot(
                        target.rect.centerx - self.rect.centerx,
                        target.rect.centery - self.rect.centery,
                    )
                    life_value_weight = 1 / (target.life_value + 1)  # 避免除以0

                    # 根据优先级来计算权重
                    if self.priority == "distance":
                        # 距离优先，生命值作为次要条件
                        return distance + life_value_weight * 0.1
                    else:
                        # 生命值优先，距离作为次要条件
                        return life_value_weight + distance * 0.01

                # 按定义的权重函数排序目标，选择权重最低的
                closest_target = min(targets, key=target_weight)
                return closest_target

        # 如果所有组都为空，则没有目标可以选择
        return None

    def update(self, targets: List[pygame.sprite.Group] = None):
        """更新炮弹位置，并生成尾部粒子效果"""
        # 生成粒子效果
        for _ in range(1):  # 生成两个粒子
            self.particle_group.add(
                Particle(
                    self.rect.centerx,
                    self.rect.bottom,
                    Colors.white,
                    speed_range=(1, 3),
                    size_range=(1, 3),
                )
            )

        if not targets:
            targets = self.target_groups

        # 跟踪逻辑
        if targets:
            target = self._track_target(targets)
            if target:
                # 计算移动方向
                dx, dy = (
                    target.rect.centerx - self.rect.centerx,
                    target.rect.centery - self.rect.centery,
                )
                dist = math.hypot(dx, dy)
                dx, dy = dx / dist, dy / dist  # 单位化
                self.rect.x += self.speed * dx
                self.rect.y += self.speed * dy
            else:
                self.kill()
        else:
            # 根据原始方向移动
            if self.direction == "up":
                self.rect.y -= self.speed
            elif self.direction == "down":
                self.rect.y += self.speed
            elif self.direction == "left":
                self.rect.x -= self.speed
            elif self.direction == "right":
                self.rect.x += self.speed

        # 移除屏幕外的炮弹
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed_range=(0.1, 2), size_range=(1, 3, 5)):
        super().__init__()
        self.color = color
        self.size = random.choice(size_range)  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))

        # 随机分配速度和方向
        speed = random.uniform(*speed_range)
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = speed * math.cos(angle)
        self.vel_y = speed * math.sin(angle)

        self.lifetime = random.randint(20, 100)  # 随机生命周期

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1  # 递减生命周期
        self.size -= 0.05  # 逐渐减小粒子的大小，减小速度更慢一些以延长显示时间
        if self.size <= 0 or self.lifetime <= 0:
            self.kill()  # 当粒子消失或生命周期结束时，从精灵组中移除
        else:
            # 每次更新时重新创建圆形图像
            self.image = pygame.Surface(
                (int(self.size) * 2, int(self.size) * 2), pygame.SRCALPHA
            )
            self.image = self.image.convert_alpha()  # 确保支持透明度
            pygame.draw.circle(
                self.image, self.color, (int(self.size), int(self.size)), int(self.size)
            )
            self.rect = self.image.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )


class SuperBullet(pygame.sprite.Sprite):
    def __init__(
        self, x, y, target: pygame.sprite.Sprite, particle_group: None, config_data=None
    ):
        super().__init__()
        self.config = config_data
        self.particle_group = particle_group
        self.x = x
        self.y = y
        self.target = target  # 目标对象是另一个Sprite
        self.damage = self.config["damage"]
        self.speed = self.config["speed"]
        # 加载图像时保留原始图像用于旋转
        self.original_image = res_manager.load_image(self.config["image"])
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.life_value = self.config["life_value"]  # 假设初始生命值为100

    def attack(self):
        for _ in range(2):  # 生成两个粒子
            self.particle_group.add(
                Particle(self.rect.centerx, self.rect.centery, Colors.orange)
            )

        # 计算到目标的距离和角度
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # 距离目标120时，速度加倍
        if dist < self.config["acc_distance_1"]:
            self.speed *= 1.1

        # 距离目标120时，速度加倍
        if dist < self.config["acc_distance_2"]:
            self.speed *= 1.2

        # 调整炮弹位置
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # 旋转图像。注意Pygame中的角度是逆时针方向，需要转换为角度，并调整以使0度向上
        angle_degrees = math.degrees(angle) + 90
        self.image = pygame.transform.rotate(
            self.original_image, -angle_degrees
        )  # 注意这里的角度需要是负的，因为Pygame旋转方向与数学方向相反
        self.rect = self.image.get_rect(
            center=(self.rect.center)
        )  # 更新rect以保持中心位置不变

        # 边界检测
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()

    def hit(self, damage):
        """处理被击中"""
        self.life_value -= damage
        if self.life_value <= 0:
            self.kill()
        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.play()

    def update(self):
        self.attack()


class UfoSuperBullet(pygame.sprite.Sprite):
    def __init__(
        self, x, y, target: pygame.sprite.Sprite, particle_group: None, config_data=None
    ):
        super().__init__()
        self.config = config_data
        self.particle_group = particle_group
        self.x = x
        self.y = y
        self.target = target  # Target object is another Sprite
        self.damage = self.config["damage"]
        self.speed = self.config["speed"]
        self.original_image = res_manager.load_image(self.config["image"])
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.life_value = self.config["life_value"]
        self.rotation_angle = 0  # Initial rotation angle

    def attack(self):
        for _ in range(2):  # Generate two particles
            self.particle_group.add(
                Particle(self.rect.centerx, self.rect.centery, Colors.orange)
            )

        # Calculate distance and angle to target
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        angle = math.atan2(dy, dx)

        # Double the speed at certain distances
        if dist < self.config["acc_distance_1"]:
            self.speed *= 1.02
        if dist < self.config["acc_distance_2"]:
            self.speed *= 1.2

        # Adjust bullet position
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # Rotation for visual effect (since it's a circular bullet, rotation doesn't affect its direction)
        self.rotation_angle = (
            self.rotation_angle + self.speed * 15
        ) % 360  # Add 5 degrees each update
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        self.rect = self.image.get_rect(
            center=self.rect.center
        )  # Update rect to keep center position unchanged

        # Boundary check
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()

    def hit(self, damage):
        """Handle being hit"""
        self.life_value -= damage
        if self.life_value <= 0:
            self.kill()
        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.play()

    def update(self):
        self.attack()


class ShockParticle(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, color, speed=0.5):
        super().__init__()
        self.color = color
        self.speed = speed
        self.size = random.randint(9, b=15)  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # 随机生成一个角度
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.float_x = float(center_x)  # 添加这行
        self.float_y = float(center_y)  # 添加这行

        self.lifetime = random.randint(50, 100)  # 给粒子更长的生命周期

    def update(self):
        # 更新浮点数位置
        self.float_x += self.vel_x
        self.float_y += self.vel_y

        # 更新速度，使粒子加速
        self.vel_x *= 1.02
        self.vel_y *= 1.01

        # 减少生命周期，逐渐减小粒子的大小
        self.lifetime -= 0.3
        self.size -= 0.3

        if self.lifetime <= 0 or self.size <= 0:
            self.kill()  # 当生命周期结束或大小减小到0时，移除粒子
        else:
            # 重新创建图像以匹配新的大小，并保持中心位置不变
            self.image = pygame.Surface(
                (max(int(self.size * 2), 1), max(int(self.size * 2), 1)),
                pygame.SRCALPHA,
            )
            self.image = self.image.convert_alpha()
            pygame.draw.circle(
                self.image,
                self.color,
                (int(self.size), int(self.size)),
                max(int(self.size), 1),
            )

            # 更新rect对象，以便在绘制时使用正确的位置
            # 这里使用浮点数位置并转换为整数，保证粒子的中心位置绘制时不会因为尺寸变化而移动
            self.rect = self.image.get_rect(
                center=(int(self.float_x), int(self.float_y))
            )


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
        pygame.draw.rect(
            self.image, Colors.blue, (0, 0, self.rect.width, self.rect.height)
        )

        # 计算当前进度并绘制前景长方形（橘色）
        percentage = (
            self.current_points / self.total_points if self.total_points > 0 else 0
        )
        foreground_width = int(self.rect.width * percentage)
        pygame.draw.rect(
            self.image, Colors.orange, (0, 0, foreground_width, self.rect.height)
        )

        # 在长方形上显示整数百分比
        font = pygame.font.Font(None, 24)
        text_surf = font.render(
            f"upgrade: {int(percentage * 100)}%", True, Colors.white
        )
        text_rect = text_surf.get_rect(
            center=(self.rect.width // 2, self.rect.height // 2)
        )
        self.image.blit(text_surf, text_rect)


class Meteor(pygame.sprite.Sprite):
    
    def __init__(self, mtype, config_data):
        super().__init__()
        self.config = config_data
        self.x = random.choice([random.randint(10, DISPLAY_WIDTH-100), random.randint(10, DISPLAY_WIDTH-200)])
        self.y = -100
        self.speed = random.choice(self.config[mtype]["speed"])
        self.type = mtype
        self.damage = self.config[self.type]["damage"]
        self.image = res_manager.load_image(random.choice(self.config[self.type]["images"]))
        self.life_value = self.config[self.type]["life_value"]
        self.score_value = self.config[self.type]["score_value"]
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def hit(self, damage):
        self.life_value -= damage
        if self.life_value <= 0:
            self.kill()
        
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > DISPLAY_HEIGHT:
            self.kill()
