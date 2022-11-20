#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer
w = display.set_mode((700,500))
display.set_caption('shuter')
bg = transform.scale(image.load('galaxy.jpg'),(700,500))
c = time.Clock()
r = True
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
f = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, size_x, size_y, p_speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image),(size_x,size_y))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        w.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameSprite):
    def update(self):
        kp = key.get_pressed()
        if kp[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if kp[K_RIGHT] and self.rect.x<630:
            self.rect.x += self.speed
    def fire(self):
        bu = Bullet('bullet.png', self.rect.centerx, self.rect.top,50,100,10)
        b.add(bu)
lost = 0
max_lost = 3
score = 0 
max_score = 10
life = 3
rel_time = False
pule = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 750 - 80)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        global score
        if self.rect.y < 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(80, 750 - 80)
            self.rect.y = 0
font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial',80)

p = Player('rocket.png',5,500 - 100,80, 100, 10)
en = sprite.Group()
for i in range(6):
    ene = Enemy('ufo.png', randint(80, 750 - 80), -40, 80, 50, randint(1,2))
    en.add(ene)
b = sprite.Group()
ast  = sprite.Group()
for i in range(3):
    aster = Asteroid('asteroid.png', randint(80, 750 - 80), -40, 100, 100, randint(1,2))
    ast.add(aster)
finish = False
goal = 10
win = font2.render('YOU WIN', True, (255,215,0))
lose = font2.render('YOU LOSE', True, (0,170,220))
while r:
    for e in event.get():
        if e.type == QUIT:
            r = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if pule < 5 and rel_time== False:
                    pule = pule + 1
                    p.fire()
                    f.play()
                if pule >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        w.blit(bg,(0,0))
        p.update()
        p.reset()
        b.update()
        b.draw(w)
        en.update()
        en.draw(w)
        ast.update()
        ast.draw(w)
        tl = font1.render('Пропущено: ' + str(lost), 1, (3, 250, 200))
        t = font1.render('Счет: ' + str(score), 1, (3, 250, 200))
        l = font1.render('Жизни: ' + str(life), 1, (3, 250, 200))
        w.blit(tl, (10, 20))
        w.blit(t, (10, 70))
        w.blit(l, (10, 120))
        if rel_time == True:
            now_time= timer()
            if now_time - last_time <2:
                rel = font1.render('wait, reload...', 1, (100,0,0))
                w.blit(rel, (260,420))
            else:
                pule = 0
                rel_time = False
        co = sprite.groupcollide(en, b, True, True)
        for t in co:
            score = score + 1
            ene = Enemy('ufo.png', randint(80, 750 - 80), -40, 80, 50, randint(1,2))
            en.add(ene)
        if sprite.spritecollide(p,ast, True) or sprite.spritecollide(p,en, True) or lost >= max_lost:
            aster = Asteroid('asteroid.png', randint(80, 750 - 80), -40, 100, 100, randint(1,2))
            ast.add(aster)
            ene = Enemy('ufo.png', randint(80, 750 - 80), -40, 80, 50, randint(1,2))
            en.add(ene)
            life = life - 1
        if life <= 0:
            finish = True
            w.blit(lose, (200, 200))
        if score >= max_score:
            finish = True
            w.blit(win, (200, 200))
    display.update()
    c.tick(60)