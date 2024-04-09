import pygame
from .common import Scene
from .common import res_manager, get_assets, Colors, SceneManager
from .actors import Particle
from .config import configmap



class GamePreScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)

    def on_enter(self, **kwargs):
        self.chorus_channel = pygame.mixer.Channel(0)
        self.particles = pygame.sprite.Group()
        self.cover_image = res_manager.load_image(configmap["game_cover"]["cover_image"])
        self.stage_pre_sound = res_manager.load_sound(configmap["stage_pre"]["sound"])
        if self.chorus_channel and self.stage_pre_sound:
            self.chorus_channel.play(self.stage_pre_sound)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 15:
                self.manager.switch_scene("GameMainScene")
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.manager.switch_scene("GameMainScene")
            

    def update(self):
        for _ in range(10):  # 创建粒子
            self.particles.add(Particle(450, 300, Colors.yellow))
        self.particles.update()

    def draw(self, screen):
        scaled_image = pygame.transform.scale(
            self.cover_image, (screen.get_width(), screen.get_height())
        )
        screen.blit(scaled_image, (0, 0))
        self.particles.draw(screen)
        pygame.display.flip()

    def on_exit(self, **kwargs):
        self.particles.empty()

class GameEndScene(Scene):
    
    __name__ = "GameEndScene"
    
    def __init__(self, manager):
        super().__init__(manager)

    def on_enter(self, **kwargs):
        self.particles = pygame.sprite.Group()
        self.chorus_channel = kwargs.get('chorus_channel', None)
        self.game_win = kwargs.get('game_win', False)
        self.game_restart = kwargs.get('game_restart', False)
        if self.game_win:
            self.sound_stage_end = res_manager.load_sound(configmap["stage_end_win"]["sound"])
        else:
            self.sound_stage_end = res_manager.load_sound(configmap["stage_end_loss"]["sound"])
        
        if self.game_win:
            self.cover_image = res_manager.load_image(
                configmap["game_cover"]["cover_win"]
            )
        else:
            self.cover_image = res_manager.load_image(
                configmap["game_cover"]["cover_loss"]
            )
        if self.chorus_channel and self.sound_stage_end:
            self.chorus_channel.play(self.sound_stage_end)

    def update(self):
        for _ in range(10):  # 创建粒子
            self.particles.add(Particle(450, 300, Colors.yellow))
        self.particles.update()

    def draw(self, screen):
        scaled_image = pygame.transform.scale(
            self.cover_image, (screen.get_width(), screen.get_height())
        )
        screen.blit(scaled_image, (0, 0))
        self.particles.draw(screen)
        pygame.display.flip()
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_scene("GamePreScene")
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

    def on_exit(self, **kwargs):
        self.particles.empty()