# Blessed Mind by 3A (S3AL Productions)
# Art from Kenney.nl



import pygame
import random
import os


WIDTH = 720
HEIGHT = 900
FPS = 60
#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)




font_name = pygame.font.match_font('arial')
def show_vi_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ChooChoo 'Em Up!", 64, WIDTH /2, HEIGHT /4 )  
    draw_text(screen, "Victory!!!", 56, WIDTH /2, HEIGHT /2)
    draw_text(screen, f'Final score = {score} x {max(combo_list)}  =  {score*max(combo_list)}',45, WIDTH /2, HEIGHT * 3/4)
    pygame.display.flip()
    waiting = True
    now = pygame.time.get_ticks()
    pygame.event.clear()
    while waiting:
        clock.tick(FPS)
        delay = 2000
        if pygame.time.get_ticks() - now > delay:
            screen.blit(background, background_rect)
            draw_text(screen, " Press a Key for Harder Difficulty... ", 40, WIDTH /2, HEIGHT * 1/2)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

                    
def show_go_screen(): 
    screen.blit(background, background_rect)
    draw_text(screen, "ChooChoo 'Em Up!", 64, WIDTH /2, HEIGHT /4 )  
    global death_player
    clock.tick(FPS) 
    waiting = True
    if death_player == 0  :
        while waiting:
            draw_text(screen, "Press a key to continue", 20, WIDTH /2, HEIGHT * 3/4)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYUP:
                    waiting = False
    if death_player > 0 :
        death_timer = pygame.time.get_ticks()
        draw_text(screen, "Game Over!", 18, WIDTH /2, HEIGHT * 2/4)
        draw_text(screen, "Restarting soon...", 18, WIDTH /2, HEIGHT * 3/4)
        pygame.display.flip()
        while waiting:
            if pygame.time.get_ticks() - death_timer >= 3000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYUP:
                        waiting = False
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, text_rect)
def health_bar(surf,x,y, pct):
    if pct <0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100) * BAR_LENGTH
    outline_rect = pygame.Rect(x,y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN, fill_rect)
    pygame.draw.rect(surf,WHITE, outline_rect, 2)
def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y 
        surf.blit(img, img_rect)

    
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 30
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = (WIDTH /2)
        self.rect.bottom = (HEIGHT-10)
        self.speedx = 0
        self.speedy=0
        self.shield = 100
        self.last_update = pygame.time.get_ticks()
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left= 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        global collision
        
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT - 10
            
        if self.power>= 2 and pygame.time.get_ticks()- self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
    def shoot(self):
        now = pygame.time.get_ticks()
        if now  - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power > 1:
                bullet1 = Bullets(self.rect.left, self.rect.centery)
                bullet2 = Bullets(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            else:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

    def Blink(self):
        current_time = pygame.time.get_ticks()
        global collision_time, delay
        if current_time > collision_time:
            global show_player_img
            show_player_img = False #SHow Blink
            collision_time = current_time + delay
            global blink_timer
            blink_timer = pygame.time.get_ticks()
        elif current_time <= collision_time and (pygame.time.get_ticks() - blink_timer) >= 200:
            show_player_img = True #Show Spaceship
    def hide(self):
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT + 200)
        self.hidden = True
        self.shield = 100
    def powerup(self):
        self.power +=1
        self.power_time = pygame.time.get_ticks()    
            
class Teleporters(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(teleporter_img)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius =  int(self.rect.width*.85/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange (50,500)
        self.last_update = pygame.time.get_ticks()
        self.spawn_timer = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 800
        self.spawn_delay = 5000
        self.speedy = 3
        self.speedx = random.randrange(-3,3)
    def update(self):
        self.teleport()
        self.shoot()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
    def teleport(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 1500:
            self.rect.x = WIDTH/2
            self.rect.y = -100
            self.last_shot = now 
            if now - self.last_update > 2000:        
                    self.last_update = now
                    self.rect.x = random.randrange(WIDTH - self.rect.width)
                    self.rect.y = random.randrange (50,500)
                    if self.rect.top < 0:
                        self.rect.top = 0
    def shoot(self):
        now = pygame.time.get_ticks()
        if now  - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1 = EnemyBullets(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet1)
            enemybullets.add(bullet1)
    def spawn(self):
        now = pygame.time.get_ticks()
        if now  - self.spawn_timer > self.spawn_delay: 
            self.spawn_timer = now
            t = Teleporters()
            all_sprites.add(t)
            mobs.add(t)
class Boss(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image =Boss_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius =  int(self.rect.width*.85/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH /2 
        self.rect.y =50
        self.last_update = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 350
        self.spawn_delay = 500000
        self.spawn_timer = -500000
        self.shoot_pattern_timer = pygame.time.get_ticks()
        self.shield = 5000
        self.speedy = random.randrange(1,2)
        self.speedx = random.randrange(-3,3)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.move()
        self.shoot(self.Random())
         
    def move(self):
        if self.rect.left <= 0:
            self.speedx = -self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
        if self.rect.top > 100:
            self.speedy = - self.speedy
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, Random):
        now = pygame.time.get_ticks()
        if now  - self.last_shot > self.shoot_delay and Random ==1:
            self.last_shot = now
            bullet1 = EnemyBullets(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet1)
            enemybullets.add(bullet1)
        elif now  - self.last_shot > self.shoot_delay and Random ==2:
            self.last_shot = now
            bullet1 = EnemyBullets(self.rect.left, self.rect.centery)
            bullet2 = EnemyBullets(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            enemybullets.add(bullet1)
            enemybullets.add(bullet2)
    def Random(self):
        random_choice = random.choice([1,2])
        return random_choice
                
    def spawn(self):
        now = pygame.time.get_ticks()
        if now  - self.spawn_timer > self.spawn_delay: 
            self.spawn_timer = now
            b = Boss()
            all_sprites.add(b)
            boss.add(b)        
class NormalMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(Normalmob_img)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius =  int(self.rect.width*.85/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange (50,500)
        self.last_update = pygame.time.get_ticks()
        self.spawn_timer = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 800
        self.spawn_delay = 2500
        self.speedy = random.randrange(1,3)
        self.speedx = random.randrange(-5,5)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.move()
        self.shoot()
    def move(self):
        if self.rect.left <= 0:
            self.speedx = -self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange (-100,-40)
            self.speedy = random.randrange(-3,3)
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self):
        now = pygame.time.get_ticks()
        if now  - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet1 = EnemyBullets(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet1)
            enemybullets.add(bullet1)
    def spawn(self):
        now = pygame.time.get_ticks()
        if now  - self.spawn_timer > self.spawn_delay: 
            self.spawn_timer = now
            n = NormalMob()
            all_sprites.add(n)
            mobs.add(n)   
                     
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius =  int(self.rect.width*.85/2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange (-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pygame.transform.rotate(self.image_orig, self.rot) 
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange (-100,-40)
            self.speedy = random.randrange(1,8)
class EnemyBullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
            global combo
            combo_list.append(combo)
            combo = 0    
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image =powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 6
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()
class Explosion(pygame.sprite.Sprite): 
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = meteor_explosion[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60
        
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(meteor_explosion[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = meteor_explosion[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
def Level():
    global level, mobs_killed, boss_spawn, b, show_timer
    if mobs_killed <60 :
        if mobs_killed >= 20 and mobs_killed < 35:
            if mobs_killed == 20:
                show_timer = pygame.time.get_ticks()
            elif pygame.time.get_ticks () - show_timer <= 2000:
                draw_text(screen, "Level 2", 64, WIDTH /2, HEIGHT /4 )     
            n.spawn()
        if mobs_killed >= 35 and mobs_killed < 60:
            n.spawn()
            t.spawn()
            if mobs_killed == 35:
                show_timer = pygame.time.get_ticks()
            elif pygame.time.get_ticks () - show_timer <= 2000:
                draw_text(screen, "Level 3", 64, WIDTH /2, HEIGHT /4)               
    elif mobs_killed >= 60:
        if mobs_killed == 60:
            show_timer = pygame.time.get_ticks()
        if pygame.time.get_ticks () - show_timer <= 2000:
            draw_text(screen, "Boss", 64, WIDTH /2, HEIGHT /4 )
            pygame.display.flip() 
        if (mobs_killed >= 60) and (boss_spawn ==1):
            b.spawn() 
            boss_spawn +=1     



#Start Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot'em up!")
clock = pygame.time.Clock()
game_folder = os.path.dirname(__file__)
show_timer = pygame.time.get_ticks()

#Set up all visual assets
img_folder = os.path.join(game_folder, 'Assets\Space Shooter\PNG')
sound_folder = os.path.join(game_folder, 'Assets\Space Shooter\Music')
player_img = pygame.image.load(os.path.join(img_folder, r'playerShip1_blue.png')).convert()
enemy_img = pygame.image.load(os.path.join(img_folder,r'Meteors/meteorBrown_Big1.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_folder,r'Lasers\laserRed01.png ')).convert()
bullet_player_img = pygame.image.load(os.path.join(img_folder,r'Lasers\laserBlue01.png ')).convert()
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(BLACK)
Boss_img = pygame.image.load(os.path.join(img_folder, r'blue1.png')).convert()
powerup_images = {}
powerup_images['gun'] = pygame.image.load(os.path.join(img_folder, r'Power-ups\bolt_gold.png'))
powerup_images['shield'] = pygame.image.load(os.path.join(img_folder, r'Power-ups\shield_gold.png'))

teleporter_img = []
for img in ['enemyBlack4.png', 'enemyGreen4.png', 'enemyRed4.png']:
    teleporter_img.append(pygame.image.load(os.path.join(img_folder, r'Enemies/'+img)))

Normalmob_img = []
for img in ['enemyBlack1.png', 'enemyGreen1.png', 'enemyRed1.png']:
    Normalmob_img.append(pygame.image.load(os.path.join(img_folder, r'Enemies/'+img)))

meteor_explosion = {}
meteor_explosion['lg'] = []
meteor_explosion['sm'] = []
meteor_explosion['player'] = []
meteor_explosion_files =  os.path.join(game_folder, 'Assets\Space Shooter\PNG\Explosions')
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(os.path.join(meteor_explosion_files, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75,75))
    meteor_explosion['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    meteor_explosion['sm'].append(img_sm)
    filename = f'sonicExplosion0{i}.png'
    img = pygame.image.load(os.path.join(img_folder, r'sonicExplosion/'+filename)).convert()
    img.set_colorkey(BLACK)
    meteor_explosion['player'].append(img)

meteor_images = []
meteorfiles =  os.listdir(img_folder +r'\Meteors')

for img in meteorfiles:
    meteor_images.append(pygame.image.load(os.path.join(img_folder, 'Meteors/'+img)).convert())


background_transform = pygame.image.load(os.path.join(img_folder,r'starfield.png ')).convert()
background = pygame.transform.scale(background_transform,(720,900))
background_rect = background.get_rect()

#Set up Sounds

shield_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'sfx_shieldUp.ogg'))
shootup_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'sfx_zap.ogg'))
shoot_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'sfx_laser1.ogg'))
hit_sound = pygame.mixer.Sound(os.path.join(sound_folder,'lose.ogg'))

expl_sounds = []

for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, sound)))
pygame.mixer.music.load(os.path.join(sound_folder, 'Blessedmind.ogg'))
pygame.mixer.music.set_volume(0.5)





#Set up Sprites groups for collisions
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
boss = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

show_player_img = True #For the Hide()

#Variables
combo = 0 #THe amount of time you hit an enemy without missing in a row
combo_list = [] #List which stocks all the combos and is used to find the max value 

POWERUP_TIME = 5000 #the amount of MS the powerup lasts

blink_timer = 0 #Timer for the Blink() 


delay = 500 #delay for the spawn 

collision_timer = 0 #variable for the blink 
collision_time = 0 #variable for the invincibility
collision = False #boolean for invincibility

mobs_killed = 0 #Works with the Level function to change the level you're at

#Spawning the first mobs
t=Teleporters()
n = NormalMob()
b = Boss() 

game_over = True #Start the game with a paused screen
Victory = False #Start the game without victory

victory_timer = 9999999999 #Longest timer to not trigger undesirable event

death_player = 0    # Number of deaths

show_timer = 0 #Timer for loading screens

boss_spawn = 1 #Variable to limit the # of spawned boss (level()) 

score = 0

ammo = 0 #not used right now, but can be used to implement an ammo system

difficulty_level = 0#starting difficulty

for i in range(random.randint(6,8)): #spawning a random number of meteors
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

pygame.mixer.music.play(loops=1) #sets up the music 
running = True #Making sure the main loop continues
while running:
    #keep loop running at right speed
    clock.tick(FPS) #keeps fps stable
    if game_over: #start and death screen
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mobs_killed = 0
        boss_spawn = 1
        for i in range(random.randint(4,6)):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
    if Victory:  #victory screen
        b = Boss()
        difficulty_level += 1
        b.shield = 5000 * difficulty_level 
        player.shield = 100
        player.lives = 3
        boss_spawn = 1
        mobs_killed = 0
        show_vi_screen()
        difficulty_level += 1
        for i in range(random.randint(8,12*difficulty_level)):
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
        for i in range (random.randint(2,4*difficulty_level)):
            n = NormalMob()
            all_sprites.add(n)
            mobs.add(n)
        Victory = False
    
 

    
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
    
  

    #update
    
    #Collision detection
    
    if b.shield > 0: #Boss interaction
        hits4 = pygame.sprite.groupcollide(boss, bullets, False, True)
        for hit in hits4:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            b.shield -=50   
    else:  #Boss Death interaction
        hits4 = pygame.sprite.groupcollide(boss, bullets, True, True)
        for hit in hits4:
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            random.choice(expl_sounds).play()
            victory_timer = pygame.time.get_ticks()
    
        if pygame.time.get_ticks() - victory_timer >= 2000: #Wait 2 seconds after killing the Boss
            Victory = True
    
    
    hits3 = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits3:
        if hit.type == 'shield':
            player.shield += random.randrange(10,30)
            if player.shield >= 100:
                player.shield = 100
            shield_sound.play()
        if hit.type == 'gun':
            player.powerup()
            shootup_sound.play()

    
    
    hits2 = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits2:
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if mobs_killed <= 35:
            m= Mob()
            all_sprites.add(m)
            mobs.add(m)
            ammo += 1
            
        else:
            if random.random() < 0.2:
                n = NormalMob()
                all_sprites.add(n)
                mobs.add(n)
            if random.random() < 0.2:
                t = Teleporters()
                all_sprites.add(t)
                mobs.add(t)
            if random.random() < 0.1:
                m= Mob()
                all_sprites.add(m)
                mobs.add(m)
                ammo += 1
        mobs_killed += 1
        combo+=1
        score+= 50 - hit.radius
        random.choice(expl_sounds).play()
        if random.random() >0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    for hit in hits:
        collision = True
        if pygame.time.get_ticks() - collision_timer <= 3000:
            collision = False
        elif pygame.time.get_ticks() - collision_timer > 3000:
            player.shield -= hit.radius * 2
            hit_sound.play()
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        if player.shield <= 0:
            death_explosion = Explosion(hit.rect.center, 'player')
            all_sprites.add(expl)
            player.hide()
            player.lives -=1
            
    hits5 = pygame.sprite.spritecollide(player, enemybullets, False)
    for hit in hits5:
        collision = True
        if pygame.time.get_ticks() - collision_timer <= 3000:
            collision = False
        elif pygame.time.get_ticks() - collision_timer > 3000:
            player.shield -= 30
            hit_sound.play()
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
        if player.shield <= 0:
            death_explosion = Explosion(hit.rect.center, 'player')
            all_sprites.add(expl)
            player.hide()
            player.lives -=1
    
    if player.lives == 0 and not death_explosion.alive():
        death_player +=1
        game_over = True
        
    if combo >=5:
        for i in range(5):
            player.shoot()
 
    if collision == True:
        collision_time = pygame.time.get_ticks()
        collision_timer = pygame.time.get_ticks()
        collision = False
        
    if show_player_img == False:
        player.image = pygame.image.load(os.path.join(img_folder, r'playerShip1_red.png')).convert()
        player.image.set_colorkey(BLACK)
        
    else:
        player.image = player_img
        player.image.set_colorkey(BLACK)
        
        
    if pygame.time.get_ticks() - collision_timer <= 3000:
        player.Blink()
        
        

    
    
    all_sprites.update()
    #Draw
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    Level()
    draw_text(screen, "Score: " + str(score),18, WIDTH/2, 10)
    draw_text(screen, "Combo:" + str(combo),18, WIDTH/2, 40)
    draw_text(screen, "Mobs Killed:" + str(mobs_killed),18, WIDTH/2, 70)
    health_bar(screen, 5,5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives,player_mini_img)
    #Flips the display after drawing
    pygame.display.flip()

pygame.quit()

    
    
    
    
    
    
    
    