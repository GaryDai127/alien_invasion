import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """管理游戏资源和行为的类"""
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        # 创建子弹编组
        self.bullets = pygame.sprite.Group()
        # 创建外星人群组
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            # print(len(self.bullets))
            self._update_screen()

            # 设置时钟频率
            self.clock.tick(60)

    def _check_events(self):
        """侦听键盘和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _fire_bullet(self):
        """创建一颗子弹，加入编组"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除已消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()
        self._check_bullet_alien_collisions()

        # 当前舰队被清理后，清除子弹并生成新的舰队
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _check_fleet_edges(self):
        """在有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整个外星舰队向下移动，并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """边缘检查，并更新外星舰队中的所有外星人"""
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人与飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")

    def _create_fleet(self):
        """创建一个外星舰队"""
        # 创建一个外星人，不断添加，直到没有空间为止
        # 外星人的间距为一个外星人的宽度 和 高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x,current_y = alien_width, alien_height

        while self.settings.screen_height - current_y > 5 * alien_height:
            while self.settings.screen_width - current_x > 2 * alien_width:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一行后，重置 x 且更新 y
            current_x = alien_width
            current_y += 2 * alien_height
    
    def _create_alien(self, x_position, y_position):
        """创建一个外星人，并将其放在当前行中"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if not self.aliens:
            # 删除现有的所有子弹，并创建一个新的外星舰队
            self.bullets.empty()
            self._create_fleet()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 重绘屏幕
        self.screen.fill(self.settings.bg_color)
        # 绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制飞船
        self.ship.blitme()
        # 绘制外星人
        self.aliens.draw(self.screen)
        # 显示最新绘制的屏幕
        pygame.display.flip()

    def _check_keydown_events(self, event):
        """响应按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应释放"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

if __name__ == "__main__":
    # 创建实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()