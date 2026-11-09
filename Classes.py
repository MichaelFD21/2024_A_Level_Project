import pygame
import math
import Rooms
import random

pygame.init()
Screen_Width, Screen_Height = 1280, 720
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
DefaultProjectile=pygame.image.load('Assets/Projectiles/Projectile1.png').convert_alpha()
BouncyProjectile=pygame.image.load('Assets/Projectiles/Projectile2.png').convert_alpha()
PoisonProjectile=pygame.image.load('Assets/Projectiles/Projectile3.png').convert_alpha()
Projectiles = pygame.sprite.Group()
Enemies = pygame.sprite.Group()
EnemyProjectiles = pygame.sprite.Group()
class PlayerProjectile(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, target_world_x, target_world_y, ProjectileType, rooms, damage, type_name="default"):
        super().__init__()
        self.image = ProjectileType
        self.rect = self.image.get_rect(center=(world_x, world_y))
        self.speed = 1  # Projectile speed
        # Calculate direction
        angle = math.atan2(target_world_y - world_y, target_world_x - world_x)
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
        # Precise world position
        self.float_x = world_x
        self.float_y = world_y
        self.rooms = rooms
        self.damage = damage
        # Type info for special behavior
        self.type_name = type_name
        self.poison_ticks = 8 if type_name == "poison" else 0
        self.tick_timer = 0
        self.tick_interval = 500  # ms between ticks
        self.target = None
        self.spawn_time = 0
        self.poison_applied = False
        self.bounces_remaining = 5 if type_name == "bouncy" else 0
    def update(self, player_movement_x, player_movement_y):
        # Move first
        self.float_x += self.vel_x
        self.float_y += self.vel_y
        # Wall collision check
        for room, pos in self.rooms:
            room_offset_x, room_offset_y = pos
            rel_x = int((self.float_x - room_offset_x) // Rooms.Tile_Size)
            rel_y = int((self.float_y - room_offset_y) // Rooms.Tile_Size)
            if 0 <= rel_y < len(room) and 0 <= rel_x < len(room[0]):
                tile = room[rel_y][rel_x]
                if tile == Rooms.W:
                    if self.bounces_remaining > 0:
                        # Backtrack to test previous axis independently
                        prev_x = self.float_x - self.vel_x
                        prev_y = self.float_y - self.vel_y
                        # Check horizontal bounce (left/right)
                        test_rel_x = int((prev_x - room_offset_x) // Rooms.Tile_Size)
                        if 0 <= rel_y < len(room[0]) and 0 <= test_rel_x < len(room[0]):
                            if room[rel_y][test_rel_x] != Rooms.W:
                                self.vel_x *= -1
                                self.bounces_remaining -= 1
                                print(f"Horizontal wall bounce! Bounces left: {self.bounces_remaining}")
                                return
                        # Check vertical bounce (top/bottom)
                        test_rel_y = int((prev_y - room_offset_y) // Rooms.Tile_Size)
                        if 0 <= test_rel_y < len(room) and 0 <= rel_x < len(room[0]):
                            if room[test_rel_y][rel_x] != Rooms.W:
                                self.vel_y *= -1
                                self.bounces_remaining -= 1
                                print(f"Vertical wall bounce! Bounces left: {self.bounces_remaining}")
                                return
                        # If it can't determine a clean axis bounce, just bounce both as fallback
                        self.vel_x *= -1
                        self.vel_y *= -1
                        self.bounces_remaining -= 1
                        print(f"Default bounce. Bounces left: {self.bounces_remaining}")
                        return
                    else:
                        print("Projectile hit a wall and was destroyed.")
                        self.kill()
                        return
        # Draw projectile
        screen_x = self.float_x + player_movement_x
        screen_y = self.float_y + player_movement_y
        self.rect.center = (screen_x, screen_y)
        screen.blit(self.image, self.rect.topleft)

class Player(pygame.sprite.Sprite):
    HealthBarSprites=['Assets/HealthImage/NoHP.png',
                      'Assets/HealthImage/OneHP.png',
                      'Assets/HealthImage/TwoHP.png',
                      'Assets/HealthImage/ThreeHP.png',
                      'Assets/HealthImage/FourHP.png',
                      'Assets/HealthImage/FiveHP.png',
                      'Assets/HealthImage/FullHP.png']
    def __init__(self, pos_x, pos_y):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.currentfloor=1
        self.boss_room_next=False
        self.PotentialPowerUps=["SpeedPowerUp" , "DamagePowerUp", "AttackSpeedPowerUp"]
        self.SPU, self.ASPU, self.DPU = 0,0,0
        self.ProjectileType=DefaultProjectile
        self.PlayerSprite = pygame.image.load('Assets/PlayableCharacters/Patrick.png').convert_alpha()
        self.image = self.PlayerSprite
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        #The Current Position of the Player will be contained here
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        #velocity is used within the calculation of moving smoothly
        self.vel_x = 0
        self.vel_y = 0
        #left, right, up down being pressed bools required for movement
        self.Lpress = False
        self.Rpress = False
        self.Upress = False
        self.Dpress = False
    BaseShotCD=5
    shot_CD_max, shot_CD= BaseShotCD,0
    def shoot(self, mouse_x, mouse_y):
        if self.shot_CD == 0:
            # Convert mouse position to world coordinates
            target_world_x = mouse_x - self.PMove_X
            target_world_y = mouse_y - self.PMove_Y
            # Player's actual world position
            player_world_x = -self.PMove_X + (Screen_Width // 2)
            player_world_y = -self.PMove_Y + (Screen_Height // 2)
            # Determine projectile type name
            if self.ProjectileType == BouncyProjectile:
                type_name = "bouncy"
            elif self.ProjectileType == PoisonProjectile:
                type_name = "poison"
            else:
                type_name = "default"
            projectile = PlayerProjectile(
                world_x=player_world_x,
                world_y=player_world_y,
                target_world_x=target_world_x,
                target_world_y=target_world_y,
                ProjectileType=self.ProjectileType,
                rooms=self.rooms,
                damage=self.Damage,
                type_name=type_name
            )
            Projectiles.add(projectile)
            self.shot_CD = self.shot_CD_max

    def set_rooms(self,rooms):
        self.rooms = rooms # store rooms for collision
    def ModifyStats(self):
        self.Damage= self.BaseDamage+(0.25*self.DPU)
        print(f"Damage is now {self.Damage}")
        if self.BaseMoveSpeed +(0.25*self.SPU) > 4:
            self.MoveSpeed=4
        else:
            self.MoveSpeed= self.BaseMoveSpeed+(0.25*self.SPU)
        print(f"Move Speed is Now {self.MoveSpeed}")
        if self.BaseShotCD-(0.5*self.ASPU) < 2:
            self.shot_CD_max = 2
        else:
            self.shot_CD_max=self.BaseShotCD-(0.5*self.ASPU)
        print(f"Shooting Cooldown is Now {self.shot_CD_max}")

    def take_damage(self,amount): #Function adjusting player HP when taking damage
        self.Hp-=amount
    def give_gold(self,amount): #Gives the player gold
        self.Gold+=amount
    def give_powerup(self, PowerUp):
        #Gives the player a power-up and updates stats.
        if PowerUp == "SpeedPowerUp":
            self.SPU += 1
            print("Speed increased!")
        elif PowerUp == "DamagePowerUp":
            self.DPU += 1
            print("Damage increased!")
        elif PowerUp == "AttackSpeedPowerUp":
            self.ASPU += 1
            print("Attack speed increased!")
        self.ModifyStats()  # Update player stats

    def check_interact(self):
        # Checks if the player is colliding with an interactive tile
        player_rect = pygame.Rect(Screen_Width // 2, Screen_Height // 2, self.rect.width, self.rect.height)
        for room, pos in self.rooms:
            room_offset_x, room_offset_y = pos
            for y, row in enumerate(room):
                for x, tile in enumerate(row):
                    tile_x = room_offset_x + x * Rooms.Tile_Size + self.PMove_X
                    tile_y = room_offset_y + y * Rooms.Tile_Size + self.PMove_Y
                    tile_rect = pygame.Rect(tile_x, tile_y, Rooms.Tile_Size, Rooms.Tile_Size)
                    if player_rect.colliderect(tile_rect):  # Player is touching the tile
                        if tile in [Rooms.C_C, Rooms.O_C, Rooms.L_C]:  
                            self.InteractWithChest(room, x, y)  
                        elif tile == Rooms.M:  
                            self.interact_market()
                        elif tile == Rooms.St:
                            print("Stair tile detected. Attempting floor transition.")
                            new_rooms = self.interact_stairs()
                            if new_rooms:
                             return "next_floor"
        return None # No Interactable

    Boss = False
    def interact_stairs(self):
        print(f"Interacted with Stairs, moving to floor {self.currentfloor + 1}")
        self.currentfloor += 1  
        floor_seed = self.base_seed + self.currentfloor
        Boss = self.currentfloor % 5 == 1
        new_rooms = Rooms.GenRooms(floor_seed, Boss)
        for room, pos in new_rooms:
            if room == Rooms.SpawnRoom:
                start_x = pos[0] + (len(room[0]) // 2) * Rooms.Tile_Size
                start_y = pos[1] + (len(room) // 2) * Rooms.Tile_Size
                self.rect.topleft = (start_x, start_y)
                print(f"Placed player at: {self.rect.topleft}")
                break
        return new_rooms

    def interact_market(self):
        cost = 4 + self.currentfloor
        if self.Gold >= cost:
            self.Gold -= cost
            print(f"Spent {cost} gold on market powerup!")
            # Determine which market tile player is on
            player_rect = pygame.Rect(Screen_Width // 2, Screen_Height // 2, self.rect.width, self.rect.height)
            for room, pos in self.rooms:
                room_offset_x, room_offset_y = pos
                for y, row in enumerate(room):
                    for x, tile in enumerate(row):
                        tile_x = room_offset_x + x * Rooms.Tile_Size + self.PMove_X
                        tile_y = room_offset_y + y * Rooms.Tile_Size + self.PMove_Y
                        tile_rect = pygame.Rect(tile_x, tile_y, Rooms.Tile_Size, Rooms.Tile_Size)
                        if player_rect.colliderect(tile_rect) and tile == Rooms.M:
                            # Set seed based on market tile (like render_map does)
                            marketchoice = int(self.base_seed) + x + y + self.currentfloor
                            random.seed(marketchoice)
                            powerup = random.choice(self.PotentialPowerUps)
                            self.give_powerup(powerup)
                            print(f"Received powerup from market: {powerup}")
                            room[y][x] = Rooms.F  # Set tile to floor (used up)
                            return
        else:
            print("Not enough gold for market powerup.")

    def InteractWithChest(self, room, x, y):
        #Chest Interaction
        CurrentChestState = room[y][x]  # Get the current state of the chest
        if CurrentChestState == Rooms.C_C:  # Closed chest
            print("Chest Opened!")
            room[y][x] = Rooms.O_C  # Change to opened chest
        elif CurrentChestState == Rooms.O_C:  # Opened chest
            print("Chest Looted!")
            room[y][x] = Rooms.L_C  # Change to looted chest
            num = random.randint(1, 10)
            if num <= 7:
                self.give_gold(num) # Update player's gold
                print(f"Received {num} gold!")
            else:
                powerup_type = random.choice(self.PotentialPowerUps) # Randomly selects powerup
                self.give_powerup(powerup_type) # passes power up into function to modify stats
                print(f"Received powerup: {powerup_type}")
        elif CurrentChestState == Rooms.L_C:  # Looted chest
            print("This chest is empty.")

    def check_collision(self, direction):
        #Collision Check with walls
        player_center_x = Screen_Width // 2
        player_center_y = Screen_Height // 2
        next_offset_x = self.PMove_X
        next_offset_y = self.PMove_Y
        if direction == "left":
            next_offset_x += self.MoveSpeed
        elif direction == "right":
            next_offset_x -= self.MoveSpeed
        elif direction == "up":
            next_offset_y += self.MoveSpeed
        elif direction == "down":
            next_offset_y -= self.MoveSpeed
        for room, pos in self.rooms:
            room_offset_x, room_offset_y = pos
            for y, row in enumerate(room):
                for x, tile in enumerate(row):
                    if tile == Rooms.W:  # Wall tile
                        wall_rect = pygame.Rect(
                            room_offset_x + x * Rooms.Tile_Size + next_offset_x,
                            room_offset_y + y * Rooms.Tile_Size + next_offset_y,
                            Rooms.Tile_Size,
                            Rooms.Tile_Size
                        )
                        player_rect = pygame.Rect(player_center_x, player_center_y, self.rect.width, self.rect.height)
                        if wall_rect.colliderect(player_rect):
                            return True  # Collision detected
        return False  # No collision

    def update(self):   
        self.vel_x = 0
        self.vel_y = 0
        if self.Lpress and not self.Rpress:
            if not self.check_collision("left"):  
                self.PMove_X += self.MoveSpeed  
        if self.Rpress and not self.Lpress:
            if not self.check_collision("right"):  
                self.PMove_X -= self.MoveSpeed  
        if self.Upress and not self.Dpress:
            if not self.check_collision("up"):  
                self.PMove_Y += self.MoveSpeed  
        if self.Dpress and not self.Upress:
            if not self.check_collision("down"):  
                self.PMove_Y -= self.MoveSpeed  
        # Keep player centered on screen
        self.rect.topleft = (Screen_Width // 2, Screen_Height // 2)
        # Render the player at the center
        screen.blit(self.PlayerSprite, self.rect.topleft)
        SPU_Image=pygame.image.load('Assets/OtherAssets/SPDPower.png')
        screen.blit(pygame.transform.scale(SPU_Image,(50,50)),(300,0))
        DPU_Image=pygame.image.load('Assets/OtherAssets/AttackPowerUp.png')
        screen.blit(pygame.transform.scale(DPU_Image,(50,50)),(400,0))
        ASPU_Image=pygame.image.load('Assets/OtherAssets/AttackSpeedPower.png')
        screen.blit(pygame.transform.scale(ASPU_Image,(50,50)),(500,0))
        Currency_Image=pygame.image.load('Assets/OtherAssets/Currency.png')        #Defines Player's Currency Icon
        screen.blit(pygame.transform.scale(Currency_Image,(50,50)), (10 , 50))     #Displays Currency Icon

        # Update cooldown timer if active
        if self.shot_CD > 0:
            self.shot_CD -= 0.05
            if self.shot_CD < 0:
                self.shot_CD = 0

    MaxHP, Hp, BaseDamage, Damage, Gold, BaseMoveSpeed, MoveSpeed = 6, 6, 1, 1, 0, 1, 1
    PMove_X, PMove_Y = 0,0
class Warrior(Player):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.BaseDamage = 2
        self.Damage = 2
        self.BaseMoveSpeed = 1.25
        self.MoveSpeed = 1.25
        self.ProjectileType = DefaultProjectile
        self.PlayerSprite = pygame.image.load('Assets/PlayableCharacters/Warrior.png')
        self.image = self.PlayerSprite
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

class ArmouredMage(Player):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.ProjectileType = BouncyProjectile
        self.BaseDamage = 3
        self.Damage = 3
        self.PlayerSprite = pygame.image.load("Assets/PlayableCharacters/ArmouredMage.png")
        self.image = self.PlayerSprite
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

class Assassin(Player):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.ProjectileType = PoisonProjectile
        self.BaseDamage = 1
        self.Damage = 1
        self.BaseMoveSpeed = 1.5
        self.MoveSpeed = 1.5
        self.PlayerSprite = pygame.image.load("Assets/PlayableCharacters/Assassin.png")
        self.image = self.PlayerSprite
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

class TrapTile:
    STATES = [Rooms.TrapA, Rooms.TrapB, Rooms.TrapC]
    def __init__(self, room, x, y, room_position):
        self.room = room
        self.x = x  
        self.y = y
        #Tile positions in room ^
        self.room_position = room_position  # World offset of the room
        self.state_index = 0
        self.timer = 0
        self.cooldown = 0  # Prevent repeated damage in same TrapC cycle

    def update(self, dt, player):
        # Rotate trap state every 2 seconds
        self.timer += dt
        if self.timer >= 2000:
            self.timer = 0
            self.state_index = (self.state_index + 1) % 3
            self.room[self.y][self.x] = self.STATES[self.state_index]
            if self.state_index == 0:
                self.cooldown = 0  # Reset damage at start of new cycle
        # Only damage player in TrapC state
        if self.room[self.y][self.x] == Rooms.TrapC:
            room_offset_x, room_offset_y = self.room_position
            # Calculate trap's screen-relative position
            tile_x = room_offset_x + self.x * Rooms.Tile_Size + player.PMove_X
            tile_y = room_offset_y + self.y * Rooms.Tile_Size + player.PMove_Y
            trap_rect = pygame.Rect(tile_x, tile_y, Rooms.Tile_Size, Rooms.Tile_Size)
            # Player is always centered on screen
            player_rect = pygame.Rect(
                Screen_Width // 2,
                Screen_Height // 2,
                player.rect.width,
                player.rect.height
            )
            if player_rect.colliderect(trap_rect) and self.cooldown == 0:
                print("Collision with TrapC! Damaging player.")
                player.take_damage(1)
                self.cooldown = 1
#Enemy Classes + Functions/Procedures
#Pathfinding/Movement Helping functions
def tile_is_walkable(tile):
    return tile in [Rooms.F, Rooms.E, Rooms.D, Rooms.C_C, Rooms.O_C, Rooms.L_C]
def get_tile_at(world_x, world_y, rooms):
    for room, (room_x, room_y) in rooms:
        if not (room_x <= world_x < room_x + len(room[0]) * Rooms.Tile_Size and
                room_y <= world_y < room_y + len(room) * Rooms.Tile_Size):
            continue
        rel_x = (world_x - room_x) // Rooms.Tile_Size
        rel_y = (world_y - room_y) // Rooms.Tile_Size
        if 0 <= rel_x < len(room[0]) and 0 <= rel_y < len(room):
            return room[int(rel_y)][int(rel_x)]
    return None

#Enemy Projectile Class
class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, world_x, world_y, target_x, target_y, rooms, damage):
        super().__init__()
        self.image = pygame.image.load('Assets/Projectiles/EnemyProjectile.png')
        self.rect = self.image.get_rect(center=(world_x, world_y))
        self.speed = 1
        self.rooms = rooms
        self.damage = damage
        self.float_x = world_x
        self.float_y = world_y
        dx = target_x - world_x
        dy = target_y - world_y
        if dx == 0 and dy == 0:
            angle = random.uniform(0.01, 2 * math.pi)
        else:
            angle = math.atan2(dy, dx)
        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed
    def update(self, player_offset_x, player_offset_y):
        self.float_x += self.vel_x
        self.float_y += self.vel_y
        # Collision check with walls
        for room, pos in self.rooms:
            offset_x, offset_y = pos
            rel_x = int((self.float_x - offset_x) // Rooms.Tile_Size)
            rel_y = int((self.float_y - offset_y) // Rooms.Tile_Size)
            if 0 <= rel_y < len(room) and 0 <= rel_x < len(room[0]):
                tile = room[rel_y][rel_x]
                if tile == Rooms.W:
                    self.kill()
                    return
        screen_x = self.float_x + player_offset_x
        screen_y = self.float_y + player_offset_y
        self.rect.center = (screen_x, screen_y)
        screen.blit(self.image, self.rect.topleft)

#Enemy Classes
#Stationary Enemy
class BaseEnemy(pygame.sprite.Sprite):
    def __init__(self, world_position, player):
        super().__init__()
        self.image = pygame.image.load('Assets/PlayableCharacters/Patrick.png').convert_alpha()  # placeholder
        self.rect = self.image.get_rect(topleft=world_position)
        self.shot_cooldown = 0  # in frames
        self.shot_cooldown_max = 1440
        self.rect = self.image.get_rect(topleft=world_position)
        self.pos_x, self.pos_y = world_position
        self.HP = 1
        self.gold_reward = 1
        self.player = player
        self.fire_range = 200
        self.poisoned = False
        self.poison_ticks_remaining = 0
        self.poison_tick_interval = 500  # in ms
        self.poison_next_tick = 0
        self.poison_damage = 0
        self.alive = True
    def apply_poison(self, damage):
        if not self.poisoned:
            self.poisoned = True
            self.poison_ticks_remaining = 8
            self.poison_damage = damage / 5
            self.poison_next_tick = pygame.time.get_ticks() + self.poison_tick_interval
    def update(self, player_offset_x, player_offset_y):
        if not self.alive:
            return
        player_world_x = -self.player.PMove_X + (Screen_Width // 2)
        player_world_y = -self.player.PMove_Y + (Screen_Height // 2)
        dx = player_world_x - self.pos_x
        dy = player_world_y - self.pos_y
        dist = math.hypot(dx, dy)
        if dist < getattr(self, "fire_range", 0):
            if self.shot_cooldown <= 0:
                self.shoot_projectile(player_world_x, player_world_y)
                self.shot_cooldown = self.shot_cooldown_max
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        screen_x = self.pos_x + player_offset_x
        screen_y = self.pos_y + player_offset_y
        self.rect.topleft = (screen_x, screen_y)
        # Poison status ticking
        if self.poisoned and self.alive:
            now = pygame.time.get_ticks()
            if now >= self.poison_next_tick:
                self.take_damage(self.poison_damage)
                self.poison_ticks_remaining -= 1
                self.poison_next_tick = now + self.poison_tick_interval
                if self.poison_ticks_remaining <= 0:
                    self.poisoned = False
        screen.blit(self.image, self.rect.topleft)
    def take_damage(self, amount):
        self.HP -= amount
        print(f"{self.__class__.__name__} took {amount} damage, HP now {self.HP}")
        if self.HP <= 0:
            self.die()
    def die(self):
        print(f"{self.__class__.__name__} died.")
        self.player.give_gold(self.gold_reward)
        self.alive = False
        self.kill()
    def shoot_projectile(self, target_x, target_y):
        projectile = EnemyProjectile(
            world_x=self.pos_x,
            world_y=self.pos_y,
            target_x=target_x,
            target_y=target_y,
            rooms=self.player.rooms,
            damage=1
        )
        EnemyProjectiles.add(projectile)

#Enemies that can move
class SmartEnemy(BaseEnemy):
    def __init__(self, world_position, player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/PlayableCharacters/Patrick.png').convert_alpha()
        self.HP = 4
        self.gold_reward = 1
        self.move_speed = 0.8
        self.fire_range = 250
        self.vision_range = 600
        self.shot_cooldown = 0
        self.shot_cooldown_max = 720
        # aggro
        self.aggro = False
        self.memory_timer = 0
        self.memory_max = 300  # 3 seconds at 60 FPS
        # Dodge behavior
        self.dodge_timer = 0
        self.dodge_direction = random.choice([-1, 1])

    def can_move_to(self, x, y):
        enemy_width = self.rect.width
        enemy_height = self.rect.height
        half_w = enemy_width / 2
        half_h = enemy_height / 2
        corners = [
            (x - half_w, y - half_h),  # Top-left
            (x + half_w, y - half_h),  # Top-right
            (x - half_w, y + half_h),  # Bottom-left
            (x + half_w, y + half_h)   # Bottom-right
        ]
        for cx, cy in corners:
            tile = get_tile_at(cx, cy, self.player.rooms)
            if tile is None or tile == Rooms.W:
                return False
        return True

    def has_line_of_sight(self, target_x, target_y):
        distance = math.hypot(target_x - self.pos_x, target_y - self.pos_y)
        steps = max(1, int(distance / Rooms.Tile_Size) * 2)
        dx = (target_x - self.pos_x) / steps
        dy = (target_y - self.pos_y) / steps

        for i in range(1, steps):
            check_x = self.pos_x + dx * i
            check_y = self.pos_y + dy * i
            tile = get_tile_at(check_x, check_y, self.player.rooms)
            if tile == Rooms.W:
                return False
        return True

    def update(self, player_offset_x, player_offset_y):
        if not self.alive:
            return
        player_world_x = -self.player.PMove_X + (Screen_Width // 2)
        player_world_y = -self.player.PMove_Y + (Screen_Height // 2)
        dx = player_world_x - self.pos_x
        dy = player_world_y - self.pos_y
        dist = math.hypot(dx, dy)
        sees_player = dist <= self.vision_range and self.has_line_of_sight(player_world_x, player_world_y)
        if sees_player:
            self.aggro = True
            self.memory_timer = self.memory_max
        elif self.aggro and self.memory_timer > 0:
            self.memory_timer -= 1
        else:
            self.aggro = False
            self.memory_timer = 0
        if self.aggro:
            if dist > self.fire_range or not self.has_line_of_sight(player_world_x, player_world_y):
                if dist > 0.1:
                    step_dx = dx / dist * self.move_speed
                    step_dy = dy / dist * self.move_speed
                    new_x = self.pos_x + step_dx
                    new_y = self.pos_y + step_dy
                    # Try full diagonal move first
                    if self.can_move_to(new_x, new_y):
                        self.pos_x = new_x
                        self.pos_y = new_y
                    else:
                        # Try only x-axis
                        if self.can_move_to(new_x, self.pos_y):
                            self.pos_x = new_x
                        # Try only y-axis
                        elif self.can_move_to(self.pos_x, new_y):
                            self.pos_y = new_y
            else:
                # Dodge behavior
                if dist > 0.1:
                    angle = math.atan2(dy, dx)
                    perp_angle = angle + math.pi / 2 * self.dodge_direction
                    forward_dx = math.cos(angle) * self.move_speed * 0.3
                    forward_dy = math.sin(angle) * self.move_speed * 0.3
                    side_dx = math.cos(perp_angle) * self.move_speed * 0.7
                    side_dy = math.sin(perp_angle) * self.move_speed * 0.7
                    total_dx = forward_dx + side_dx
                    total_dy = forward_dy + side_dy
                    new_x = self.pos_x + total_dx
                    new_y = self.pos_y + total_dy
                    if self.can_move_to(new_x, new_y):
                        self.pos_x = new_x
                        self.pos_y = new_y
                    else:
                        # Try opposite dodge direction
                        alt_perp_angle = angle - math.pi / 2 * self.dodge_direction
                        side_dx = math.cos(alt_perp_angle) * self.move_speed * 0.7
                        side_dy = math.sin(alt_perp_angle) * self.move_speed * 0.7
                        total_dx = forward_dx + side_dx
                        total_dy = forward_dy + side_dy
                        new_x = self.pos_x + total_dx
                        new_y = self.pos_y + total_dy
                        if self.can_move_to(new_x, new_y):
                            self.pos_x = new_x
                            self.pos_y = new_y
                            # Flip dodge direction for next time
                            self.dodge_direction *= -1
                        else:
                            # Still blocked, try x or y only as last resort
                            if self.can_move_to(self.pos_x + total_dx, self.pos_y):
                                self.pos_x += total_dx
                            elif self.can_move_to(self.pos_x, self.pos_y + total_dy):
                                self.pos_y += total_dy

                self.dodge_timer += 1
                if self.dodge_timer > 60:
                    self.dodge_timer = 0
                    self.dodge_direction = random.choice([-1, 1])
                if dist <= self.fire_range and self.has_line_of_sight(player_world_x, player_world_y):
                    if self.shot_cooldown <= 0:
                        self.shoot_projectile(player_world_x, player_world_y)
                        self.shot_cooldown = self.shot_cooldown_max
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
        super().update(player_offset_x, player_offset_y)

class Evil_Totem(BaseEnemy):
    def __init__(self, world_position, player):
            super().__init__(world_position, player)
            self.image = pygame.image.load('Assets/Enemies/Turret.png').convert_alpha()
            self.HP = 2
class Default_Zombie(SmartEnemy):
    def __init__(self, world_position, player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Zombie.png').convert_alpha()
        self.HP = 4
class Armoured_Zombie(SmartEnemy):
    def __init__(self, world_position,player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Zombie_A.png').convert_alpha()
        self.HP = 6
        self.gold_reward = 2
class Skeleton_Archer(SmartEnemy):
    def __init__(self, world_position,player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Skeleton_archer.png').convert_alpha()
        self.HP = 4
        self.gold_reward = 2
class Skeleton_Warrior(SmartEnemy):
    def __init__(self, world_position,player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Skeleton_Warrior.png').convert_alpha()
        self.HP = 8            
        self.gold_reward = 4
class Crusader(SmartEnemy):
    def __init__(self, world_position,player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Crusader.png').convert_alpha()
        self.HP = 14
        self.gold_reward = 6
class Skeleton_Warlock(SmartEnemy):
    def __init__(self, world_position,player):
        super().__init__(world_position, player)
        self.image = pygame.image.load('Assets/Enemies/Skeletal_Warlock.png').convert_alpha()
        self.HP = 50
        self.gold_reward = 10
#Enemy Difficulty System
EnemyTiers = {
    "easy": [Default_Zombie, Evil_Totem],
    "medium": [Armoured_Zombie, Evil_Totem, Skeleton_Archer],
    "hard": [Skeleton_Archer, Armoured_Zombie, Skeleton_Warrior],
    "very_hard": [Skeleton_Warrior, Skeleton_Archer, Crusader],
    "boss": [Skeleton_Warlock]
}