import pygame
from .scene_main import GameMainScene
from .scenes import GameEndScene
from .scenes import GamePreScene
from .config import configmap
from .common import get_assets, SceneManager, res_manager
from .actors import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
)

IS_FULLSCREEN = configmap["fullscreen"]


class SpaceDefense(object):
    
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.joystick.init()
        pygame.mixer.init()
        pygame.mixer.set_reserved(2)
        if IS_FULLSCREEN:
            self.screen = pygame.display.set_mode(
                (DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.set_icon(res_manager.load_image("images/icon.png"))
        pygame.display.set_caption("Space Defense")

        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()        
        
    #######################################################
    ## start game
    #######################################################
    def start_game(self):
        """开始游戏"""
        scene_manager = SceneManager()
        main_scene = GameMainScene(scene_manager)
        pre_scene = GamePreScene(scene_manager)
        end_scene = GameEndScene(scene_manager)
        scene_manager.add_scene(main_scene)
        scene_manager.add_scene(pre_scene)
        scene_manager.add_scene(end_scene)
        scene_manager.switch_scene(GamePreScene.__name__)

        running = True
        clock = pygame.time.Clock()
        while running:
            scene_manager.handle_events(pygame.event.get())
            scene_manager.update()
            scene_manager.draw(self.screen)
            pygame.display.flip()  # 更新显示
            clock.tick(60)  # 设置帧率


def main():
    SpaceDefense().start_game()


if __name__ == "__main__":
    main()
