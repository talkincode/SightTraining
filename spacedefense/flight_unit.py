import random
import random
from typing import List
import pygame

from .actors import Bullet, SuperBullet, TraceBullet, UfoSuperBullet
from .common import res_manager, Colors
from .config import configmap

DISPLAY_WIDTH = configmap["display_width"]
DISPLAY_HEIGHT = configmap["display_height"]


class FlightUnit(pygame.sprite.Sprite):
    """飞行单位"""

    def __init__(self, type: str, config_data, sound_channel=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        self.sound_channel = pygame.mixer.Channel(2)
        self.type = type
        self.hp = self.config["life_value"]
        self.life_value = self.config["life_value"]
        self.shield_hp = self.config["shield_value"]
        self.shield_value = self.config["shield_value"]
        self.image_sequence = []
        self.image_index = 0
        if self.config.get("image_sequence"):
            self.image_sequence = res_manager.load_image_sequence(
                self.config["image_sequence"]
            )
            self.image = self.image_sequence[self.image_index]
        else:
            self.image = res_manager.load_image(
                random.choice(self.config["images"])
            )  # 加载图片
        self.rect = self.image.get_rect()
        self.rect.x = self.config["first_pos"][0]  # 初始化x坐标
        self.rect.y = self.config["first_pos"][1]
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 300  # 每帧间隔毫秒数
        self.speed_x = random.randint(1, 6)  # 在x方向上设置随机速度
        self.speed_y = random.randint(1, 4)  # 在y方向上设置随机速度
        # 被消灭的时间
        self.kill_time = None
        self.fire_delay = 0
        self.trace_fire_delay = 0
        self.super_fire_delay = 0
        self.fire_interceptor_delay = 0
        self.is_angry = False

        self.recharge_delay = 0  # 护盾充能延迟
        self.shield_recharge_step = self.config["shield_recharge_step"]  # 护盾充能步长

    def fire(
        self,
        group,
        direction,
        target_groups: List[pygame.sprite.Group] = None,
        particle_group: pygame.sprite.Group = None,
    ):
        self.trace_fire(group, target_groups, particle_group)
        if self.fire_delay == 0:
            group.add(
                Bullet(
                    self.rect.width // 2 + self.rect.x,
                    self.rect.width // 2 + self.rect.y,
                    speed=self.config["bullet_speed"],
                    damage=self.config["bullet_damage"],
                    direction=direction,
                    color=Colors.get(self.config["bullet_color"]),
                    radius=self.config["bullet_radius"],
                )
            )
            if self.is_angry:
                self.fire_delay = self.config["fire_delay"] // 2
            else:
                self.fire_delay = self.config["fire_delay"]

            sound = res_manager.load_sound(self.config["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def trace_fire(
        self,
        src_group,
        target_groups: List[pygame.sprite.Group]=None,
        particle_group: pygame.sprite.Group=None,
    ):
        if not target_groups:
            return
        
        if isinstance(target_groups, pygame.sprite.Group):
            target_groups = [target_groups]
            
        if target_groups and particle_group and self.trace_fire_delay == 0:
            src_group.add(
                TraceBullet(
                    target_groups,
                    particle_group,
                    self.rect.width // 2 + self.rect.x,
                    self.rect.y,
                    speed=self.config["bullet_speed"],
                    damage=self.config["bullet_damage"],
                    direction="up",
                    color=Colors.get(self.config["bullet_color"]),
                    radius=self.config["bullet_radius"],
                )
            )

            self.trace_fire_delay = self.config["trace_fire_delay"]
            sound = res_manager.load_sound(self.config["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def super_fire(self, src_group, target, particle_group):
        if self.type != "ufo_master" and "super_bullet" not in self.config:
            return 
        # self.recharge_delay = 0
        if self.super_fire_delay == 0:
            src_group.add(
                UfoSuperBullet(
                    self.rect.width // 2 + self.rect.x,
                    self.rect.y,
                    target=target,
                    particle_group=particle_group,
                    config_data=self.config["super_bullet"],
                )
            )
            self.super_fire_delay = self.config["super_bullet"]["fire_delay"]
            sound = res_manager.load_sound(
                self.config["super_bullet"]["fire_sound"],
            )
            if self.sound_channel:
                self.sound_channel.play(sound)
            else:
                sound.play()

    def fire_interceptor(
        self,
        group,
        target_groups: List[pygame.sprite.Group] = None,
        particle_group: pygame.sprite.Group = None,
    ):
        if not target_groups:
            return
        
        if isinstance(target_groups, pygame.sprite.Group):
            target_groups = [target_groups]
            
        if target_groups and particle_group and self.fire_interceptor_delay == 0:
            group.add(
                TraceBullet(
                    target_groups,
                    particle_group,
                    self.rect.width // 2 + self.rect.x,
                    self.rect.y,
                    speed=self.config["bullet_speed"],
                    damage=self.config["bullet_damage"],
                    direction="up",
                    color=Colors.get(self.config["bullet_color"]),
                    radius=self.config["bullet_radius"],
                )
            )

            self.fire_interceptor_delay = self.config["fire_interceptor_delay"]
            sound = res_manager.load_sound(self.config["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()


    def hit(self, damage: int):
        damage_value = damage
        if self.shield_hp > 0:
            if self.shield_value > 0:
                self.shield_value -= damage
                if self.shield_value < 0:
                    # 护盾值小于0，计算超出的伤害
                    excess_damage = -self.shield_value
                    self.shield_value = 0  # 重置护盾值为0
                    self.life_value -= excess_damage  # 扣除超出护盾的伤害
            else:
                self.life_value -= damage

        else:
            if self.life_value > 0:
                self.life_value -= damage_value

        if self.life_value <= 0:
            self.life_value = 0
            if not self.kill_time:
                self.kill_time = pygame.time.get_ticks()

        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.set_volume(self.config["firehit_sound_volume"])
        sound.play()

    def on_killed(self):
        pass

    def draw_health_bar(self, surface):
        """绘制血条到给定的surface上"""
        bar_length = int(self.rect.width * 1 / 2)  # 血条长度为精灵宽度的三分之二
        bar_height = 8  # 血条的厚度
        fill = (self.life_value / self.hp) * bar_length  # 根据当前生命值计算填充长度

        # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
        outline_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            bar_length,
            bar_height,
        )  # 血条外框位置
        fill_rect = pygame.Rect(
            self.rect.centerx - bar_length // 2,
            self.rect.top + self.rect.height,
            fill,
            bar_height,
        )  # 血条填充位置

        pygame.draw.rect(surface, Colors.blue, outline_rect)  # 绘制血条外框
        pygame.draw.rect(surface, Colors.yellow, fill_rect)

        if self.shield_hp > 0:
            ## 绘制护盾值到给定的surface上
            fill = (
                self.shield_value / self.shield_hp
            ) * bar_length  # 根据当前护盾计算填充长度

            # 如果血条长度仍然不符合你的需求，可以直接调整这里的 bar_length 值
            soutline_rect = pygame.Rect(
                self.rect.centerx - bar_length // 2,
                self.rect.top + self.rect.height + 10,
                bar_length,
                bar_height,
            )
            sfill_rect = pygame.Rect(
                self.rect.centerx - bar_length // 2,
                self.rect.top + self.rect.height + 10,
                fill,
                bar_height,
            )

            pygame.draw.rect(surface, Colors.blue, soutline_rect)
            pygame.draw.rect(surface, Colors.orange, sfill_rect)

    def update(self):
        self.recharge_delay += 1
        if (
            self.shield_hp > 0
            and self.shield_recharge_step > 0
            and self.shield_value < self.shield_hp
            and self.recharge_delay % self.shield_recharge_step == 0
        ):
            self.shield_value += 1

        if self.fire_delay > 0:
            self.fire_delay -= 1

        if self.trace_fire_delay > 0:
            self.trace_fire_delay -= 1
            
        if self.super_fire_delay > 0:
            self.super_fire_delay -= 1
            
        if self.fire_interceptor_delay > 0:
            self.fire_interceptor_delay -= 1

        if self.image_sequence:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.image_index = (self.image_index + 1) % len(self.image_sequence)
                self.image = self.image_sequence[self.image_index]

        if self.kill_time:
            if pygame.time.get_ticks() - self.kill_time > 500:  # 500毫秒后
                self.kill()
            else:
                self.on_killed()
        else:
            self.rect.x += self.speed_x  # 水平移动单位
            self.rect.y += self.speed_y  # 垂直移动单位

            if self.rect.left < 0:
                self.speed_x = abs(random.randint(1, 6))  # 反转x方向的速度

            if self.rect.right > DISPLAY_WIDTH:
                self.speed_x = -abs(random.randint(1, 6))  # 反转x方向的速度

            if self.rect.top < 0:
                self.speed_y = abs(random.randint(1, 4))  # 反转y方向的速度

            if self.rect.bottom > DISPLAY_HEIGHT // 2:
                self.speed_y = -abs(random.randint(1, 4))  # 反转y方向的速度

    def dodge_fighter(self, target: pygame.sprite.Sprite):
        """根据目标位置和自身速度进行闪避"""
        # 确定躲闪方向：目标在左侧还是右侧
        if target.rect.centerx < self.rect.centerx:
            # 目标在左侧，尝试向右移动
            self.speed_x = abs(self.speed_x)  # 确保速度为正值，向右移动
        else:
            # 目标在右侧，尝试向左移动
            self.speed_x = -abs(self.speed_x)  # 确保速度为负值，向左移动

        # 确定躲闪方向：目标在上方还是下方
        if target.rect.centery < self.rect.centery:
            # 目标在上方，尝试向下移动
            self.speed_y = abs(self.speed_y)  # 确保速度为正值，向下移动
        else:
            # 目标在下方，尝试向上移动
            self.speed_y = -abs(self.speed_y)  # 确保速度为负值，向上移动

        # 应用速度调整
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 避免移动出边界
        self.rect.x = max(0, min(DISPLAY_WIDTH - self.rect.width, self.rect.x))
        self.rect.y = max(0, min(DISPLAY_HEIGHT - self.rect.height, self.rect.y))

        # 如果靠近边界，适当调整速度方向和大小
        if self.rect.x <= 0 or self.rect.right >= DISPLAY_WIDTH:
            self.speed_x = -self.speed_x * 1.5  # 反转方向并加速
        if self.rect.y <= 0 or self.rect.bottom >= DISPLAY_HEIGHT // 2:
            self.speed_y = -self.speed_y * 1.5  # 反转方向并加速

    @classmethod
    def get_ufo_master(cls):
        return FlightUnit("ufo_master", configmap["ufo_master"])

    @classmethod
    def get_ufo_slave(cls):
        return FlightUnit("ufo_slave", configmap["ufo_slave"])

    @classmethod
    def get_my_slave_fighter(cls):
        return FlightUnit("myf_slave", configmap["myf_slave"])
