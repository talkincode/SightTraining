# SightTraining

这是一个为儿童视力训练创建的游戏项目， 由于某些原因， 某些医生建议和开具的视力训练游戏无法让孩子有兴趣， 视力训练成为一种对父母和孩子的折磨，于是一个让孩子感兴趣的视力训练项目诞生了。

SightTraining 将打造一个系列游戏， 这些游戏根据 CAM 光栅学的理论， 让孩子通过游戏来训练视力， 并保持持续的兴趣。

## SpaceDefense 太空保卫战

在浩瀚的宇宙中，隐藏着无数的奥秘与危险。一股来自远古的力量正在悄然觉醒，它们的目的只有一个——摧毁所有文明。宇宙之中的和平正面临前所未有的威胁，而你，作为太空保卫战系列的核心，被赋予了守卫家园、保护宇宙和平的重大任务。你将驾驶着自己的战斗机，与恶势力展开一场史诗般的太空战争。为了胜利，除了勇气和决心，你还需要策略和技巧。

### 游戏特色

- **精彩纷呈的太空战斗**：体验紧张刺激的太空对决，让玩家在宇宙的壮观景象中体验速度与激情的碰撞。
- **丰富多样的战舰选择**：游戏提供多种不同功能的战舰，每种战舰都有独特的技能和升级路径，玩家可以根据自己的战斗风格和需要进行选择和定制。
- **视觉和听觉的双重盛宴**：精心设计的游戏界面和背景音乐，将玩家完全拉入一个充满科幻风格的太空世界。
- **激励玩家的积分系统**：通过击败敌人和完成任务，玩家可以获得积分，用于升级和增强自己的战舰。
- **多样化的敌人与AI**：从侵略性的小型飞船到庞大的母舰，战斗中的敌人多种多样，AI的设计使得每一场战斗都充满挑战。
- **简单易懂，深度丰富**：易于上手的操作让玩家快速融入游戏，丰富的系统和策略让游戏长久玩下去依然充满乐趣。

### 操作说明

使用键盘 1，2，3，4，5，进行战斗操作， 左右键移动， 支持索尼 PS4/5手柄

- 1. 速射机炮，定向发射， 速度快，无法跟踪制导， 可升级最高6连发， 升级到一定级别可以同时发射干扰弹
- 2. 制导机炮，伤害高，自动跟踪敌人战机，无法定向发射，升级后可2连发
- 3. 发射干扰弹，伤害低， 但是可以拦截敌人普通炮弹
- 4. 呼叫战斗无人机， 可吸引敌人火力，为我方主舰掩护，伤害一般
- 5. 发射巡航导弹，高伤害， 并且产生冲击波，清除范围内所有炮弹， 两段加速，有较长的发射延时， 并且需要大量能量点数

### 敌人特色

一群高科技武装的外星侵略者， 他们的飞碟高生命值高护甲， 快速移动，发射光子炮弹， 母舰还会发射超级聚变弹， 产生范围冲击波，对范围内的单位持续伤害以及清除范围内炮弹

- 高强度的飞船船体， 难以直接攻击穿透
- 能量护盾可以快速充能，吸收大量攻击伤害
- 快速移动， 快速发射光子炮弹
- 母舰还会发射超级聚变弹， 两段加速，产生范围冲击波持续伤害
- 受伤严重时进入狂暴状态， 攻击加速，但伤害承受更多

### 攻略秘籍

- 只要对敌舰持续伤害就可以获得能量点数和升级点数
- 升级点数可以用于升级战舰， 能量点数可以用来呼叫无人战斗机和发射巡航导弹， 应尽量加速升级
- 随着升级，我方主舰伤害增加，护甲提升减少伤害承受
- 使用制导炮弹和巨变导弹可以拦截地方母舰聚变炮弹， 尽量避免被聚变炮弹攻击
- 保留足够能量点数，地方母舰狂暴后，我方可以呼叫大量无人战斗机作战
- 如果能阻止敌方母舰获得能量点数，地方母舰将无法派出作战飞碟以及发射聚变炮弹

### 玩家的使命

玩家将成为最后的防线，保护人类免受外来侵略者的摧毁。选择和升级你的战舰，发挥出色的操作技巧，在太空中穿梭，抵御一波又一波的敌人攻击。解锁新的武器和战舰，提高你的战斗能力，准备好在这场关乎命运的战争中成为英雄。

### 加入战斗吧

它不仅仅是一个游戏，它是一个关于勇气、智慧和牺牲的故事。只有最勇敢的战士才能存活下来，成为宇宙的保护者。太空保卫战等你加入，一起守卫我们共同的家园，让和平再次回归这片星辰大海。让我们一起，向着遥远的宇宙深处，启航！

准备好了吗？勇士，让我们在『SpaceDefense 太空保卫战』中书写属于你的传奇吧！


## 快速开始

- pip 安装

```bash
pip install  SightTraining
```

- 源码安装

```bash
git clone git@github.com:talkincode/SightTraining.git
cd SightTraining

pip install .
```

安装完成后， 输入 `spacex01` 即可开始太空保卫战游戏


- 参数说明 

```bash
options:
  -h, --help            显示帮助信息
  -D, --debug           Debug 模式.
  -t, --train           视力训练模式， CAM 光栅风格轮换.
  -f, --fullscreen      全屏模式.
  -r {1080,900,720}, --resolution {1080,900,720}  
                        设置游戏分辨率。
  -l {x,xx,xxx}, --level {x,xx,xxx}
                        设置游戏难度级别
```

比如要挑战最高难度， 运行命令 `spacex01 -l=xxx`

> 注意较高的分辨率需要更好的硬件支持
