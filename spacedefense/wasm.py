import asyncio
import pygame
from .config import configmap
from .scene_main import GameMainScene
from .scenes import GameEndScene
from .scenes import GamePreScene
from .common import Scene, SceneManager, res_manager
from .actors import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
)

IS_FULLSCREEN = configmap["fullscreen"]


class WasmGameStartScene(Scene):

    __name__ = "WasmGameStartScene"

    def __init__(self, manager):
        super().__init__(manager)
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(
            "Press any key to start", True, (255, 255, 255)
        )
        self.text_rect = self.text_surface.get_rect(center=(450, 300))

    def on_enter(self, **kwargs):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN:
                self.manager.switch_scene("GamePreScene")
                return

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.text_surface, self.text_rect)
        pygame.display.flip()

    def on_exit(self, **kwargs):
        pass


class AsyncSpaceDefense(object):

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
    async def start_game(self):
        """开始游戏"""
        scene_manager = SceneManager()
        wasm_scene = WasmGameStartScene(scene_manager)
        main_scene = GameMainScene(scene_manager)
        pre_scene = GamePreScene(scene_manager)
        end_scene = GameEndScene(scene_manager)
        scene_manager.add_scene(wasm_scene)
        scene_manager.add_scene(main_scene)
        scene_manager.add_scene(pre_scene)
        scene_manager.add_scene(end_scene)
        scene_manager.switch_scene(WasmGameStartScene.__name__)

        running = True
        clock = pygame.time.Clock()
        while running:
            scene_manager.handle_events(pygame.event.get())
            scene_manager.update()
            scene_manager.draw(self.screen)
            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)


async def main():
    await AsyncSpaceDefense().start_game()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
