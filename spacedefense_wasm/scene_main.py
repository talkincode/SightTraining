import random
import pygame

from .my_master import MyMasterFighter
from .config import configmap
from .common import (
    Scene,
    res_manager,
    get_assets,
    Colors,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
)
from .flight_unit import FlightUnit
from .actors import (
    Background,
    Particle,
    ProgressRect,
    ShockParticle,
)


IS_FULLSCREEN = configmap["fullscreen"]


class GameMainScene(Scene):

    __name__ = "GameMainScene"

    def __init__(self, manager):
        super().__init__(manager)

    def on_enter(self, **kwargs):
        self.auto_game = False
        self.chorus_channel = pygame.mixer.Channel(0)
        self.myf_channel = pygame.mixer.Channel(1)
        self.chorus_channel.set_volume(0.5)
        self.title_font = pygame.font.Font(None, 42)
        self.subtitle_font = pygame.font.Font(None, 36)
        self.countdown = configmap["game_time"]
        self.my_support_delay = 0
        self.my_score = 0
        self.ufo_score = 0
        self.my_score_step = configmap["my_score_step"]
        self.ufo_score_step = configmap["ufo_score_step"]
        self.unit_collision_cooldown = configmap["unit_collision_cooldown"]
        self.unit_collision_cooldowns = {}

        self.ufo_limit = configmap["ufo_slave"]["min_limit"]
        self.myf_limit = configmap["myf_slave"]["min_limit"]

        self.myf_master_fire1_active = False
        self.myf_master_fire2_active = False
        self.myf_master_fire3_active = False
        self.myf_master_x_position = 0

        self.setup_background()
        self.setup_groups()
        self.setup_events()
        self.create_actors()
        self.play_bgm()

    def setup_background(self):
        self.background_type = configmap["background"]["type"]
        self.background = Background([0, 0], configmap["background"]["vmove"])
        self.bggroup = pygame.sprite.Group()
        self.bggroup.add(self.background)

    def update_my_socre(self, score_value):
        self.my_score += score_value
        if score_value > 0:
            self.my_master_fighter.upgrade_points += score_value / 5
        if self.my_score < 0:
            self.my_score = 0

    def update_ufo_socre(self, score_value):
        self.ufo_score += score_value
        if self.ufo_score < 0:
            self.ufo_score = 0

    def play_bgm(self):
        """播放背景音乐""" ""
        pygame.mixer.music.load(get_assets(configmap["bgm"]["sound"]))
        pygame.mixer.music.set_volume(configmap["bgm"]["sound_volume"])
        pygame.mixer.music.play(-1)

    def setup_groups(self):
        # 粒子组
        self.particles = pygame.sprite.Group()
        self.shock_particles = pygame.sprite.Group()
        # 我方炮弹组
        self.my_bullets = pygame.sprite.Group()
        self.my_super_bullets = pygame.sprite.Group()
        # 敌方炮弹组
        self.ufo_super_bullets = pygame.sprite.Group()
        self.ufo_bullets = pygame.sprite.Group()
        # 我方飞行单位组
        self.my_flight_units = pygame.sprite.Group()
        # 敌方飞行单位组
        self.ufo_units = pygame.sprite.Group()
        self.layout_units = pygame.sprite.Group()

    def create_actors(self):
        # 创建敌方飞行单位
        self.ufo_master = FlightUnit.get_ufo_master()
        self.ufo_units.add(self.ufo_master)
        self.my_master_fighter = MyMasterFighter(
            configmap["myf_master"], self.myf_channel
        )
        self.my_flight_units.add(self.my_master_fighter)

        self.my_master_upstate = ProgressRect(180, 32, 20, y=20)
        self.layout_units.add(self.my_master_upstate)

    def setup_events(self):
        # 创建一个计时器事件
        self.TIMEREVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TIMEREVENT, 1000)

        # 创建一个UFO开火计时器事件
        self.UFO_FIRE_TIMEREVENT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.UFO_FIRE_TIMEREVENT, millis=250)

        # UFO Slave 进场事件
        self.SUFO_TIMEREVENT = pygame.USEREVENT + 4
        pygame.time.set_timer(self.SUFO_TIMEREVENT, 3000)

        # 我方导弹事件
        self.MY_FIGHTER_SUPER_FIRE_TIMEREVENT = pygame.USEREVENT + 5

        self.MY_FIGHTER_FIRE_TIMEREVENT = pygame.USEREVENT + 6
        pygame.time.set_timer(self.MY_FIGHTER_FIRE_TIMEREVENT, 250)

        self.SWITCH_BG_TIMEREVENT = pygame.USEREVENT + 7
        pygame.time.set_timer(self.SWITCH_BG_TIMEREVENT, 30000)

        self.STAGE_STATE_EVENT = pygame.USEREVENT + 10

    def create_hit_particle(self, actor_obj, num):
        for _ in range(int(num)):
            particle = Particle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + 10,
                Colors.light_yellow,
            )
            self.particles.add(particle)

    def create_uhit_particle(self, actor_obj, num):
        for _ in range(int(num)):
            particle = Particle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + 10,
                Colors.yellow,
                speed_range=(0.1, 3),
            )
            self.particles.add(particle)

    def myf_fire_super_bullet(self):
        # 发射导弹
        score_cast = configmap["myf_master"]["super_bullet"]["score_cast"]
        if self.my_score >= score_cast and self.my_master_fighter.super_fire_delay == 0:
            _target = self.ufo_master
            if len(self.ufo_super_bullets) > 0:
                _target = self.ufo_super_bullets.sprites()[0]
            self.my_master_fighter.super_fire(
                self.my_super_bullets,
                _target,
                self.particles,
            )
            pygame.event.post(pygame.event.Event(self.MY_FIGHTER_SUPER_FIRE_TIMEREVENT))
            self.update_my_socre(-score_cast)

    def myf_fire_level1(self):
        """发射1级炮弹"""
        self.my_master_fighter.fire(
            self.my_bullets,
            "level1",
        )
        if self.my_master_fighter.level >= 5:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_super_bullets, self.ufo_bullets],
                self.particles,
                "level3",
                trace_fire_delay=32,
            )

    def create_hit_shock_particle(self, actor_obj, num):
        for _ in range(int(num)):
            particle = ShockParticle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + actor_obj.rect.height // 2,
                Colors.white,
                speed=4,
            )
            self.shock_particles.add(particle)

    def _proc_on_joyaxis_event(self, event):
        """手柄事件"""
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                self.myf_master_x_position = event.value
            # elif event.axis == 4 and event.value > 0.2:

            elif event.axis == 5 and event.value > 0.2:
                self.myf_fire_super_bullet()

        if event.type == pygame.JOYBUTTONUP:
            if event.button == 0:
                self.myf_master_fire1_active = False
            elif event.button == 1:
                self.myf_master_fire2_active = False
            elif event.button == 3:
                self.myf_master_fire3_active = False

        elif event.type == pygame.JOYBUTTONDOWN:
            # 左右移动
            if event.button == 13:
                self.myf_master_x_position = -1
            elif event.button == 14:
                self.myf_master_x_position = 1

            elif event.button == 0:
                # 速射机炮
                self.myf_master_fire1_active = True

            elif event.button == 1:
                # 制导重炮
                self.myf_master_fire2_active = True
            elif event.button == 3:
                # 发射干扰弹
                self.myf_master_fire3_active = True
            elif event.button == 2:
                self.myf_fire_super_bullet()
            elif event.button == 9:
                self.auto_game = not self.auto_game
                self.my_master_fighter.reset_speed_x()
            elif event.button == 10:
                # 呼叫资源
                if self.my_support_delay == 0:
                    self._call_my_support()

    def _proc_update_myf_master_x_position(self):
        # 这里假设 self.my_master_fighter.move 接受一个速度参数
        # 并根据这个速度连续移动角色
        # 你可能需要根据摇杆位置调整移动速度的实际值
        if abs(self.myf_master_x_position) > 0.1:  # 应用死区
            self.my_master_fighter.move(self.myf_master_x_position)

    def _proc_check_joystick_fire_active(self):
        if self.myf_master_fire1_active:
            self.myf_fire_level1()
        elif self.myf_master_fire2_active:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_super_bullets, self.ufo_units],
                self.particles,
                "level2",
                priority="life_value",
            )
        elif self.myf_master_fire3_active:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_super_bullets, self.ufo_bullets],
                self.particles,
                "level3",
            )

    def _proc_on_keydown(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.my_master_fighter.move(-1)  # 向左移动
        if keys[pygame.K_RIGHT]:
            self.my_master_fighter.move(1)  # 向右移动
        if keys[pygame.K_1]:
            self.myf_fire_level1()
        if keys[pygame.K_2]:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_super_bullets, self.ufo_units],
                self.particles,
                "level2",
            )
        if keys[pygame.K_3]:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_super_bullets, self.ufo_bullets],
                self.particles,
                "level3",
            )
        if keys[pygame.K_5]:
            self.myf_fire_super_bullet()
        if keys[pygame.K_4]:
            if self.my_support_delay == 0:
                self._call_my_support()

        if keys[pygame.K_a]:
            self.auto_game = not self.auto_game
            self.my_master_fighter.reset_speed_x()

        if keys[pygame.K_f]:
            if pygame.display.is_fullscreen():
                self.screen = pygame.display.set_mode(
                    (DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN
                )
            else:
                self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

    def _proc_on_event(self, event):
        if event.type == pygame.QUIT:
            self.manager.switch_scene("WasmGameStartScene", game_win=False)
            return
        elif event.type == self.TIMEREVENT:  # 如果是计时器事件
            self.countdown -= 1  # 倒计时减1
            if (
                self.ufo_master.life_value <= 0
                and self.my_master_fighter.life_value > 0
            ):
                self.manager.switch_scene("WasmGameStartScene", game_win=True)
                return
            elif self.my_master_fighter.life_value <= 0 or self.countdown <= 0:
                self.manager.switch_scene("WasmGameStartScene", game_win=False)
                return

            if self.my_support_delay > 0:
                self.my_support_delay -= 1

        elif event.type == self.UFO_FIRE_TIMEREVENT:
            for ufo in self.ufo_units:
                directions = ["down"]
                if len(self.my_flight_units) > 1:
                    directions = [
                        "down",
                        "down",
                        "left",
                        "down",
                        "right",
                        "down",
                    ]

                ufo.fire(
                    group=self.ufo_bullets,
                    direction=random.choice(directions),
                    target_groups=[self.my_flight_units, self.my_bullets],
                    particle_group=self.particles,
                )
                score_cast = configmap["ufo_master"]["super_bullet"]["score_cast"]
                if (
                    self.ufo_score > score_cast * 3
                    and self.ufo_master.super_fire_delay == 0
                ):
                    ufo.super_fire(
                        self.ufo_super_bullets,
                        self.my_master_fighter,
                        self.particles,
                    )
                    self.update_ufo_socre(-score_cast)
                ufo.fire_interceptor(
                    group=self.ufo_bullets,
                    target_groups=[self.my_super_bullets],
                    particle_group=self.particles,
                )

        elif event.type == self.MY_FIGHTER_FIRE_TIMEREVENT:
            for myf in self.my_flight_units:
                if myf.type == "myf_master" and self.auto_game:
                    self._auto_myf_master()
                if myf.type == "myf_slave":
                    my_direction = "left"
                    if myf.rect.x < self.ufo_master.rect.x:
                        my_direction = "right"
                    myf.fire(
                        group=self.my_bullets,
                        direction=my_direction,
                        target_groups=[
                            self.ufo_super_bullets,
                            self.ufo_units,
                            self.ufo_bullets,
                        ],
                        particle_group=self.particles,
                    )

        elif event.type == self.MY_FIGHTER_SUPER_FIRE_TIMEREVENT:
            for uf in self.ufo_units:
                uf.fire_interceptor(
                    group=self.ufo_bullets,
                    target_groups=[self.my_super_bullets],
                    particle_group=self.particles,
                )
        elif event.type == self.SUFO_TIMEREVENT:
            # UFO 自动呼叫支援
            self._auto_ufo_support()

    def _auto_myf_master(self):
        # fire_type = "level2"

        if len(self.ufo_bullets) > len(self.my_bullets) * 2:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_bullets],
                self.particles,
                "level3",
            )

        if self.my_score < 100:
            self.my_master_fighter.trace_fire(
                self.my_bullets,
                [self.ufo_units],
                self.particles,
                "level2",
                priority="life_value",
            )

        # if abs(self.my_master_fighter.rect.centery - self.ufo_master.rect.centery) < 100:
        #     fire_type = "level1"

        # if fire_type == "level1":
        #     self.my_master_fighter.fire(
        #         self.my_bullets,
        #         "level1",
        #     )
        # elif fire_type == "level2":
        #     self.my_master_fighter.trace_fire(
        #         self.my_bullets,
        #         [self.ufo_units],
        #         self.particles,
        #         "level2",
        #         priority="life_value",
        #     )
        # elif fire_type == "level3":
        #     self.my_master_fighter.trace_fire(
        #         self.my_bullets,
        #         [self.ufo_bullets],
        #         self.particles,
        #         "level3",
        #     )

        if self.my_support_delay == 0 and len(self.my_flight_units) < 2:
            self._call_my_support()

        self.myf_fire_super_bullet()

    def _auto_ufo_support(self):
        score_cast = configmap["ufo_slave"]["score_cast"]
        ufo_max_limit = configmap["ufo_slave"]["max_limit"]
        myf_max_limit = configmap["myf_slave"]["max_limit"]
        if self.ufo_score >= score_cast and len(self.ufo_units) - 1 < self.ufo_limit:
            sufo = FlightUnit.get_ufo_slave()
            self.ufo_score -= score_cast
            if self.ufo_score < 0:
                self.ufo_score = 0
            self.ufo_units.add(sufo)

        # 狂暴检测
        if self.countdown < 120:
            if not self.ufo_master.is_angry:
                self.ufo_master.is_angry = True
                self.ufo_limit = ufo_max_limit
                self.myf_limit = myf_max_limit

    def _call_my_support(self):
        score_cast = configmap["myf_slave"]["score_cast"]
        if (
            self.my_score >= score_cast
            and len(self.my_flight_units) - 1 < self.myf_limit
        ):
            self.my_support_delay = 3
            my_support = FlightUnit.get_my_slave_fighter()
            self.update_my_socre(-score_cast)
            self.my_flight_units.add(my_support)

    def check_collision_cooldown(self, obja, objb):
        # 碰撞冷却检测
        collision_key = (min(id(obja), id(objb)), max(id(obja), id(objb)))
        current_time = pygame.time.get_ticks()
        last_collision_time = self.unit_collision_cooldowns.get(collision_key, 0)
        if current_time - last_collision_time > self.unit_collision_cooldown:
            self.unit_collision_cooldowns[collision_key] = current_time
            return True
        return False

    def _proc_on_collisions(self):
        """处理碰撞检测, 伤害值， 分数值更新"""

        # 检测我方导弹与UFO单位的碰撞
        super_collisions = pygame.sprite.groupcollide(
            self.my_super_bullets, self.ufo_units, False, False
        )
        for my_bullet, hit_ufo_units in super_collisions.items():
            for ufo_unit in hit_ufo_units:
                if self.check_collision_cooldown(my_bullet, ufo_unit):
                    if ufo_unit.type == "ufo_master":
                        ufo_unit.hit(my_bullet.damage)
                        self.create_hit_shock_particle(ufo_unit, 50)
                        super_fire_sound = res_manager.load_sound(
                            "sounds/super_firehit.ogg"
                        )
                        self.myf_channel.play(super_fire_sound)
                        my_bullet.kill()
                    else:
                        ufo_unit.dodge_fighter(my_bullet)
                        if my_bullet.life_value > 50:
                            self.create_uhit_particle(ufo_unit, 30)
                            ufo_unit.hit(10)
                            my_bullet.hit(10)
                        else:
                            ufo_unit.hit(my_bullet.damage)
                            my_bullet.kill()

        # 检测UFO导弹与我方单位的碰撞
        ufo_super_collisions = pygame.sprite.groupcollide(
            self.ufo_super_bullets, self.my_flight_units, False, False
        )
        for ufo_bullet, hit_myf_units in ufo_super_collisions.items():
            for myf_unit in hit_myf_units:
                if self.check_collision_cooldown(ufo_bullet, myf_unit):
                    if myf_unit.type == "myf_master":
                        myf_unit.hit(ufo_bullet.damage)
                        self.create_hit_shock_particle(myf_unit, 30)
                        super_fire_sound = res_manager.load_sound(
                            "sounds/super_firehit.ogg"
                        )
                        self.myf_channel.play(super_fire_sound)
                        ufo_bullet.kill()
                    else:
                        myf_unit.dodge_fighter(ufo_bullet)
                        if ufo_bullet.life_value > 50:
                            self.create_uhit_particle(myf_unit, 30)
                            myf_unit.hit(10)
                            ufo_bullet.hit(10)
                        else:
                            myf_unit.hit(ufo_bullet.damage)
                            ufo_bullet.kill()

        # 检测我方炮弹与UFO单位的碰撞
        collisions = pygame.sprite.groupcollide(
            self.my_bullets, self.ufo_units, False, False
        )
        for my_bullet, hit_ufo_units in collisions.items():
            for ufo_unit in hit_ufo_units:
                ufo_unit.hit(my_bullet.damage)
                self.create_hit_particle(ufo_unit, my_bullet.damage * 2)
                self.update_my_socre(my_bullet.damage // self.my_score_step)
                my_bullet.kill()

        # 检测UFO炮弹与我方飞行单位的碰撞
        ucollisions = pygame.sprite.groupcollide(
            self.ufo_bullets, self.my_flight_units, True, False
        )

        for u_bullet, hit_my_units in ucollisions.items():
            for my_unit in hit_my_units:
                my_unit.hit(u_bullet.damage)
                self.create_hit_particle(my_unit, u_bullet.damage)
                self.update_ufo_socre(u_bullet.damage // self.ufo_score_step)

        # 检测UFO导弹与我方导弹的碰撞
        ss_collisions = pygame.sprite.groupcollide(
            self.ufo_super_bullets, self.my_super_bullets, True, True
        )

        for u_bullet, my_bullets in ss_collisions.items():
            self.create_hit_shock_particle(u_bullet, 30)

        # 检测我方炮弹与UFO炮弹的碰撞
        mbub_collisions = pygame.sprite.groupcollide(
            self.my_bullets, self.ufo_bullets, True, True
        )
        for myb, ubs in mbub_collisions.items():
            for ub in ubs:
                self.create_hit_particle(ub, 2)

        # 检测我方导弹与UFO炮弹的碰撞
        sbub_collisions = pygame.sprite.groupcollide(
            self.my_super_bullets, self.ufo_bullets, False, True
        )

        for myb, ubs in sbub_collisions.items():
            for ub in ubs:
                self.create_hit_particle(myb, 5)
                myb.hit(ub.damage)

        # 检测我UFO导弹与我方炮弹的碰撞
        usbub_collisions = pygame.sprite.groupcollide(
            self.ufo_super_bullets, self.my_bullets, False, True
        )

        for usupb, mybs in usbub_collisions.items():
            for myb in mybs:
                self.create_hit_particle(usupb, 5)
                usupb.hit(myb.damage)
                self.update_my_socre(myb.damage // self.my_score_step)

        # 检测导弹冲击波与UF方炮弹的碰撞
        pygame.sprite.groupcollide(
            self.shock_particles, self.ufo_bullets, dokilla=True, dokillb=True
        )

        # 检测导弹冲击波与我方炮弹的碰撞
        pygame.sprite.groupcollide(
            self.shock_particles, self.my_bullets, dokilla=True, dokillb=True
        )

        # 检测我方飞行单位与UFO单位的碰撞
        xcollisions = pygame.sprite.groupcollide(
            self.my_flight_units, self.ufo_units, False, False
        )
        for myf, uflist in xcollisions.items():
            for uf in uflist:
                myf.dodge_fighter(uf)
                uf.dodge_fighter(myf)
                if self.check_collision_cooldown(myf, uf):
                    self.create_uhit_particle(uf, 50)
                    myf.hit(10)
                    uf.hit(10)
                    blast_sound = res_manager.load_sound("sounds/fire_blast.ogg")
                    blast_sound.set_volume(0.8)
                    self.myf_channel.play(blast_sound)
                    self.update_my_socre(10)
                    self.update_ufo_socre(10)

        # 检测导弹爆炸冲击波粒子对 UF单位的碰撞
        super_collisions = pygame.sprite.groupcollide(
            self.shock_particles, self.ufo_units, False, False
        )
        for mysp, uflist in super_collisions.items():
            for uf in uflist:
                if self.check_collision_cooldown(mysp, uf):
                    uf.hit(0.01)

        # 检测导弹爆炸冲击波粒子对我方单位的碰撞
        super_collisions2 = pygame.sprite.groupcollide(
            self.shock_particles, self.my_flight_units, False, False
        )
        for mysp, myflist in super_collisions2.items():
            for myf in myflist:
                if self.check_collision_cooldown(mysp, myf):
                    myf.hit(0.01)

    def _proc_draw_texts(self, screen):
        #################### 在左下角绘制倒计时
        mins, secs = divmod(self.countdown, 60)
        timer_str = "{:02d}:{:02d}".format(mins, secs)
        countdown_text = self.title_font.render(str(timer_str), True, Colors.white)
        screen.blit(
            countdown_text,
            (20, screen.get_height() - countdown_text.get_height() - 36),
        )

        #################### 在中间显示战斗机 HP
        fighter_life_text = self.title_font.render(
            f"OUR/{round(self.my_master_fighter.level)} : {round(self.my_master_fighter.life_value)} <> SCORE: {round(self.my_score)}",
            True,
            Colors.red,
        )
        screen.blit(
            fighter_life_text,
            (
                200,
                screen.get_height() - fighter_life_text.get_height() - 36,
            ),
        )

        fighter_recharge_text = self.subtitle_font.render(
            f"Shield: {round(self.my_master_fighter.shield_value)}",
            True,
            Colors.white,
        )
        screen.blit(
            fighter_recharge_text,
            (
                200,
                screen.get_height() - fighter_recharge_text.get_height() - 8,
            ),
        )

        #################### 在右下角显示UFO HP
        ufo_life_text = self.title_font.render(
            f"UFO: {round(self.ufo_master.life_value)} <> SCORE: {round(self.ufo_score)}",
            True,
            Colors.orange,
        )  # 创建分数文本
        screen.blit(
            ufo_life_text,
            (
                screen.get_width() - ufo_life_text.get_width() - 20,
                screen.get_height() - ufo_life_text.get_height() - 36,
            ),
        )

        ufo_shield_text = self.subtitle_font.render(
            f"Shield: {round(self.ufo_master.shield_value)}",
            True,
            Colors.white,
        )
        screen.blit(
            ufo_shield_text,
            (
                screen.get_width() - ufo_life_text.get_width() - 20,
                screen.get_height() - ufo_shield_text.get_height() - 8,
            ),
        )

    def update(self):

        # 检测键盘
        self._proc_on_keydown()

        # 碰撞检测
        self._proc_on_collisions()

        # 检测手柄移动状态
        self._proc_update_myf_master_x_position()
        # 检测手柄开火状态
        self._proc_check_joystick_fire_active()

        # 自动游戏
        # if self.auto_game:
        #     self.my_master_fighter.auto_move()

        # 更新精灵组
        self.particles.update()
        self.my_bullets.update()
        self.ufo_bullets.update()
        self.shock_particles.update()
        self.my_flight_units.update()
        self.ufo_units.update()
        self.my_super_bullets.update()
        self.ufo_super_bullets.update()
        self.my_master_upstate.update(
            round(self.my_master_fighter.upgrade_points),
            round(self.my_master_fighter.level * self.my_master_fighter.upgrade_cast),
        )

    def draw(self, screen):
        # 绘制背景
        self.background.update()
        screen.blit(
            self.background.image,
            (self.background.rect.x, self.background.rect.y),
        )
        screen.blit(
            self.background.image,
            (
                self.background.rect.x,
                self.background.rect.y - self.background.rect.height,
            ),
        )
        # 绘制精灵组
        self.particles.draw(screen)
        self.shock_particles.draw(screen)

        self.my_flight_units.draw(screen)
        for unit in self.my_flight_units:
            unit.draw_health_bar(screen)

        self.ufo_units.draw(screen)
        for unit in self.ufo_units:
            unit.draw_health_bar(screen)

        self.my_bullets.draw(screen)
        self.ufo_bullets.draw(screen)

        self.my_super_bullets.draw(screen)
        self.ufo_super_bullets.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), (0, DISPLAY_HEIGHT - 70, DISPLAY_WIDTH, 70))
        self._proc_draw_texts(screen)

        self.layout_units.draw(screen)

    def handle_events(self, events):
        for event in events:
            self._proc_on_event(event)
            self._proc_on_joyaxis_event(event)
