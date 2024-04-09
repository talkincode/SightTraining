import asyncio

async def main():
    from spacedefense_wasm.config import configmap
    # UFO 参数
    configmap["ufo_master"]["life_value"] = 50000  # 生命值
    configmap["ufo_master"]["shield_value"] = 2000  # 护盾
    configmap["ufo_master"]["shield_recharge_step"] = 2  # 护盾充能间隔，越小越快
    configmap["ufo_master"]["super_bullet"]["score_cast"] = 50  # 核弹消耗
    configmap["ufo_master"]["super_bullet"]["speed"] = 4  # 核弹速度
    # 我的参数
    configmap["myf_master"]["life_value"] = 700  # 生命值
    configmap["myf_master"]["shield_value"] = 300  # 护盾
    configmap["myf_master"]["upgrade_cast"] = 200  # 升级基础点数 1个升级点需要5点能量点
    configmap["myf_master"]["shield_recharge_step"] = 5  # 护盾充能间隔，越小越快
    configmap["myf_master"]["super_bullet"]["score_cast"] = 200  # 核弹消耗:
    from spacedefense_wasm.game import AsyncSpaceDefense
    await AsyncSpaceDefense().start_game()


if __name__ == "__main__":
    asyncio.run(main())
