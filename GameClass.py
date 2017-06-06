import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800

TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3

#######################################
#pygame.sprite.Sprite提供的一些比较有用的方法
#self.image …how the sprite look. It's a pygame surface, loaded or created, and you can use the pygame.draw commands on it.
#self.rect …very useful, get it with the command self.rect = self.image.get_rect() after you are done with creating self.image
#self.radius … useful for circular collision detection
#self.rect.center … if you have self.rect, use this to control the postion of a sprite on the screen.
#update(self, time): … a function (best with the passed seconds since last frame as argument) where you can calculate what the sprite should do, like moving, bouncing of walls etc
#kill(self) … very useful to destroy a sprite. the call inside the class is self.kill(), in the mainloop you would call snake222.kill()

#########################################


#子弹设计
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bulletImg, pos):
        pygame.sprite.Sprite.__init__(self)#调用父类的构造函数
        self.image = bulletImg
        self.rect = self.image.get_rect() #这里父类中应该定义了相应的方法
        self.rect.midbottom = pos #初始化中心位置
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed #移动轨迹子下而上

#玩家类设计, 飞机类,
#玩家只有以下集中行为, 发射子弹, 上.下, 左, 右, 移动
class Player(pygame.sprite.Sprite):
    def __init__(self, planeImg, planeRect, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [] #图片列表
        for i in range(len(planeRect)):
            self.image.append(planeImg.subsurface(planeRect[i]).convert_alpha())#???
        self.rect = planeRect[0] #大小以第一张图片为准
        self.rect.topleft = pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()#????
        self.imgIndex = 0 #选取第一张飞机图片,
        self.isHit = False #是否被击中

    def shoot(self, bulletImg):
        bullet = Bullet(bulletImg, self.rect.midtop)
        self.bullets.add(bullet)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed #向上移动

    def moveDown(self):
        if self.rect.down >= SCREEN_HEIGHT - self.rect.height:
            self.rect.down = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.down += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.right += self.speed


#敌人类, 有两种类型的图片, 一种正常情况下的图片, 另一种是被玩家击中后坠毁图片
class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyImg, shootedImg, pos): #shootedImg为图片list
        pygame.sprite.Sprite.__init__(self)
        self.image = enemyImg
        self.rect = self.image.get_rect()
        self.rect.topleft = pos #初始化位置, 已topleft为准, 其他也一样
        self.shootedImg = shootedImg
        self.speed = 2
        self.downIndex = 0 #????

    def move(self):
        self.rect.top += self.speed



#这里构造函数初始化时接受的物体图片, 而不是将图片作为类的变量