import random
import random
import pygame

from .actors import Bullet, SuperBullet, TraceBullet
from .common import res_manager, Colors, DISPLAY_WIDTH, DISPLAY_HEIGHT


class MyMasterFighter(pygame.sprite.Sprite):
    """我方战机"""

    def __init__(self, config_data, sound_channel=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        self.level = 1
        self.upgrade_points = 0
        self.upgrade_cast = self.config["upgrade_cast"]
        self.sound_channel = sound_channel
        self.type = "myf_master"
        self.hp = self.config["life_value"]
        self.shield_hp = self.config["shield_value"]
        self.life_value = self.config["life_value"]
        self.image_sequence = []
        self.image_index = 0
        if self.config.get("image_sequence"):
            self.image_sequence = res_manager.load_image_sequence(
                self.config["image_sequence"]
            )
            self.image = self.image_sequence[self.image_index]
        else:
            self.image = res_manager.load_image(random.choice(self.config["image"]))

        self.rect = self.image.get_rect()
        self.rect.x = DISPLAY_WIDTH // 2  # 初始化x坐标
        self.rect.y = DISPLAY_HEIGHT - 170  # 将塔的y坐标设置为固定值
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 400  # 每帧间隔毫秒数
        self.speed_x = self.config["speed_x"]
        self.speed_y = 0
        self.fire_delay = 0
        self.trace_fire_delay = 0
        self.super_fire_delay = 0
        self.fire_interceptor_delay = 0
        self.shield_value = self.config["shield_value"]  # 护盾值
        self.recharge_delay = 0  # 护盾充能延迟
        self.shield_recharge_step = self.config["shield_recharge_step"]  # 护盾充能步长

    def reset_speed_x(self):
        self.speed_x = self.config["speed_x"]

    def draw_health_bar(self, surface):
        """绘制血条到给定的surface上"""
        bar_length = int(self.rect.width * 2 / 3)
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

    def fire(self, group, level):
        # self.recharge_delay = 0
        if self.fire_delay == 0:
            _bullet_per_num = self.config[level]["bullet_per_num"]
            total_bullets = _bullet_per_num  # 想要发射的子弹总数
            if self.level > 1:
                total_bullets = _bullet_per_num + self.level - 1
            if total_bullets > 6:
                total_bullets = 6

            bullet_spacing = 15  # 子弹之间的间距

            # 计算第一个子弹的偏移量
            offset = bullet_spacing * (total_bullets - 1) / 2

            for i in range(total_bullets):
                bullet_x = self.rect.centerx - offset + i * bullet_spacing
                bullet_y = self.rect.y + 40  # 子弹发射的垂直位置
                damage = self.config[level]["bullet_damage"]
                group.add(
                    Bullet(
                        bullet_x,
                        bullet_y,
                        speed=self.config[level]["bullet_speed"],
                        damage=damage + (self.level - 1) / 20,  # 升级后伤害递增
                        direction="up",
                        color=Colors.get(self.config[level]["bullet_color"]),
                        radius=self.config[level]["bullet_radius"],
                    )
                )
            self.fire_delay = self.config[level]["fire_delay"]
            sound = res_manager.load_sound(self.config[level]["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def trace_fire(
        self,
        src_group,
        target_groups,
        particle_group,
        level,
        priority: str = "distance",
        trace_fire_delay: int = 0,
    ):
        if self.trace_fire_delay == 0:
            _bullet_per_num = self.config[level]["bullet_per_num"]  # 想要发射的子弹总数
            total_bullets = _bullet_per_num  # 想要发射的子弹总数
            bullet_spacing = 25
            if self.level > 1:
                total_bullets = self.level

            if total_bullets > 2:
                total_bullets = 2

            # 计算第一个子弹的偏移量
            offset = bullet_spacing * (total_bullets - 1) / 2
            for i in range(total_bullets):
                bullet_x = self.rect.centerx - offset + i * bullet_spacing
                bullet_y = self.rect.y + 40  # 子弹发射的垂直位置
                damage = self.config[level]["bullet_damage"]
                src_group.add(
                    TraceBullet(
                        target_groups,
                        particle_group,
                        bullet_x,
                        bullet_y,
                        speed=self.config[level]["bullet_speed"],
                        damage=damage + (self.level - 1) / 20,  # 升级后伤害递增
                        direction="up",
                        color=Colors.get(self.config[level]["bullet_color"]),
                        radius=self.config[level]["bullet_radius"],
                    )
                )
            if trace_fire_delay > 0:
                self.trace_fire_delay = trace_fire_delay
            else:
                self.trace_fire_delay = self.config[level]["fire_delay"]

            sound = res_manager.load_sound(self.config[level]["fire_sound"])
            sound.set_volume(self.config["fire_sound_volume"])
            sound.play()

    def super_fire(self, src_group, target, particle_group):
        if self.level < 4:
            return
        if self.super_fire_delay == 0:
            src_group.add(
                SuperBullet(
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

    def hit(self, damage: int):
        """被击中, 减少生命值"""
        # 升级后伤害递减
        damage - (self.level - 1) / 20

        if self.shield_value > 0:
            self.shield_value -= damage
            if self.shield_value <= 0:
                self.shield_value = 0
                self.life_value += self.shield_value
        else:
            if self.life_value > 0:
                self.life_value -= damage
                if self.life_value <= 0:
                    self.life_value = 0

        sound = res_manager.load_sound(self.config["firehit_sound"])
        sound.set_volume(self.config["firehit_sound_volume"])
        sound.play()

    def dodge_fighter(self, target: pygame.sprite.Sprite):
        pass

    def update(self):
        self.recharge_delay += 1
        if (
            self.shield_value < self.shield_hp
            and self.recharge_delay % self.shield_recharge_step == 0
        ):
            self.shield_value += 1

        if self.fire_delay > 0:
            self.fire_delay -= 1

        if self.super_fire_delay > 0:
            self.super_fire_delay -= 1

        if self.trace_fire_delay > 0:
            self.trace_fire_delay -= 1

        if self.fire_interceptor_delay > 0:
            self.fire_interceptor_delay -= 1

        if self.image_sequence:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.image_index = (self.image_index + 1) % len(self.image_sequence)
                self.image = self.image_sequence[self.image_index]

        up_points = self.upgrade_cast * self.level
        if self.upgrade_points > up_points:
            self.upgrade_points -= up_points
            self.level += 1

    def auto_move(self):
        self.rect.x += self.speed_x  # 水平移动单位

        if self.rect.left < 0:
            self.speed_x = abs(random.randint(1, 5))  # 反转x方向的速度

        if self.rect.right > DISPLAY_WIDTH:
            self.speed_x = -abs(random.randint(1, 5))  # 反转x方向的速度

    def move(self, dx):
        new_x = self.rect.x + dx * self.speed_x
        if 0 <= new_x <= DISPLAY_WIDTH - 100:
            self.rect.x = new_x
