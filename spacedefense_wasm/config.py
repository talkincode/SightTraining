configmap = {
    "display_width": 1280,
    "display_height": 720,
    "fullscreen": False,
    "game_time": 600,
    "bgm": {
        "sound": "sounds/bgm.ogg",
        "sound_volume": 0.5,
    },
    "background": {
        "vmove": {
            "images": ["images/background.webp"],
        },
        "type": "vmove",
    },
    "my_score_step": 5,
    "ufo_score_step": 2,
    "unit_collision_cooldown": 1000,
    "ufo_master": {
        "images": ["images/ufo_master.webp"],
        "first_pos": (720, 100),
        "life_value": 50000,
        "shield_value": 2000,
        "shield_recharge_step": 1,
        "bullet_color": "cyan",
        "bullet_speed": 7,
        "bullet_damage": 20,
        "bullet_radius": 10,
        "trace_fire_delay": 30,
        "fire_interceptor_delay": 20,
        "fire_delay": 30,
        "fire_score": 5,
        "fire_sound": "sounds/ufo_fire.ogg",
        "firehit_sound": "sounds/ufo_firehit.ogg",
        "fire_sound_volume": 0.4,
        "firehit_sound_volume": 0.4,
        "super_bullet": {
            "score_cast": 50,
            "life_value": 300,
            "speed": 2,
            "acc_distance_1": 350,
            "acc_distance_2": 150,
            "damage": 200,
            "fire_delay": 200,
            "image": "images/ufo_super_bullet.webp",
            "fire_sound": "sounds/super_fire.ogg",
            "firehit_sound": "sounds/firehit.ogg",
        },
    },
    "ufo_slave": {
        "images": ["images/ufo_slave.webp"],
        "first_pos": (400, -100),
        "score_cast": 50,
        "max_limit": 4,
        "min_limit": 2,
        "shield_value": 100,
        "shield_recharge_step": 5,
        "life_value": 700,
        "bullet_speed": 9,
        "bullet_color": "cyan",
        "bullet_damage": 15,
        "bullet_radius": 8,
        "trace_fire_delay": 40,
        "fire_interceptor_delay": 20,
        "fire_delay": 15,
        "fire_sound": "sounds/ufo_fire.ogg",
        "firehit_sound": "sounds/ufo_firehit.ogg",
        "fire_sound_volume": 0.4,
        "firehit_sound_volume": 0.4,
    },
    "myf_master": {
        "life_value": 700,
        "shield_value": 300,
        "shield_recharge_step": 3,
        "speed_x": 8,
        "images": ["images/myf_master.webp"],
        "firehit_sound": "sounds/firehit.ogg",
        "fire_sound_volume": 0.4,
        "firehit_sound_volume": 0.4,
        "upgrade_cast": 100,
        "level1": {
            "bullet_color": "light_yellow",
            "bullet_per_num": 2,
            "bullet_speed": 15,
            "bullet_damage": 15,
            "bullet_radius": 5,
            "fire_delay": 8,
            "fire_sound": "sounds/fire.ogg",
        },
        "level2": {
            "bullet_color": "light_yellow",
            "bullet_per_num": 1,
            "bullet_speed": 10,
            "bullet_damage": 40,
            "bullet_radius": 8,
            "fire_delay": 12,
            "fire_sound": "sounds/fire.ogg",
        },
        "level3": {
            "bullet_color": "light_yellow",
            "bullet_per_num": 2,
            "bullet_speed": 7,
            "bullet_damage": 5,
            "bullet_radius": 5,
            "fire_delay": 10,
            "fire_sound": "sounds/fire.ogg",
        },
        "super_bullet": {
            "score_cast": 200,
            "life_value": 300,
            "speed": 3,
            "acc_distance_1": 400,
            "acc_distance_2": 300,
            "damage": 200,
            "fire_delay": 200,
            "image": "images/super_bullet.webp",
            "fire_sound": "sounds/super_fire.ogg",
            "firehit_sound": "sounds/firehit.ogg",
        },
    },
    "myf_slave": {
        "images": ["images/my_slave_fighter1.webp", "images/my_slave_fighter2.webp"],
        "first_pos": (-10, 300),
        "shield_value": 100,
        "shield_recharge_step": 5,
        "score_cast": 100,
        "max_limit": 4,
        "min_limit": 1,
        "life_value": 500,
        "bullet_speed": 10,
        "bullet_color": "light_yellow",
        "bullet_damage": 30,
        "bullet_radius": 8,
        "fire_delay": 10,
        "trace_fire_delay": 30,
        "fire_sound": "sounds/fire.ogg",
        "firehit_sound": "sounds/firehit.ogg",
        "fire_sound_volume": 0.4,
        "firehit_sound_volume": 0.4,
    },
}
