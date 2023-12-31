class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""
    def __init__(self):
        """初始化游戏的设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船的设置
        self.ship_speed = 10
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_speed = 3.5
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        # 允许未消失子弹的数量
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed = 8
        self.fleet_drop_speed = 8
        # fleet_direction -1 向左  1 向右
        self.fleet_direction = 1
