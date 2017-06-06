
import pygame
from sys import exit
from pygame.locals import *
from GameClass import*
import random


#初始化
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#设置游戏屏幕初始化大小
pygame.display.set_caption('PyGame')#设置标题

# 载入游戏音乐
bulletSound = pygame.mixer.Sound('resources/sound/bullet.wav')#设置子弹声音
enemyShootedSound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')#敌军被击中声音
gameOverSound = pygame.mixer.Sound('resources/sound/game_over.wav')
bulletSound.set_volume(0.3)
enemyShootedSound.set_volume(0.3)
gameOverSound.set_volume(0.3)
pygame.mixer.music.load('resources/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
# If the loops is -1 then the music will repeat indefinitely
#The starting position argument controls where in the music the song starts playing
#play(loops=0, start=0.0) -> None
pygame.mixer.music.set_volume(0.25)

# 载入背景
background = pygame.image.load('resources/image/background.png').convert()
gameOver = pygame.image.load('resources/image/gameover.png')

fileName = 'resources/image/shoot.png'
planeImg = pygame.image.load(fileName)#跟上面那句有什么区别?

#设置玩家参数
playerRect = []
playerRect.append(pygame.Rect(0, 99, 102, 126))   #玩家图片
playerRect.append(pygame.Rect(165, 360, 102, 126))
playerRect.append(pygame.Rect(165, 234, 102, 126))     # 玩家爆炸精灵图片区域
playerRect.append(pygame.Rect(330, 624, 102, 126))
playerRect.append(pygame.Rect(330, 498, 102, 126))
playerRect.append(pygame.Rect(432, 624, 102, 126))

#Rect(left, top, width, height) -> Rect
#Rect((left, top), (width, height)) -> Rect
#Rect(object) -> Rect

playerPos = [200, 600]#初始化位置
player = Player(planeImg, playerRect, playerPos) #init一个玩家

# 定义子弹对象使用的surface参数
bulletRect = pygame.Rect(1004, 987, 9, 21)
bulletImg = planeImg.subsurface(bulletRect)
#create a new surface that references its parent

#定义敌机使用surface相关参数
enemyRect_1 = pygame.Rect(534, 612, 57, 43)
enemyImg_1 = planeImg.subsurface(enemyRect_1)

enemyShootedImg_1 = []#坠毁图片序列表, 敌机坠毁过程图片
enemyShootedImg_1.append(planeImg.subsurface(pygame.Rect(267, 347, 57, 43)))
enemyShootedImg_1.append(planeImg.subsurface(pygame.Rect(873, 697, 57, 43)))
enemyShootedImg_1.append(planeImg.subsurface(pygame.Rect(267, 296, 57, 43)))
enemyShootedImg_1.append(planeImg.subsurface(pygame.Rect(930, 697, 57, 43)))

enemies_1 = pygame.sprite.Group()

enemiesShooted = pygame.sprite.Group()

shootFrequency = 0#射击频率
enemyFrequency = 0#敌机出现频率

playerDownIndex = 16 #???

score = 0
clock = pygame.time.Clock()

running = True

while(running):
    clock.tick(90) #控制游戏最大帧率为60

    #控制发射子弹频率, 并发射子弹
    if not player.isHit:
        if shootFrequency % 15 == 0:
            bulletSound.play()
            player.shoot(bulletImg)
        shootFrequency += 1
        if shootFrequency >= 15:
            shootFrequency = 0

    #控制敌机生成频率
    if enemyFrequency % 50 == 0:
        enemyPos_1 = [random.randint(0, SCREEN_WIDTH - enemyRect_1.width), 0] #随机产生敌机出现位置(x轴), y坐标固定于0
        enemy_1 = Enemy(enemyImg_1, enemyShootedImg_1, enemyPos_1)
        enemies_1.add(enemy_1)
    enemyFrequency += 1
    if enemyFrequency >= 100:
        enemyFrequency = 0

    for bullet in player.bullets: #子弹列表进行循环, 若存在, 判断是否超出位置
        bullet.move() #调用子弹移动, 若移动后出了边框, 那么移除子弹
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)


    #移动敌机, 超出范围删除
    for enemy in enemies_1:
        enemy.move()
        if pygame.sprite.collide_circle(enemy, player):#如果敌机与玩家出现碰撞
            enemiesShooted.add(enemy) #将坠毁敌机加入敌机列表
            enemies_1.remove(enemy)
            player.isHit = True
            gameOverSound.play()
            break

        if enemy.rect.top > SCREEN_HEIGHT:
            enemies_1.remove(enemy)


    # 将被击中的敌机对象添加到击毁敌机Group中, 用来渲染击毁动画
    enemiesShooted_1 = pygame.sprite.groupcollide(enemies_1, player.bullets, 1, 1)#用于两个集合处理碰撞
    for enemyShoot in enemiesShooted_1:
        enemiesShooted.add(enemyShoot)

    # 绘制背景
    screen.fill(0)
    screen.blit(background, (0, 0))
    #blit()
    #draw one image onto another
    #blit(source, dest, area=None, special_flags = 0) -> Rect

    # 绘制玩家飞机
    if not player.isHit:
        screen.blit(player.image[player.imgIndex], player.rect)
        player.imgIndex = shootFrequency // 8
        #更换图片索引
        player.imgIndex = shootFrequency // 8 #返回整数部分, shootFrquence 最高为15

    else:
        player.imgIndex = playerDownIndex // 8
        screen.blit(player.image[player.imgIndex], player.rect)#在屏幕中绘制
        playerDownIndex += 1
        if playerDownIndex > 47:
            running = False

    # 绘制击毁动画, 这是每一帧循环一次还是?
    for enemyShoot in enemiesShooted:
        if enemyShoot.downIndex == 0 :
            enemyShootedSound.play()
        if enemyShoot.downIndex > 7:
            enemiesShooted.remove(enemyShoot)
            score += 1000
            continue

        screen.blit(enemyShoot.shootedImg[enemyShoot.downIndex // 2], enemyShoot.rect)
        enemyShoot.downIndex += 1
        #坠毁过程循环

    # 绘制子弹和敌机
    player.bullets.draw(screen)
    enemies_1.draw(screen)

    # 绘制得分
    scoreFont = pygame.font.Font(None, 36)
    scoreText = scoreFont.render(str(score), True, (128, 128, 128))#字体渲染

    textRect = scoreText.get_rect()
    textRect.topleft = [10, 10]#设置位置
    screen.blit(scoreText, textRect)

    #更新屏幕
    pygame.display.update()

    for event in pygame.event.get():#事件获取
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    keyPressed = pygame.key.get_pressed()#监听键盘事件

    if not player.isHit:
        if keyPressed[K_w] or keyPressed[K_UP]:
            player.moveUp()
        if keyPressed[K_s] or keyPressed[K_DOWN]:
            player.moveDown()
        if keyPressed[K_a] or keyPressed[K_LEFT]:
            player.moveLeft()
        if keyPressed[K_d] or keyPressed[K_RIGHT]:
            player.moveRight()


#while循环结束
font = pygame.font.Font(None, 48)
text = font.render('Score :' + str(score), True, (255, 0, 0))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(gameOver, (0, 0))
screen.blit(text, textRect)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()


















