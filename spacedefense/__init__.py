

import pygame


def runapp():
    try:
        import argparse
        parser = argparse.ArgumentParser(description="Run SightTraining game.")
        parser.add_argument("-D", "--debug", action="store_true", help="Run game in debug mode.")
        parser.add_argument("-t", "--train", action="store_true", help="Run game in eye train mode.")
        parser.add_argument("-f", "--fullscreen", action="store_true", help="Run game in fullscreen mode.")
        parser.add_argument("-r", "--resolution", choices=["1080", "900", "720"], default="720", help="Set game resolution.")
        parser.add_argument("-l", "--level", choices=["x", "xx", "xxx"], default="x", help="Set game Level.")

        args = parser.parse_args()

        
        from spacedefense.config import configmap
        
        if args.fullscreen:
            configmap["fullscreen"] = True
            
        if not args.train:
            configmap["background"]["vmove"]["image_sequence_group"] =  ["images/vmove_cambg2"]
            
        if args.level == "x":
            # UFO 参数
            configmap["ufo_master"]["life_value"] = 30000 # 生命值
            configmap["ufo_master"]["shield_value"] = 1000 # 护盾
            configmap["ufo_master"]["super_bullet"]["score_cast"] = 100 # 核弹消耗
            configmap["ufo_master"]["super_bullet"]["speed"] = 2 # 核弹速度
            # 我的参数
            configmap["myf_master"]["life_value"] = 700 # 生命值
            configmap["myf_master"]["shield_value"] = 300 # 护盾
            configmap["myf_master"]["shield_recharge_step"] = 3 # 护盾充能间隔，越小越快
            configmap["myf_master"]["super_bullet"]["score_cast"] = 100 # 核弹消耗
        elif args.level == "xx":
            # UFO 参数
            configmap["ufo_master"]["life_value"] = 50000 # 生命值
            configmap["ufo_master"]["shield_value"] = 2000 # 护盾
            configmap["ufo_master"]["shield_recharge_step"] = 2 # 护盾充能间隔，越小越快
            configmap["ufo_master"]["super_bullet"]["score_cast"] = 50 # 核弹消耗
            configmap["ufo_master"]["super_bullet"]["speed"] = 4 # 核弹速度
            # 我的参数
            configmap["myf_master"]["life_value"] = 700 # 生命值
            configmap["myf_master"]["shield_value"] = 300 # 护盾
            configmap["myf_master"]["upgrade_cast"] = 200 # 升级基础点数 1个升级点需要5点能量点            
            configmap["myf_master"]["shield_recharge_step"] = 5 # 护盾充能间隔，越小越快
            configmap["myf_master"]["super_bullet"]["score_cast"] = 200 # 核弹消耗:
        elif args.level == "xxx":
            # UFO 参数
            configmap["ufo_master"]["life_value"] = 50000 # 生命值
            configmap["ufo_master"]["shield_value"] = 5000 # 护盾
            configmap["ufo_master"]["shield_recharge_step"] = 1 # 护盾充能间隔，越小越快
            configmap["ufo_master"]["bullet_speed"] = 9 # 普通炮弹速度，越大越快
            configmap["ufo_master"]["super_bullet"]["score_cast"] = 50 # 核弹消耗
            configmap["ufo_master"]["super_bullet"]["speed"] = 5 # 核弹速度
            configmap["ufo_slave"]["min_limit"] = 3
            # 我的参数
            configmap["myf_master"]["life_value"] = 700 # 生命值
            configmap["myf_master"]["shield_value"] = 300 # 护盾
            configmap["myf_master"]["upgrade_cast"] = 300 # 升级基础点数 1个升级点需要5点能量点
            configmap["myf_master"]["shield_recharge_step"] = 5 # 护盾充能间隔，越小越快
            configmap["myf_master"]["super_bullet"]["score_cast"] = 500 # 核弹消耗:
            configmap["myf_master"]["super_bullet"]["fire_delay"] = 100 # 核弹延迟
            configmap["myf_master"]["super_bullet"]["acc_distance_1"] = 400 # 核弹一段加速距离
            configmap["myf_master"]["super_bullet"]["acc_distance_2"] = 200 # 核弹二段加速距离
            

            
            
            
        if args.resolution == "1080":
            configmap["display_width"] = 1920
            configmap["display_height"] = 1080
        elif args.resolution == "900":
            configmap["display_width"] = 1600
            configmap["display_height"] = 900
        elif args.resolution == "720":
            configmap["display_width"] = 1280
            configmap["display_height"] = 720

        from spacedefense.game import main
        main()
    except Exception as e:
        print(f"Error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

