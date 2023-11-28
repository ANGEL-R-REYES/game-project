import pygame
from pygame import mixer

from Character import *
from EventHandler import *



pygame.init()



mainDisplay = pygame.display.set_mode((800, 600))

def music(x):
    if(x == True):
        mixer.music.load('music.wav')
        mixer.music.play(-1)
    elif(x == False):
        mixer.music.pause()
   

Clock = pygame.time.Clock()
             

def main(mainDisplay):

    fps = 60
    
   
    Neo = theMain(50, 500)                   

    handleEvents = Event(mainDisplay, Neo)
    handleEvents.load_background()

     
    while True:
        handleEvents.listen(pygame.event.get())
        if handleEvents.start == False and handleEvents.game_over == False:
            handleEvents.startScreen()
            x = True
            music(x)

        elif handleEvents.game_over == False and handleEvents.start == True:
            handleEvents.draw_background()  
            Clock.tick(fps)

            handleEvents.handleWaves()
            handleEvents.spawnEnemeies()    
            
            handleEvents.check()
            handleEvents.handleEnemies()
        
            handleEvents.handle_cooldowns()
            handleEvents.scoreBoard()

            handleEvents.draw()
            handleEvents.goFaster()

            
            

            Neo.loop()      #to get user input. Space for jump, d for ducking
            

        else:           
            x = False
            music(x)
            mainDisplay.fill((0,255,0))
            handleEvents.showScore()
           
      

        pygame.display.update()

if __name__ == "__main__":      #only runs game through this file directly
    main(mainDisplay)



