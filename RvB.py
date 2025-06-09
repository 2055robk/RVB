import random
from os import path
import pygame

pygame.init()

infoObject = pygame.display.Info()

HEIGHT = 850
WIDTH = 1500
FPS = 60  #

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_RED = (130, 7, 7)
DARK_GREEN = (7, 130, 7)
DARK_BLUE = (7, 7, 130)
LIGHT_RED = (255, 128, 128)
LIGHT_GREEN = (128, 255, 128)
LIGHT_BLUE = (128, 128, 255)
LIGHT_GREY = (192, 192, 192)
GREY = (128, 128, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RvB")
src_dir = path.join(path.dirname(__file__), 'image and sounds')
background = pygame.image.load(path.join(src_dir, 'Background.png')).convert()
background_rect = background.get_rect()
laser_shoot_enemy_snd = pygame.mixer.Sound(path.join(src_dir, 'laser_shoot_1.wav'))
laser_shoot_enemy_snd.set_volume(0.1)
laser_shoot_ours_snd = pygame.mixer.Sound(path.join(src_dir, 'laser_shoot_2.wav'))
laser_shoot_ours_snd.set_volume(0.1)
you_are_hit_snd = pygame.mixer.Sound(path.join(src_dir, 'if_you_are_hit_snd.wav'))

menu_music = path.join(src_dir, 'menu_music.mp3')
game_music = path.join(src_dir, 'game_music.wav')
boss_music = path.join(src_dir, 'boss_music.wav')


class FullscreenButton(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'Fullscreen_button.png')).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (35, 35)
        self.is_fullscreen = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, column, n, n_max):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'enemy_1.png')).convert()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH + 100, HEIGHT / n_max * n)
        self.is_start = True
        self.column = column
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 3000)  # 1000 ms = 1 sec
        self.HP = 100

    def update(self):
        if self.is_start:
            self.rect.x -= 1
            if self.rect.x < WIDTH - 100 * self.column:
                self.is_start = False
                self.last_shoot = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_shoot > self.shoot_delay and not self.is_start:
            self.last_shoot = pygame.time.get_ticks()
            laser = EnemyLaser(self.rect.centerx - 50, self.rect.centery)
            all_sprites.add(laser)
            enemy_laser.add(laser)
            laser_shoot_enemy_snd.play()


class EnemyBosses(pygame.sprite.Sprite):
    def __init__(self, column, n, n_max):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'enemy_Red_boss_level1.png')).convert()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH + 100, HEIGHT / n_max * n)
        self.column = column
        self.is_start = True
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 3000)  # 1000 ms = 1 sec
        self.HP = 250
        self.speed = 1

    def update(self):
        if not self.is_start:
            self.rect.y += self.speed
            if self.rect.top == 0:
                self.speed *= -1
            if self.rect.bottom == HEIGHT:
                self.speed *= -1
        if self.is_start:
            self.rect.x -= self.speed
            if self.rect.x < WIDTH - 100 * self.column:
                self.is_start = False
                self.last_shoot = pygame.time.get_ticks()
        if pygame.time.get_ticks() - self.last_shoot > self.shoot_delay and not self.is_start:
            self.last_shoot = pygame.time.get_ticks()
            laser = EnemyLaser(self.rect.centerx - 50, self.rect.centery - 25)
            all_sprites.add(laser)
            enemy_laser.add(laser)
            laser = EnemyLaser(self.rect.centerx - 50, self.rect.centery)
            all_sprites.add(laser)
            enemy_laser.add(laser)
            laser = EnemyLaser(self.rect.centerx - 50, self.rect.centery + 25)
            all_sprites.add(laser)
            enemy_laser.add(laser)
            laser_shoot_enemy_snd.play()


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'Blue-laser.png')).convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (40, 7))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 8

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()


class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'Red-laser(weak).png')).convert()
        self.image = pygame.transform.rotate(self.image, 90)
        self.image = pygame.transform.scale(self.image, (40, 7))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = -8

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.image.load(path.join(src_dir, 'meteorBrown_big2.png')).convert()
        self.image_orig = pygame.transform.scale(self.image_orig, (100, 100))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rot = 0
        self.rot_speed = random.randint(-8, 8)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(WIDTH + 50, WIDTH + 100),
                            random.randint(0, HEIGHT))
        self.speed_x = random.randint(2, 3)
        self.speed_y = random.randint(-1, 1)
        self.last_rotate = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x -= self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0:
            self.kill()

    def rotate(self):
        if pygame.time.get_ticks() - self.last_rotate > 5:
            self.last_rotate = pygame.time.get_ticks()
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


class MeteorController:
    def __init__(self):
        self.spawn_delay = random.randint(10000, 15000)
        self.last_spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.last_spawn_time > self.spawn_delay:
            self.last_spawn_time = pygame.time.get_ticks()
            meteor = Meteor()
            all_sprites.add(meteor)
            meteors.add(meteor)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(src_dir, 'player_ship.png')).convert()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.image = pygame.transform.rotate(self.image, 90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (285, HEIGHT / 2.2)
        self.speed = 6
        self.health = 100
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 500  # 1000 ms = 1 sec

    def update(self):
        is_shoot = True
        for enemie in enemies:
            if enemie.is_start:
                is_shoot = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed - 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed - 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed - 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed - 1
        if keys[pygame.K_SPACE] and is_shoot:
            self.shoot()

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH / 3:
            self.rect.right = WIDTH / 3

    def shoot(self):
        if pygame.time.get_ticks() - self.last_shoot > self.shoot_delay:
            self.last_shoot = pygame.time.get_ticks()
            laser = Laser(self.rect.centerx + 51, self.rect.centery - 15)
            all_sprites.add(laser)
            lasers.add(laser)
            laser = Laser(self.rect.centerx + 51, self.rect.centery + 13)
            all_sprites.add(laser)
            lasers.add(laser)
            laser_shoot_ours_snd.play()


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, width, height)
        self.width = width
        self.height = height
        self.text = text
        self.hover_color = hover_color
        self.color = color
        self.active = False
        self.font = pygame.font.Font(None, 32)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.active = True
        else:
            self.active = False
        return self.active

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, 1, BLACK)
        screen.blit(text_surface, (self.x + self.width / 2 - text_surface.get_width() / 2,
                                   self.y + self.height / 2 - text_surface.get_height() / 2))


class Menu:
    def __init__(self):
        self.buttons = [
            Button(WIDTH / 2 - 100, 100, 200, 50, "Play", RED, LIGHT_RED),
            Button(WIDTH / 2 - 100, 200, 200, 50, "Levels", GREEN, LIGHT_GREEN),
            Button(WIDTH / 2 - 100, 300, 200, 50, "Settings", GREY, LIGHT_GREY),
            Button(WIDTH / 2 - 100, 400, 200, 50, "Quit", BLUE, LIGHT_BLUE)
        ]
        self.state = "MENU"

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_click(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.active:
                    if button.text == "Play":
                        self.state = "GAME"
                    elif button.text == "Quit":
                        pygame.quit()

class YouWonMenu:
    def __init__(self):
        self.buttons = [
            Button(WIDTH / 2 - 100, 100, 200, 50, "Next Level", RED, LIGHT_RED),
            Button(WIDTH / 2 - 100, 200, 200, 50, "Menu", BLUE, LIGHT_BLUE),
        ]
        self.font = pygame.font.Font(None, 32)
        pygame.mixer.music.load(path.join(src_dir, 'menu_music.mp3'))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def draw(self, screen):

        text_surface = self.font.render("You Won!", 1, WHITE)
        screen.blit(text_surface, ( WIDTH / 2 - text_surface.get_width() / 2, 300))

        for button in self.buttons:
            button.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_click(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.active:
                    if button.text == "Next Level":
                        m.state = "GAME"
                    elif button.text == "Menu":
                        m.state = "MENU"

class Game:
    def __init__(self, level):
        self.player = Player()
        self.state = "GAME"
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.score = 0
        self.high_score = 0
        self.level = level
        self.wave = 1
        self.meteor_controller = MeteorController()
        all_sprites.add(self.player)
        self.fullscreen_button = FullscreenButton()
        all_sprites.add(self.fullscreen_button)
        self.level_builder()

    def check_enemies(self):
        if len(enemies) == 0:
            self.wave += 1
            self.level_builder()

    def level_builder(self):
        global current_level
        if self.level == 1:
            if self.wave == 1:
                for position in range(1, 2):
                    enemy = Enemy(1, position, 2)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif self.wave == 2:
                for position in range(1, 4):
                    enemy = Enemy(1, position, 4)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif self.wave == 3:
                for position in range(1, 6):
                    enemy = Enemy(1, position, 6)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif self.wave == 4:
                enemy = EnemyBosses(2, 1, 2)
                all_sprites.add(enemy)
                enemies.add(enemy)
            else:
                m.state = "YOU WON"
                current_level += 1
        elif self.level == 2:
            if self.wave == 1:
                for position in range(1, 5):
                    enemy = Enemy(1, position, 5)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif self.wave == 2:
                for position in range(1, 7):
                    enemy = Enemy(1, position, 7)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            elif self.wave == 3:
                for position in range(1, 7):
                    enemy = Enemy(1, position, 7)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                for position in range(1, 4):
                    enemy = Enemy(2, position, 4)
                    all_sprites.add(enemy)
                    enemies.add(enemy)
            else:
                m.state = "YOU WON"
                current_level += 1


    def handle_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                m.state = "MENU"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.fullscreen_button.rect.collidepoint(event.pos):
                    if not self.fullscreen_button.is_fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        infoObject = pygame.display.Info()
                        global HEIGHT, WIDTH
                        HEIGHT = infoObject.current_h
                        WIDTH = infoObject.current_w
                        self.fullscreen_button.is_fullscreen = True
                        self.player.speed /= 2
                    else:
                        HEIGHT = 850
                        WIDTH = 1500
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        self.fullscreen_button.is_fullscreen = False
                        self.player.speed *= 3

    def check_collision(self):
        hits = pygame.sprite.spritecollide(self.player, meteors, True)
        if hits:
            self.player.health -= 75
            if self.player.health <= 0:
                self.player.kill()
                m.state = "MENU"
        hits = pygame.sprite.spritecollide(self.player, enemy_laser, True)
        if hits:
            self.player.health -= 25
            if self.player.health <= 0:
                self.player.kill()
                m.state = "MENU"
            else:
                you_are_hit_snd.play()
        pygame.sprite.groupcollide(lasers, meteors, True, True)
        hits = pygame.sprite.groupcollide(enemies, lasers, False, True)
        for enemy, hit_lases in hits.items():
            enemy.HP -= 50 * len(hit_lases)
            if enemy.HP <= 0:
                enemy.kill()

def play_music(music_path, loop=True, volume=0.2):
    global current_music
    if current_music == music_path:
        return
    pygame.mixer.music.stop()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(volume)
    if loop == True:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.play(1)
    current_music = music_path

lasers = pygame.sprite.Group()
meteors = pygame.sprite.Group()
enemy_laser = pygame.sprite.Group()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
current_level = 1
current_music = None
YOU_WON = YouWonMenu()
game = Game(current_level)
m = Menu()

while True:
    if m.state == "MENU":
        for event in pygame.event.get():
            m.handle_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
        play_music(menu_music)
        screen.fill(BLACK)
        m.draw(screen)
        pygame.display.flip()
    elif m.state == "GAME":

        for event in pygame.event.get():
            game.handle_events(event)
        game.check_collision()

        game.check_enemies()
        play_music(game_music)

        if m.state == "MENU" or m.state == "YOU WON":
            all_sprites = pygame.sprite.Group()
            meteors = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            lasers = pygame.sprite.Group()
            enemy_laser = pygame.sprite.Group()
            game = Game(current_level)
            continue

        game.meteor_controller.update()
        all_sprites.update()
        screen.fill(BLACK)
        screen.blit(background, background_rect)
        all_sprites.draw(screen)
        pygame.display.flip()

    elif m.state == "YOU WON":
        for event in pygame.event.get():
            YOU_WON.handle_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill(BLACK)
        YOU_WON.draw(screen)
        pygame.display.flip()
# trhu4eri8rt9itrokgfvjnghju7ygvjn vvbjmvb jnfcheditedjgvnj n  jn jnfvjrfujedyhfbgfc
# record 32 mistakes(RED)
