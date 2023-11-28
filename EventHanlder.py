import pygame

import random

from Character import*




#you can insert music and sounds in this class

class Event:
    def __init__(self, window, main):
        self.window = window                                #for game screen
        
        self.scroll = 0                                     #for scrolling background purposes
        self.scroll_speed = 5

        self.x = self.window.get_width()
        self.flying_y = 375                                 #locations and speeds of the enemies
        self.ground_y = 425
        self.vel = 3

        self.active_wave = False                            #keeps track of waves and holds the current enemies of wave
        self.waves = 0
        self.spawn_cooldown = 0
        self.enemies = []

        self.score = 0                                      #to keep track and display score
        self.score_cooldown = 0
        self.font = pygame.font.SysFont("arial", 50, True)


        self.faster_cooldown = 1000                         #to prevent the speed from changing to frequently

        self.start = False                                  #to know when the game is over and when it starts
        self.game_over = False

        self.main = main                                    #for sprite collision
        self.mainGroup = pygame.sprite.Group()
        self.mainGroup.add(self.main)


        

    def listen(self, theEvents):
        self.queueOfEvents = theEvents
        for event in self.queueOfEvents:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


    def startScreen(self):              #insert start screen code here
        self.window.fill((0,255,0))
        self.start_text = self.font.render(f"Welcome to endless runner!", True, (255,255,255), None)
        self.start_text2 = self.font.render(f"Press 0 to Start!", True, (255,255,255), None)
        textRect = self.start_text.get_rect()
        textRect2 = self.start_text2.get_rect()
        textRect.center = (400,50)
        textRect2.center = (400, 150)
        self.window.blit(self.start_text, textRect)
        self.window.blit(self.start_text2, textRect2)


        keys = pygame.key.get_pressed()
        self.main.action = 5
        self.main.offset[1] = 50
        self.draw()
        self.main.update_sprite()
        if keys[pygame.K_0]:
            self.start = True
            self.main.offset[1] = 10



    def load_background(self):      #loads the background
        self.bg_images = []

        for i in range(0, 6):
            if i < 5:
                bg_image = pygame.image.load(f"Background/{i}.png").convert_alpha()
                bg_image = pygame.transform.scale(bg_image, (600,600))
                self.bg_images.append(bg_image)
            else:
                self.ground_image = pygame.image.load(f"Background/{i}.png")
                self.ground_image = pygame.transform.scale(self.ground_image, (800,100))

        

    def draw_background(self):      #creates the parrallox effect (scrolling)
        bg_width = self.bg_images[4].get_width()


        ground_width = self.ground_image.get_width()

        for z in range(4):
            speed = 1
            for i in self.bg_images:
                self.window.blit(i, ((z * bg_width + self.scroll * speed),0))
                speed += .2

        for y in range(15):
            self.window.blit(self.ground_image, ((y * ground_width) + self.scroll * 2.5, 550))

        self.scroll -= self.scroll_speed
        if abs(self.scroll)  > bg_width:
            self.scroll = 0

    

    
    def handleWaves(self):      #keeps track of how many waves have passed
        if self.active_wave != True:
            self.active_wave = True
            self.waves += 1

    def spawnEnemeies(self):        #creates and draws the enemies 
        if self.active_wave == False:
            return
        if len(self.enemies) < 4 and self.spawn_cooldown == 0:
            random_number = random.randrange(0,4)
            if random_number == 0:
                self.enemies.append(flyingEnemies(self.x + random.randrange(0,250, 50), self.flying_y))
            elif random_number == 1:
                self.enemies.append(groundEnemies(self.x + random.randrange(0,250, 50), self.ground_y))
            elif random_number == 2:
                self.enemies.append(flyingEnemies(self.x + random.randrange(0,250, 50), self.flying_y))
                self.enemies.append(flyingEnemies(self.x + random.randrange(0,250, 50), self.flying_y -150))
            else:
                self.enemies.append(groundEnemies(900, self.ground_y))
                self.enemies.append(groundEnemies(1000, self.ground_y))

            self.spawn_cooldown = 100
        else: 
            return

    def check(self):        #check to see if enemies are out of the screen. If yes, then it would remove them from list
        checker = 0
        size_of_wave = len(self.enemies)
        for enemy in self.enemies:
            if enemy.rect.x < 0:
                checker += 1
        if checker == size_of_wave:
            self.active_wave = False

    def handleEnemies(self):        
        for enemy in self.enemies:  
            bottomr, _ = enemy.rect.bottomright
            if bottomr > 0:
                self.check_enemy_collision(enemy)
                self.handle_enemy_attack(enemy)
                enemy.rect.x -= self.vel * 2
            
            else:
                self.enemies.remove(enemy)

    def check_enemy_collision(self, enemy):
        if pygame.Rect.colliderect(enemy.rect, self.main.rect):
            if pygame.sprite.spritecollide(enemy, self.mainGroup, False):
                self.main.health -=100
                if self.main.health == 0:
                    self.game_over = True    
                    print("Game Over")

    def handle_enemy_attack(self, enemy):
        if enemy.rect.x - self.main.rect.x < 125 and self.main.rect.centery - enemy.rect.centery < 75:
            enemy.attacking = True
        else:
            enemy.attacking = False

    def scoreBoard(self):
        if self.score_cooldown == 0:
            self.score += 1
            self.score_cooldown = 10
        self.showScore()

    def showScore(self):
        if self.game_over == False:
            self.score_text = self.font.render(f"Score: {self.score} meters", True, (255,255,255), None)
        else:
            self.score_text = self.font.render(f"Final Score: {self.score} meters", True, (255,255,255), None)
        textRect = self.score_text.get_rect()
        textRect.center = (400,50)
        self.window.blit(self.score_text, textRect)

    def handle_cooldowns(self):
        if self.spawn_cooldown > 0:
            self.spawn_cooldown -=1

        if self.score_cooldown > 0:
            self.score_cooldown -=1

        if self.faster_cooldown > 0:
            self.faster_cooldown -= 10


    
    def draw(self):
        for enemy in self.enemies:
            enemy.update_sprite()
            enemy.draw(self.window)
        self.main.update_sprite()
        self.main.draw(self.window)

    def goFaster(self):

        if self.score % 20 == 0 and self.faster_cooldown == 0:
            self.faster_cooldown = 100
            self.vel += .5
            self.scroll_speed += .3



    


