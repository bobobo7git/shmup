import pygame
import numpy as np
import os
import random
import math

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# 색 정의
WHITE = (255, 255, 255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SILVER = (192,192,192)
GREY = (222,222,222)

pygame.font.init()
pygame.mixer.init()



class Weapon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = loadImage('moon')
        self.rect = self.image.get_rect()
        self.inchant = 0
        self.dmg = 1
        self.delay = 0.5
        self.bnum = 1
        self.D = 100
        self.deg = 0
        
        
        

    def update(self):
        self.deg += 1
        self.rect.center =  ((Rmat(self.deg) @ np.array([self.D,self.D,1]).T  @ Tmat(player.rect.centerx,player.rect.centery).T ).T)[:2]
        
        

class Upgrades():
    def __init__(self):
        self.t1 = {1:'Move speed +1', 2: 'Bullet Lv.2', 3:'Shot delay -10%'}
        self.t2 = {1:'Move speed +2', 2: 'Bullet Lv.3',3:'Shot delay -20%'}
        self.t3 = {1:'Move speed +3',2:'Bullets LV.4',3:'Shot delay -30%'}
        self.add_wpn = {1: 'extra linear shot',2:'extra rotating shot',3:'god'}

        self.tier1 = []
        self.tier2 = []
        self.tier3 = []
        self.all = []

        self.tier1.append(self.t1)
        self.tier2.append(self.t2)
        self.tier3.append(self.t3)
        #self.tier3.append(self.add_wpn)

        for i in range(3):
            self.all.append(self.t1[i+1])
            self.all.append(self.t2[i+1])
            self.all.append(self.t3[i+1])
            #self.all.append(self.add_wpn[i+1])

        
        

        
        
        
        

   

class Game(Upgrades):
    def __init__(self,screen):
        super().__init__()
        self.score = 0
        self.money = 0
        self.playing = True
        self.font16 = pygame.font.SysFont('FixedSys', 16, False, False)
        self.font24 = pygame.font.SysFont('FixedSys', 24, False, False)
        self.font36 = pygame.font.SysFont('FixedSys', 36, True, False)
        self.font56 = pygame.font.SysFont('FixedSys', 56, True, False)
        self.title_store = self.font36.render("Select your upgrade", True, WHITE)
        self.desc_store = self.font24.render("Press 1,2,3 on keyboard to select", True, WHITE)
        self.money_store = self.font24.render(f"Money : {self.money}", True, WHITE)
        self.rnum = self.getRandomNum()
        
        self.storeTerm = [10,50,200,500,1000,2000]
        for i in range(1,10):
            self.storeTerm.append(2000 * i)
        
        
        self.tried = 0
        self.num = np.random.randint(1,10)
        self.num2 = np.random.randint(1,10)
        self.num3 = np.random.randint(1,10)
        self.timer = 0
        self.getop = False
        self.opt_txt = []
        self.opt_n = 0
        self.opt_input = 0
        
        

    def getOptions(self,mg):
        r = np.random.randint(1,4)
        i1 = np.random.randint(0,len(self.tier1))
        i2 = np.random.randint(0,len(self.tier2))
        i3 = np.random.randint(0,len(self.tier3))

        if mg == 1:
            return self.tier1[i1][r]
        if mg == 2:
            return self.tier2[i2][r]
        if mg == 3:
            return self.tier3[i3][r]

    def scoreUp(self,s):
        self.score += s
        self.money += s
        self.money_store = self.font24.render(f"Money : {self.money}", True, WHITE)

    def minigame(self, num, num2, num3):
        nums = []
        nums.append(num)
        nums.append(num2)
        nums.append(num3)
        nums.sort()
        print(nums)

        if nums[0] == nums[1] == nums[2]:
            return 3, '3 options'
        elif nums[0] == 1 and nums[1] == 2 and nums[2] == 3:
            return 2, '2 options'
        elif nums[0] == 2 and nums[1] == 3 and nums[2] == 4:
            return 2, '2 options'
        elif nums[0] == 3 and nums[1] == 4 and nums[2] == 5:
            return 2, '2 options'
        elif nums[0] == 4 and nums[1] == 5 and nums[2] == 6:
            return 2, '2 options'
        elif nums[0] == 5 and nums[1] == 6 and nums[2] == 7:
            return 2, '2 options'
        elif nums[0] == 6 and nums[1] == 7 and nums[2] == 8:
            return 2, '2 options'
        elif nums[0] == 7 and nums[1] == 8 and nums[2] == 9:
            return 2, '2 options'
        return 1, '1 optioins'

    def showStore(self):
        
        game.playing = False
        w = WINDOW_WIDTH /2 + 200   #600
        h = WINDOW_HEIGHT /2 + 50   #350
        l = 3
        margin = 30

        

        #Text controll for each status
        if self.tried < 3:
            self.desc_store = self.font24.render("Press 1,2,3 on keyboard to select", True, WHITE)
        elif self.tried <= 4:
            self.desc_store = self.font24.render(f"You got {self.opt_n}. press spacebar.", True, WHITE)
        else:
            self.desc_store = self.font24.render("Choose one!", True, WHITE)
            

        self.money_store = self.font24.render(f"Money : {self.money}", True, WHITE)

        

        #Define Rect
        rect = pygame.Rect(WINDOW_WIDTH/2 - w/2,WINDOW_HEIGHT/2-h/2,w,h)
        box_rect = pygame.Rect(WINDOW_WIDTH/2 - w/5/2,rect.bottom -w/5 - 100,w/5,w/5)
        box2_rect = pygame.Rect(box_rect.left - box_rect.w - 70,box_rect.top,w/5,w/5)
        box3_rect = pygame.Rect(box_rect.right + box_rect.w -50,box_rect.top,w/5,w/5)

        speed = 12
        
        
        if self.tried < 3:
            self.timer += speed
            if(self.timer >  FPS ):
                self.timer = 0
            elif FPS - self.timer < speed:
                self.timer = FPS
        else:
            self.timer += 1
            

        if self.tried <= 0:
            self.num += math.floor(self.timer / FPS)
            self.num2 += math.floor(self.timer / FPS)
            self.num3 += math.floor(self.timer / FPS)
            if self.num >= 10:
                self.num = 1
            if self.num2 >= 10:
                self.num2= 1
            if self.num3 >= 10:
                self.num3 = 1
            
        elif self.tried == 1:
            self.num += math.floor(self.timer / FPS)
            self.num3 += math.floor(self.timer / FPS)
            if self.num >= 10:
                self.num = 1
            if self.num3 >= 10:
                self.num3 = 1

        elif self.tried == 2:
            self.num3 += math.floor(self.timer / FPS)
            if self.num3 >= 10:
                self.num3 = 1
        elif self.tried == 3:
            if self.getop == False:
                self.opt_n = self.minigame(self.num,self.num2,self.num3)[0]
                for i in range(self.opt_n):
                    self.opt_txt.append(self.getOptions(i+1))
                    print(self.opt_txt, self.opt_n)
                
                self.getop = True
            self.tried +=1
        elif self.tried >= 5:   # minigame is over
            self.tried = 5
            
            
            

        


        #Draw window
        #pygame.draw.rect(screen,BLACK,rect,0)
        #pygame.draw.rect(screen,GREY,[rect.left + l, rect.top + l, w-l*2,h-l*2],0)
        screen.blit(loadImage('ug_ui'),rect)

        #Draw text
        screen.blit(self.title_store,[WINDOW_WIDTH/2 - self.title_store.get_width()/2,WINDOW_HEIGHT/2-rect.h/2 + margin])
        screen.blit(self.desc_store,[WINDOW_WIDTH/2 - self.desc_store.get_width()/2,WINDOW_HEIGHT/2-rect.h/2 + margin + self.title_store.get_height()])
        #screen.blit(self.money_store,[WINDOW_WIDTH/2 + w/2 - self.money_store.get_width() - margin,WINDOW_HEIGHT/2-rect.h/2
        # + margin * 5 + self.title_store.get_height() + self.desc_store.get_height()])
        
        #Draw box
        pygame.draw.rect(screen,WHITE,box_rect,3)
        pygame.draw.rect(screen,WHITE,box2_rect,3)
        pygame.draw.rect(screen,WHITE,box3_rect,3)

        #Fill box for each condition
        if self.tried <= 4:
            screen.blit(self.font56.render(str(self.num),True,WHITE),[box_rect.left + (box_rect.w - 28)/2, box_rect.top + (box_rect.h - 36)/2])
            screen.blit(self.font56.render(str(self.num2),True,WHITE),[box2_rect.left + (box2_rect.w - 28)/2, box2_rect.top + (box2_rect.h - 36)/2])
            screen.blit(self.font56.render(str(self.num3),True,WHITE),[box3_rect.left + (box3_rect.w - 28)/2, box3_rect.top + (box3_rect.h - 36)/2])
        
        elif self.getop :
            if self.opt_n == 1:
                txt2 = self.font24.render(self.opt_txt[0],False,WHITE)
                screen.blit(txt2,[box2_rect.centerx - txt2.get_width()/2, box2_rect.centery - txt2.get_height()/2])
            if self.opt_n == 2:
                txt2 = self.font24.render(self.opt_txt[0],False,WHITE)
                screen.blit(txt2,[box2_rect.centerx - txt2.get_width()/2, box2_rect.centery - txt2.get_height()/2])
                txt = self.font24.render(self.opt_txt[1],False,WHITE)
                screen.blit(txt,[box_rect.centerx - txt.get_width()/2, box_rect.centery - txt.get_height()/2])
            if self.opt_n == 3:
                txt2 = self.font24.render(self.opt_txt[0],False,WHITE)
                screen.blit(txt2,[box2_rect.centerx - txt2.get_width()/2, box2_rect.centery - txt2.get_height()/2])
                txt = self.font24.render(self.opt_txt[1],False,WHITE)
                screen.blit(txt,[box_rect.centerx - txt.get_width()/2, box_rect.centery - txt.get_height()/2])
                txt3 = self.font24.render(self.opt_txt[2],False,WHITE)
                screen.blit(txt3,[box3_rect.centerx - txt3.get_width()/2, box3_rect.centery - txt3.get_height()/2])

            if self.opt_input != 0:
                if self.opt_input <= self.opt_n:    
                    
                    self.doUpgrade()
                    self.exitStore()

    def getRandomNum(self):
        self.rnum = np.random.randint(0,101)
        if self.rnum < 50:
            rnum = 1
        elif self.rnum < 90:
            rnum = 2
        else:
            rnum = 3
        
        return rnum
        

    def exitStore(self):
        bullets.update()
        game.playing = True
        self.getop = False
        self.storeTerm.remove(self.storeTerm[0])
        self.rnum = self.getRandomNum()
        self.tried = 0
        self.timer = 0
        self.num = np.random.randint(1,10)
        self.num2 = np.random.randint(1,10)
        self.num3 = np.random.randint(1,10)
        self.opt_txt.clear()
        self.opt_input = 0
        

    def getGameState(self):
        if self.score >= self.storeTerm[0]:
            self.showStore()

    def getOptionInput(self,input):
        self.opt_input = input

    def doUpgrade(self):
        up = self.opt_txt[self.opt_input -1]
        for i in range(3):
            if up == list(self.t1.values())[i]:
                #print(list(self.t1.keys())[i])
                if i == 0:
                    player.dx += 1
                if i == 1 and player.bnum < 2:
                    player.bnum = 2
                if i == 2:
                    player.delay = player.delay * 0.9
                return

        for i in range(3):
            if up == list(self.t2.values())[i]:
                #print(list(self.t1.keys())[i])
                if i == 0:
                    player.dx += 2
                if i == 1 and player.bnum < 3:
                    player.bnum = 3
                if i == 2:
                    player.delay = player.delay * 0.8
                return

        for i in range(3):
            if up == list(self.t3.values())[i]:
                #print(list(self.t1.keys())[i])
                if i == 0:
                    player.dx += 3
                if i == 1 and player.bnum < 4:
                    player.bnum = 4
                if i == 2:
                    player.delay = player.delay * 0.7
                return

       


    
    
    

        
            
            

    



class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.radius = 1
        self.scale = 0.3
        self.image = loadImage('Player')
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (self.scale * self.size[0], self.scale * self.size[1]))
        self.rect = self.image.get_rect()
        self.speed = 0
        self.dx = 0
        self.life = 3
        self.rect.centerx = WINDOW_WIDTH/2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.fired = False
        self.timer = 0
        self.bnum = 1
        self.delay = 0.5
        self.shoot_snd = loadWav('shot')

        
        

    def update(self):
        self.speed = 0

        
        if self.fired:
            self.timer += 1
        if self.timer >= FPS * self.delay:
            self.timer = 0
            self.fired = False

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed = -8 - self.dx
        if keystate[pygame.K_RIGHT]:
            self.speed = 8 + self.dx
        if keystate[pygame.K_SPACE] and self.fired == False:
            self.shoot()
            self.fired = True
        
        
        self.rect.x += self.speed
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        self.shoot_snd.play()
        if self.bnum == 1:
            b = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            

            
        if self.bnum == 2:
            b = Bullet(self.rect.left + 10, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            
            b2 = Bullet(self.rect.right -10, self.rect.top)
            all_sprites.add(b2)
            bullets.add(b2)

        if self.bnum == 3:
            b = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            b2 = Bullet(self.rect.left, self.rect.top)
            all_sprites.add(b2)
            bullets.add(b2)
            b3 = Bullet(self.rect.right, self.rect.top)
            all_sprites.add(b3)
            bullets.add(b3)
        
        if self.bnum == 4:
            b = Bullet(self.rect.centerx -13, self.rect.top)
            all_sprites.add(b)
            bullets.add(b)
            b2 = Bullet(self.rect.centerx + 13, self.rect.top)
            all_sprites.add(b2)
            bullets.add(b2)
            b3 = Bullet(self.rect.left -15, self.rect.top)
            
            all_sprites.add(b3)
            bullets.add(b3)
            b4 = Bullet(self.rect.right +15, self.rect.top)
            
            all_sprites.add(b4)
            bullets.add(b4)
        
        
            

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if player.bnum == 1:
            self.image = loadImage('bullet0')
        if player.bnum == 2:
            self.image = loadImage('bullet1')
        if player.bnum >= 3:
            self.image = loadImage('bullet2')
        
        self.rect = self.image.get_rect()
        self.dy = 10
        self.deg = 0
        self.image = pygame.transform.rotate(self.image,self.deg)
        self.rect.centerx = x
        self.rect.bottom = y 
        
    def update(self):
        self.rect.y -= self.dy
 
        if self.rect.bottom <0:
            self.kill()
        if game.playing == False:
            self.kill()
        

        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, img = None):
        super().__init__()
        if img:
            self.image = loadImage(img)
        else:
            self.image = loadImage('enemy0')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.dx = np.random.randint(-200, 200) / 75.
        self.dy = random.randrange(1,3)

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.y > WINDOW_HEIGHT:
            self.rect.y = np.random.randint(-100,-40)
            self.rect.x = random.randrange(WINDOW_WIDTH - self.rect.width)
        if self.rect.x > WINDOW_WIDTH or self.rect.x +self.rect.width < 0:
            pass
            
def Rmat(deg):
    radian = np.deg2rad(deg)

    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c, -s, 0],[s, c, 0], [0, 0, 1]])
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H


def loadImage(img_name):
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets')

    img = pygame.image.load(os.path.join(assets_path, img_name + '.png'))
    
    return img

def loadWav(snd_name):
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets')

    snd = pygame.mixer.Sound(os.path.join(assets_path, snd_name + '.wav'))
    return snd

def loadMp3(snd_name):
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets')

    snd = pygame.mixer.Sound(os.path.join(assets_path, snd_name + '.mp3'))
    return snd

def genMob():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)



screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

all_sprites = pygame.sprite.Group()
player = Player()
#weapon = Weapon()
game = Game(screen)
all_sprites.add(player)
#all_sprites.add(weapon)

enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


def main():
    bgm0 = loadMp3('bgm0')
    bgm1 = loadMp3('bgm1')
    bgm2 = loadMp3('bgm2')
    

    pygame.display.set_caption("Shmup")
    
    clock = pygame.time.Clock()
    done = False   

    font = pygame.font.SysFont('FixedSys', 40, True, False)
    txt_score = font.render(f"Score : {game.score}", True, WHITE)
    timer = 0

    for i in range(8):
        genMob()

    bgm1 .play(-1,0,1000)
    

    while not done: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.exitStore()
                if event.key == pygame.K_SPACE:
                    if game.playing == False:
                        game.tried +=1
                if game.getop:
                    if event.key == pygame.K_1:
                        game.getOptionInput(1)
                    if event.key == pygame.K_2:
                        game.getOptionInput(2)
                    if event.key == pygame.K_3:
                        game.getOptionInput(3)

                        
        if game.playing:            
            timer += 1
        if (timer > 60):
            genMob()
            print('gen')
            timer = 0
        
        screen.fill(WHITE)
        screen.blit(loadImage('bg'),[0,0])

        game.getGameState()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            game.scoreUp(np.random.randint(1,5))
            genMob()

        hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
        if hits:
            done = True

        if game.playing:
            txt_score = font.render(f"Score : {game.score}", True, WHITE)
            all_sprites.update()
            #weapon.update()

            screen.blit(txt_score,(WINDOW_WIDTH/2 - txt_score.get_width()/2,0))
            all_sprites.draw(screen)

        else:
            screen.blit(txt_score,(WINDOW_WIDTH/2 - txt_score.get_width()/2,0))

        pygame.display.flip()

        clock.tick(FPS)

    return


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
