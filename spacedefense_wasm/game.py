import asyncio
import random
import pygame
from .config import configmap
from .scene_main import GameMainScene
from .common import Scene, SceneManager, res_manager, Colors
from .actors import (
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
)

IS_FULLSCREEN = configmap["fullscreen"]


class WasmGameStartScene(Scene):

    __name__ = "WasmGameStartScene"

    def __init__(self, manager):
        super().__init__(manager)
        self.title_font = pygame.font.Font(None, size=120)
        self.title_text_surface = self.title_font.render(
            "SpaceDefense", True, Colors.orange
        )
        self.title_text_rect = self.title_text_surface.get_rect(center=(500, 300))
        
        self.font = pygame.font.Font(None, size=72)
        self.text_surface = self.font.render(
            "Press space key to start", True, (255, 255, 255)
        )
        self.text_rect = self.text_surface.get_rect(center=(500, 400))

    def on_enter(self, **kwargs):
        pass

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.manager.switch_scene("GameMainScene")
                    return

    def update(self):
        pass

    def draw(self, screen):
        screen.fill((0, 0, 0))
        # Generate small stars as white or light grey dots
        for _ in range(10):  # Adjust the range for more or fewer stars
            star_color = random.choice([(255, 255, 255), (200, 200, 200)])  # White or light grey
            star_position = (random.randint(0, 1280), random.randint(0, 720))  # Assuming screen size of 1280x720
            pygame.draw.circle(screen, star_color, star_position, random.randint(1, 3))
        
        # Optionally, add some larger stars or distant galaxies as bigger circles with different colors
        for _ in range(5):  # Adjust for more or fewer larger stars/galaxies
            galaxy_color = random.choice([(255, 255, 0), (0, 255, 255), (255, 0, 0)])  # Yellow, Cyan, Red
            galaxy_position = (random.randint(0, 1280), random.randint(0, 720))
            pygame.draw.circle(screen, galaxy_color, galaxy_position, random.randint(3, 9))
            
        screen.blit(self.title_text_surface, self.title_text_rect)
        screen.blit(self.text_surface, self.text_rect)


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
        scene_manager.add_scene(wasm_scene)
        scene_manager.add_scene(main_scene)
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
