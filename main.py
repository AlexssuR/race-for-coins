# Complete your game here
import pygame
import random

#Constants used to define the game caracteristics
MAX_COINS_ON_SCREEN=5
DOORS=1
MIN_DIST=100
MONSTER_BLINK_INTERVAL = 600
SCREEN_W=800
SCREEN_H=600
PLAYER_SPEED=1
ENEMY_SPEED=1
FOOTER_RATIO = 0.10      # 12% of the screen height
MARGIN_LEFT  = 20
MARGIN_TOP   = 20
MARGIN_RIGHT = 20
GAP_ARENA_FOOTER = 10    # vertical gap between arena and footer
MATCH_POINTS=15

#Base class to handle the objects of the game
class Entity:
    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.rect = sprite.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.sprite, self.rect)

#Specialized classes to handle the player and the opponent
#This class manage the player, it move the robot according to the arrows pressed and uses doors to teleport
class Player(Entity):
    def __init__(self,sprite,x,y):
        super().__init__(sprite,x,y)
        self.points=0
        self.to_left = False
        self.to_right = False
        self.to_up = False
        self.to_down = False
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.to_left = True
            elif event.key == pygame.K_RIGHT:
                self.to_right = True
            elif event.key == pygame.K_UP:
                self.to_up = True
            elif event.key == pygame.K_DOWN:
                self.to_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.to_left = False
            elif event.key == pygame.K_RIGHT:
                self.to_right = False
            elif event.key == pygame.K_UP:
                self.to_up = False
            elif event.key == pygame.K_DOWN:
                self.to_down = False
    
    def move(self, arena_rect):
        if self.to_right:
            self.rect.x += PLAYER_SPEED
        if self.to_left:
            self.rect.x -= PLAYER_SPEED
        if self.to_up:
            self.rect.y -= PLAYER_SPEED
        if self.to_down:
            self.rect.y += PLAYER_SPEED
        self.rect.clamp_ip(arena_rect)
    
    def collect_coin(self,coins):
        for coin in coins.copy():
            if self.rect.colliderect(coin.rect):
                coins.remove(coin)
                self.points+=1
    def teleport(self, doors, arena_rect):
        for i in range(len(doors)):
            door_in = doors[i]
            if self.rect.colliderect(door_in.rect):
                door_out = doors[i ^ 1]  # paired door
                gap = 2  # pixels outside the exit door (avoid immediate re-collision)

                # Decide entry side from current movement flags.
                # Priority: horizontal over vertical (change if you prefer).
                if self.to_right:
                # preserve vertical offset relative to door center
                    offset_y = self.rect.centery - door_in.rect.centery
                    self.rect.centery = door_out.rect.centery + offset_y
                    self.rect.left = door_out.rect.right + gap
                elif self.to_left:
                    offset_y = self.rect.centery - door_in.rect.centery
                    self.rect.centery = door_out.rect.centery + offset_y
                    self.rect.right = door_out.rect.left - gap
                elif self.to_down:
                    # preserve horizontal offset relative to door center
                    offset_x = self.rect.centerx - door_in.rect.centerx
                    self.rect.centerx = door_out.rect.centerx + offset_x
                    self.rect.top = door_out.rect.bottom + gap
                elif self.to_up:
                    offset_x = self.rect.centerx - door_in.rect.centerx
                    self.rect.centerx = door_out.rect.centerx + offset_x
                    self.rect.bottom = door_out.rect.top - gap
                else:
                    # No direction pressed: fallback (keep relative offset + push right)
                    offset_x = self.rect.centerx - door_in.rect.centerx
                    offset_y = self.rect.centery - door_in.rect.centery
                    self.rect.centerx = door_out.rect.centerx + offset_x
                    self.rect.centery = door_out.rect.centery + offset_y
                    self.rect.left = door_out.rect.right + gap
                # keep inside arena
                self.rect.clamp_ip(arena_rect)
                break           
    def get_points(self):
        return self.points    

#This class handle the Enemy player. It define a simple strategy to collect coins and a funny blink effect    
class Enemy(Entity):
    def __init__(self,sprite,x,y):
       super().__init__(sprite,x,y)
       self.monster_visible=True
       self.points=0

    def get_closest_coin(self, coins):
        if not coins:
            return None
        return min(coins,key=lambda coin: (self.rect.centerx - coin.rect.centerx) ** 2 + (self.rect.centery - coin.rect.centery) ** 2)

    def get_points(self):
        return self.points    
    
    def move(self, coins, arena_rect):
        target_coin = self.get_closest_coin(coins)
        if target_coin is None:
            return
        # move to target coin
        if self.rect.centerx < target_coin.rect.centerx:
            self.rect.x += ENEMY_SPEED
        elif self.rect.centerx > target_coin.rect.centerx:
            self.rect.x -= ENEMY_SPEED

        if self.rect.centery < target_coin.rect.centery:
            self.rect.y += ENEMY_SPEED
        elif self.rect.centery > target_coin.rect.centery:
            self.rect.y -= ENEMY_SPEED
        #make sure the enemy don't exit arena
        self.rect.clamp_ip(arena_rect)
        # catch coin
        if  self.monster_visible and self.rect.colliderect(target_coin.rect):
            coins.remove(target_coin)
            self.points+=1

    def draw(self, screen):
        self.monster_visible = (pygame.time.get_ticks() // MONSTER_BLINK_INTERVAL) % 2 == 0
        if self.monster_visible:
            super().draw(screen)

#The main class that manage all the game play. It define the entities paint them and handle the game loop and events
class CoinsRace:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        w, h = self.window.get_size()
        footer_h = int(h * FOOTER_RATIO)
        self.footer_rect = pygame.Rect(0,h - footer_h,w,footer_h)
        self.arena_rect = pygame.Rect(MARGIN_LEFT,MARGIN_TOP,w - MARGIN_LEFT - MARGIN_RIGHT,(h - footer_h) - MARGIN_TOP - GAP_ARENA_FOOTER)

        self.footer_font = pygame.font.SysFont("Arial", 22) 
        self.robot = Player(pygame.image.load("robot.png"),0,0)
        self.coin_sprite=pygame.image.load("coin.png")
        self.monster=Enemy(pygame.image.load("monster.png"),self.arena_rect.centerx,self.arena_rect.centery)
        self.door_sprite=pygame.image.load("door.png")
        self.coins = []
        self.doors=[]

        #Game Over
        self.game_over=False
        self.game_over_text = pygame.font.SysFont(None, 60).render("GAME OVER", True, (255, 80, 80))
        self.restart_text = pygame.font.SysFont(None, 20).render("Press Space to restart", True, (255, 80, 80))

        self.setup_match()
        #Start game loop
        self.game_loop()
             
    def setup_match(self):
        self.game_over = False
        # reset scores
        self.robot.points = 0
        self.monster.points = 0
        
        # reset players
        self.robot = Player(pygame.image.load("robot.png"),0,0)
        self.monster=Enemy(pygame.image.load("monster.png"),self.arena_rect.centerx,self.arena_rect.centery)
        
        # reset doors and coins
        self.coins.clear()
        self.doors.clear()
        
        # create doors 
        for i in range(DOORS):
            door_x=random.randint(0,self.arena_rect.centerx)
            door_y=random.randint(0,self.arena_rect.centery)
            #Make sure the doors are not to close
            for door in self.doors:
                if(door_x - door.rect.x)**2 + (door_y - door.rect.y)**2 < MIN_DIST**2:
                    door_x += MIN_DIST
                    door_y += MIN_DIST
            #Door
            self.doors.append(Entity(self.door_sprite,door_x,door_y))    
            #Opposite Door
            self.doors.append(Entity(self.door_sprite,self.arena_rect.width - self.door_sprite.get_width()- door_x, self.arena_rect.height - self.door_sprite.get_height()- door_y))
        

    def game_loop(self):     
        clock = pygame.time.Clock()
        pygame.display.set_caption("Race for Coins")
        while True:
            clock.tick(60)
            #Handle game events
            self.handle_events()
            self.window.fill((30, 30, 30))
            self.set_game_over()  
            if not self.game_over:
                #Setup game arena
                pygame.draw.line(self.window, (90, 90, 90),(0, self.footer_rect.top),(self.window.get_width(), self.footer_rect.top),2)
                #Handle entities
                self.robot.move(self.arena_rect)
                self.robot.collect_coin(self.coins)
                self.robot.teleport(self.doors,self.arena_rect)
                self.robot.draw(self.window)
                self.add_coins_on_the_screen()
                self.add_doors_on_the_screen()
                self.monster.move(self.coins,self.arena_rect)
                self.monster.draw(self.window)
                
            else:
                 game_over_rect= self.game_over_text.get_rect(center=self.window.get_rect().center)
                 self.window.blit(self.game_over_text, game_over_rect)
                 restart_rect = self.restart_text.get_rect(midtop=(game_over_rect.centerx, game_over_rect.bottom + 10))
                 self.window.blit(self.restart_text, restart_rect)

            self.mark_points()
            pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)       

            # Restart only when game over
            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.setup_match()
                    continue

            # Only control player during active match
            if not self.game_over:
                self.robot.handle_event(event)

    def add_coins_on_the_screen(self):
        if len(self.coins) < MAX_COINS_ON_SCREEN:
            x = random.randint(0, self.arena_rect.width - self.coin_sprite.get_width())
            y = random.randint(0, self.arena_rect.height - self.coin_sprite.get_height())
            coin= Entity(self.coin_sprite, x, y)
            for door in self.doors:
                if coin.rect.colliderect(door.rect):
                    # shift away (simple deterministic shift)
                    coin.rect.x += MIN_DIST
                    coin.rect.y += MIN_DIST
                    # clamp inside arena
                    coin.rect.clamp_ip(self.arena_rect)
                    break
            self.coins.append(coin)
        #Draw coins
        for coin in self.coins:
            coin.draw(self.window)

    def add_doors_on_the_screen(self):
        for door in self.doors:
            door.draw(self.window)

    def mark_points(self):
        player_text = self.footer_font.render(f"Player: {self.robot.get_points()}", True, (0, 0, 255))
        enemy_text  = self.footer_font.render(f"Computer: {self.monster.get_points()}", True, (255, 0, 0))
        self.window.blit(player_text, (15, self.footer_rect.top + 18))
        self.window.blit(enemy_text,  (self.footer_rect.right - enemy_text.get_width() - 15, self.footer_rect.top + 18))
    
    def set_game_over(self):
        if self.robot.get_points()==MATCH_POINTS or self.monster.get_points()==MATCH_POINTS:
            self.game_over=True
        else:
            self.game_over=False    
             

if __name__ == "__main__":
    CoinsRace()
    
    
    
    

    
    
    
    
         




