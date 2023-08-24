 #Imports
import pygame, os, sys

pygame.font.init()
pygame.mixer.init()

run = True

#Constants
WIDTH, HEIGHT = 1100, 640
TITLE = "SharpShooter"

SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 85, 182


BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
BULLET1, BULLET2, BULLET3 = pygame.Rect(150, 88, 10, 5), pygame.Rect(190, 88, 10, 5), pygame.Rect(230, 88, 10, 5)
PLAY2 = pygame.image.load(os.path.join('assets', 'Play copy.png'))
PLAY1 = pygame.image.load(os.path.join('assets', 'Play.png')) 

RESTART = pygame.image.load(os.path.join('assets', 'restart.png'))


HEALTH_FONT = pygame.font.SysFont('IMPACT', 40)
WINNER_FONT = pygame.font.SysFont('IMPACT', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Bullet_hit.mp3'))
BULLET_FIRE_SOUND =pygame.mixer.Sound(os.path.join('assets', 'Gun_fire.mp3'))

BULLET_VEL = 30 
MAX_BULLETS = 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 

SPACE = pygame.image.load(
    os.path.join('assets', 'space.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'R_ship.png'))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'Y_ ship.png'))

RED_SPACESHIP_IMAGE = pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))

YELLOW_SPACESHIP_IMAGE = pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_HEIGHT, SPACESHIP_WIDTH))


#pygame initialization
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

def main_game():
    #Player Class
    class Player:

        def __init__(self, x1, y1, x2, y2):
            self.x1 = int(x1)
            self.y1 = int(y1)

            self.x2 = int(x2)
            self.y2 = int(y2)

            x1 = self.x1 
            y1 = self.y1

            x2 = self.x2 
            y2 = self.y2
        
            self.velXR = 0
            self.velYR = 0

            self.velXY = 0
            self.velYY = 0

            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False


            self.w_pressed = False
            self.a_pressed = False
            self.s_pressed = False
            self.d_pressed = False

            self.speed = 15

            self.red = pygame.Rect(self.x1, self.y1, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)
            self.yellow = pygame.Rect(self.x2, self.y2, SPACESHIP_HEIGHT, SPACESHIP_WIDTH)

            self.red_health = 5
            self.yellow_health = 5

        def Explosions(self, boom1, boom2, boom3, boom4, boom5):
            win.blit(boom1, (0, 0))
            win.blit(boom2, (0, 0))
            win.blit(boom3, (0, 0))
            win.blit(boom4, (0, 0))
            win.blit(boom5, (0, 0))
        
        def draw(self, win, r_b, y_b, r_h, y_h ):
            win.blit(SPACE, (0, 0))
            pygame.draw.rect(win, (0,0,0), BORDER)

            red_health_text = HEALTH_FONT.render(('Health: '+ str(y_h)), 1, (255, 255, 255)) 
            yellow_health_text = HEALTH_FONT.render(('Health: '+ str(r_h)), 1, (255, 255, 255)) 

            win.blit(red_health_text, (10, 10))
            win.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))

            win.blit(RED_SPACESHIP_IMAGE, (self.red.x, self.red.y)) 
            win.blit(YELLOW_SPACESHIP_IMAGE, (self.yellow.x, self.yellow.y)) 

            for bullet in r_b: 
                pygame.draw.rect(win, (255, 255, 255), bullet)

            for bullet in y_b: 
                pygame.draw.rect(win, (255, 255, 255), bullet)

        def draw_winner(self, text):
            draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
            win.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT//2 - 20 - draw_text.get_height()/2))
            win.blit(RESTART, (WIDTH//2 - 35, HEIGHT//2 - draw_text.get_height()/2 + 100))
            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if mouse[0] > 430 and mouse[0] < 580 and mouse[1] > 350 and mouse[1] < 400:
                            main_game()
                pygame.display.update()
        
        def update(self):
            self.velXR = 0
            self.velYR = 0

            self.velXY = 0
            self.velYY = 0
            
            if self.left_pressed and not self.right_pressed and self.red.x - self.velXR > 0:
                self.velXR = -self.speed
            if self.right_pressed and not self.left_pressed and self.red.x + self.velXR + 85 < BORDER.x:
                self.velXR = self.speed
            if self.up_pressed and not self.down_pressed and self.red.y - self.velYR > -40:
                self.velYR = -self.speed
            if self.down_pressed and not self.up_pressed and self.red.y + self.velYR < 500:
                self.velYR = self.speed

            if self.a_pressed and not self.d_pressed and self.yellow.x - self.velXY - 10 > BORDER.x:
                self.velXY = -self.speed
            if self.d_pressed and not self.a_pressed and self.yellow.x + self.velXY < 1030 - 10:
                self.velXY = self.speed
            if self.w_pressed and not self.s_pressed and self.yellow.y - self.velYY > -40:
                self.velYY = -self.speed
            if self.s_pressed and not self.w_pressed and self.yellow.y + self.velYY < 500:
                self.velYY = self.speed
            
            self.red.x += self.velXR
            self.red.y += self.velYR


            self.yellow.x += self.velXY
            self.yellow.y += self.velYY
            
        def handle_bullets(self, y_b, r_b):
            for bullet in y_b:
                bullet.x -= BULLET_VEL 
                if self.red.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(RED_HIT))
                    y_b.remove(bullet)

                elif bullet.x < 0:
                    y_b.remove(bullet) 


            for bullet in r_b:
                bullet.x += BULLET_VEL 
                if self.yellow.colliderect(bullet):
                    pygame.event.post(pygame.event.Event(YELLOW_HIT))
                    r_b.remove(bullet)

                elif bullet.x > WIDTH:
                    r_b.remove(bullet) 
        
        def main(self): 


            red_bullets = []
            yellow_bullets = []

            run = True
        
            #Main Loop
            while run:


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    # Red spaceship  
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            player.a_pressed = True
                        if event.key == pygame.K_RIGHT:
                            player.d_pressed = True
                        if event.key == pygame.K_UP:
                            player.w_pressed = True
                        if event.key == pygame.K_DOWN:
                            player.s_pressed = True
                        if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(self.red.x + self.red.width, self.red.y + self.red.width + 5, 10, 5)
                            red_bullets.append(bullet)
                            BULLET_FIRE_SOUND.play()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            player.a_pressed = False
                        if event.key == pygame.K_RIGHT:
                            player.d_pressed = False
                        if event.key == pygame.K_UP:
                            player.w_pressed = False
                        if event.key == pygame.K_DOWN:
                            player.s_pressed = False

                    if event.type == YELLOW_HIT:
                        self.yellow_health -= 1
                        BULLET_HIT_SOUND.play()
                    
                    # Yellow spaceship 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            player.left_pressed = True
                        if event.key == pygame.K_d:
                            player.right_pressed = True
                        if event.key == pygame.K_w:
                            player.up_pressed = True
                        if event.key == pygame.K_s:
                            player.down_pressed = True
                        if event.key == pygame.K_RSHIFT and len(yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(self.yellow.x, self.yellow.y + self.yellow.width + 5, 10, 5)
                            yellow_bullets.append(bullet)
                            BULLET_FIRE_SOUND.play()
    
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            player.left_pressed = False
                        if event.key == pygame.K_d:
                            player.right_pressed = False
                        if event.key == pygame.K_w:
                            player.up_pressed = False
                        if event.key == pygame.K_s:
                            player.down_pressed = False

                    if event.type == RED_HIT:
                        self.red_health -= 1
                        BULLET_HIT_SOUND.play()

                winner_text = ""

                if self.red_health <= 0:
                    winner_text = "Yellow Wins!!!"

                if self.yellow_health <= 0:
                    winner_text = "Red Wins!!!"
                        
                if winner_text != "":
                    player.draw_winner(winner_text)
                    
                    
                    
                #Draw
                win.fill((12, 24, 36))  
                player.draw(win, yellow_bullets, red_bullets, self.yellow_health, self.red_health )

                player.handle_bullets(yellow_bullets, red_bullets)
                

                #update
                player.update()
                pygame.display.flip()

                clock.tick(120)
    
    #Player Initialization
    player = Player(10, 220, 1010, 220)

    player.main()

def menu():
    run = True
    while run:
        pygame.init()
        mouse = pygame.mouse.get_pos()

        smallfont = pygame.font.SysFont('IMPACT',100)
        text = smallfont.render('SharpShooter' , True , (226, 226, 227))
        pygame.init()

        win.blit(SPACE, (0,0))
        win.blit(RED_SPACESHIP_IMAGE, (10,0))
        win.blit(YELLOW_SPACESHIP_IMAGE, (1010,0))
        pygame.draw.rect(win, (255,255,255), BULLET1)
        pygame.draw.rect(win, (255,255,255), BULLET2)
        pygame.draw.rect(win, (255,255,255), BULLET3)

        if mouse[0] > 490 and mouse[0] < 620 and mouse[1] > 300 and mouse[1] < 370:
            win.blit(PLAY2, (460-15, 240+10))
        else:
            win.blit(PLAY1, (470-15, 240))

        win.blit(text,(WIDTH//2 - text.get_width()/2, HEIGHT//2 - 100 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse[0] > 490 and mouse[0] < 630 and mouse[1] > 300 and mouse[1] < 360:
                    main_game()

                pygame.display.update()        

pygame.QUIT

menu()
        