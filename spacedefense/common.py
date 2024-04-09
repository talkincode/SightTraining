import pygame
import os
from .config import configmap

def get_assets(subfile):
    assetsDir = os.path.join(os.path.dirname(__file__), 'assets')
    return os.path.join(assetsDir, subfile)

def get_display_size():
    return (configmap["display_width"], configmap["display_height"])

class Colors:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    # 橘色
    orange = (255, 165, 0)
    # 青色
    cyan = (90, 255, 255)
    # 冷光色
    cold_light = (192, 192, 255)
    light_yellow = (255, 255, 192)

    
    
    
    
    @classmethod
    def get(cls, val):
        if val == "black":
            return cls.black
        elif val == "white":
            return cls.white
        elif val == "red":
            return cls.red
        elif val == "green":
            return cls.green
        elif val == "blue":
            return cls.blue
        elif val == "yellow":
            return cls.yellow
        elif val == "orange":
            return cls.orange
        elif val == "cyan":
            return cls.cyan
        elif val == "cold_light":
            return cls.cold_light
        elif val == "light_yellow":
            return cls.light_yellow
        else:
            return cls.white

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        
    
    def load_image_sequence(self, imgsubdir):
        images = []
        imgdir = os.path.join(os.path.dirname(__file__), f'assets/{imgsubdir}')
        for file_name in sorted(os.listdir(imgdir)):
            if file_name.endswith('.png') or file_name.endswith('.webp'):
                image = self.load_image(f'{imgsubdir}/{file_name}')
                images.append(image)
        return images
    
    def load_image(self, subpath):
        filepath = os.path.join(os.path.dirname(__file__), f'assets/{subpath}')
        if filepath not in self.images:
            self.images[filepath] = pygame.image.load(filepath).convert_alpha()
        return self.images[filepath]
    
    def load_sound(self, subpath):
        filepath = os.path.join(os.path.dirname(__file__), f'assets/{subpath}')
        if filepath not in self.sounds:
            self.sounds[filepath] = pygame.mixer.Sound(filepath)
        return self.sounds[filepath]

res_manager = ResourceManager()


class Scene:
    def __init__(self, manager):
        self.manager = manager
        self.name = self.__class__.__name__

    def update(self):
        pass

    def draw(self, screen):
        pass

    def handle_events(self, events):
        pass

    def on_enter(self, **kwargs):
        pass  # 进入场景的初始化

    def on_exit(self, **kwargs):
        pass  # 离开场景的清理

class SceneManager:
    def __init__(self):
        self.current_scene = None 
        self.scenes = {} 

    def add_scene(self, scene):
        self.scenes[scene.name] = scene

    def switch_scene(self, scene_name, **kwargs):
        if scene_name in self.scenes:
            # 停止当前场景（如果有）
            if self.current_scene:
                self.current_scene.on_exit(**kwargs) 

            self.current_scene = self.scenes[scene_name]
            self.current_scene.on_enter(**kwargs)
        else:
            print(f"Scene not found: {scene_name}")

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)
            