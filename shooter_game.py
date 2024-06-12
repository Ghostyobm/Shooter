from pygame import *
import random 


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65 , 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.fire_rate = 0
    def update(self):
        keys = key.get_pressed()
        self.fire_rate -= 1
        if keys[K_d] and self.rect.x < 1000 - 65:
            self.rect.x += 10
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= 10
        if keys[K_SPACE]:
            self.fire()
    def fire(self):
        if self.fire_rate <= 0:
            bullets.add(Bullet('bullet.png', self.rect.centerx, self.rect.top, 2))
            kick = mixer.Sound('fire.ogg')
            kick.play()
            self.fire_rate = 30
        

class Enemy(GameSprite):
    def update(self):
        global fall_enemy
        self.rect.y += self.speed
        if self.rect.y > 1000:
            fall_enemy += 1
            self.rect.y = random.randint(-80, -70)
            self.rect.x = random.randint(0, 600)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

font.init()

mixer.init()

FPS = 60
clock = time.Clock()
fall_enemy = 0
score_enemy = 0
health = 0

window = display.set_mode((1000, 800))
display.set_caption('Space War')
background = transform.scale(image.load("galaxy.jpg"), (1000, 800))

mixer.music.load("space.ogg")
mixer.music.play()

player = Player("rocket.png", 350, 700, 5)

enemys = sprite.Group()
for i in range(5):
    enemys.add(Enemy("ufo.png", random.randint(0, 600), random.randint(-80, -70), 2))
font1 = font.SysFont("Arial", 100)
check = font1.render('Счетчик:', 1, (100, 100, 150))
font2 = font.SysFont("Arial", 100)
lose = font2.render('Пропущено:' + str(fall_enemy), 1, (100, 100, 150))

bullets = sprite.Group()

game = True
finish = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if finish:
        pass
    else:
        check = font1.render('Счетчик:'+ str(score_enemy), 1, (100, 100, 150))
        lose = font2.render('Пропущено:' + str(fall_enemy), 1, (100, 100, 150))
        window.blit(background, (0, 0))
        window.blit(check, (0, 0))
        window.blit(lose, (0, 60))

        if score_enemy >= 5:
            finish = True
            finish1 =  font1.render('You Win!', 1, (100, 100, 150))
            window.blit(finish1, (350, 500))

        if fall_enemy >= 3:
            finish = True
            lose1 = font1.render('You lose!', 1, (100, 100, 150))
            window.blit(lose1, (350, 500))
        
        enemy = sprite.groupcollide(enemys, bullets, True, True)
        sprite_collide = sprite.spritecollide(player, enemys, True)

        for i in enemy:
            i.kill()
            score_enemy += 1
            enemys.add(Enemy("ufo.png", random.randint(0, 600), random.randint(-80, -70), 2))

        player.update()
        player.reset()
        enemys.update()
        bullets.update()
        enemys.draw(window)
        bullets.draw(window)

    clock.tick(FPS)
    display.update()