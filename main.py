import pygame
from pygame.constants import KEYDOWN, KEYUP
from pygame.locals import QUIT
import Classes
import Rooms
import random

pygame.init()
ScreenHeight=720
ScreenWidth=1280
screen = Classes.screen
clock = pygame.time.Clock()
# --------------------- Button Creation Modules ---------------------
font=pygame.font.Font(None ,24)
Text_Colour=(255,255,255)
#function for the creation and centering of text at a position
def render_text(text, font, color, center):
    text_surf=font.render(text, True, color)
    text_rect=text_surf.get_rect(center=center)
    return text_surf, text_rect
#Function that uses the image of the button and the position, generates the rect and displays it on the screen
def create_button(image_path, position, text, font, color): 
    image = pygame.image.load(image_path) 
    image = pygame.transform.scale_by(image,2/3)
    rect = image.get_rect() 
    rect.topleft = position 
    text_surf, text_rect = render_text(text, font, color, rect.center)
    screen.blit(image, rect) 
    screen.blit(text_surf, text_rect)
    return rect
# --------------------- State Management ---------------
def main_loop():
    running = True
    current_state = "menu"
    class_choice = 1
    current_seed = None
    player_instance = None
    while running:
        if current_state == "menu":
            result = StartMenuState()
            if result == "customise":
                current_state = "customise"
            elif result == "controls":
                current_state = "controls"
        elif current_state == "controls":
            result = ControlsState()
            if result == "menu":
                current_state = "menu"
        elif current_state == "customise":
            result = GameCustomisationState()
            if result:
                current_seed, class_choice = result
                player_instance = None
                current_state = "play"
            else:
                current_state = "menu"
        elif current_state == "play":
            result, player_instance = PlayState(current_seed, class_choice, player_instance)
            if result == "next_floor":
                current_state = "play"
            else:
                current_state = "menu"

# --------------------- Start Menu ---------------------
def StartMenuState():
    screen.fill("black")
    #Play Button / Controls Button / Quit Button
    screen.blit(pygame.font.Font(None, 50).render("Cursed Crypts", True, (255,255,255)), (480, 100)) #displays title
    PButton_rect=create_button('Assets/OtherAssets/BlankButton.png',(480,250),"Play",font,Text_Colour) # displays play button
    CButton_rect=create_button('Assets/OtherAssets/BlankButton.png',(480,400),"Controls",font,Text_Colour) # displays controls button
    QButton_rect=create_button('Assets/OtherAssets/BlankButton.png',(480,550),"Quit",font,Text_Colour) # displays quit button
    pygame.display.flip()
    for event in pygame.event.get(): # checks for inputs from the player
        if event.type == pygame.QUIT: #close application button (x in top right)
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if PButton_rect.collidepoint(pygame.mouse.get_pos()):   #Play Button
                return "customise"
            if CButton_rect.collidepoint(pygame.mouse.get_pos()):   #Controls Button
                return "controls"
            if QButton_rect.collidepoint(pygame.mouse.get_pos()):   #Quit Button
                quit()
# --------------------- Main Menu ---------------------
def ControlsState():
    screen.fill("black")
    BackButton_rect=create_button("Assets/OtherAssets/BlankButton.png", (80,550),"Back", font, Text_Colour)
    controlimg=pygame.image.load("Assets/OtherAssets/BasicControls.png")
    controlimg=pygame.transform.scale_by(controlimg,2/3)
    screen.blit(controlimg, (500,100))
    pygame.display.flip()
    BackButtonLoop=True
    #Loops inputs to navigate away from Controls State
    while BackButtonLoop==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if BackButton_rect.collidepoint(pygame.mouse.get_pos()):
                    return "menu"
# --------------------- Game Customisation --------------------- 
Class_Displays = ['Assets/OtherAssets/Warrior_Display.png', 'Assets/OtherAssets/Mage_Display.png', 'Assets/OtherAssets/Assassin_Display.png']
def GameCustomisationState():
     PositionInFile=0
     input_active=False #Seed Input Loop
     SelectionLoop=True #State Loop
     global ClassChoice
     ClassChoice=1
     user_input="Set Seed" #user_input = seed when entered
     while SelectionLoop == True:
        seed=""
        screen.fill("black")
        # Creation of Buttons
        screen.blit(pygame.font.Font(None, 50).render("Customise your game", True, (255,255,255)), (480, 100))
        SeedInputButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (80,100),user_input,font,Text_Colour)
        LoadSeedButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (80, 250), "Load Previous Seeds", font, Text_Colour)
        StartButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (80,400),"Start",font,Text_Colour)
        BackButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (80,550),"Back", font, Text_Colour)
        #Button Text for playable classes being either Select or Selected based on if a class is currently selected.
        if ClassChoice==1:
            WText="Selected"
        else:
            WText="Select"
        if ClassChoice==2:
            MText="Selected"
        else:
            MText="Select"
        if ClassChoice==3:
            AText="Selected"
        else:
            AText="Select"
        ClassCount = 1
        for image_path in Class_Displays:
            image = pygame.image.load(image_path) 
            image = pygame.transform.scale_by(image,2/3)
            rect = image.get_rect() 
            rect.topleft = 80+(300*ClassCount),200
            ClassCount+=1  
            screen.blit(image, rect)
        WarriorClassButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (380, 550), WText, font, Text_Colour)
        MageClassButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (680, 550), MText, font, Text_Colour)
        AssassinClassButton_rect=create_button('Assets/OtherAssets/BlankButton.png', (980, 550), AText, font, Text_Colour)
        #End of playable classes buttons
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                quit()
            
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            #Button that starts the game
                if StartButton_rect.collidepoint(pygame.mouse.get_pos()):
                    print("Started Button Pressed")
                    SelectionLoop=False
                    seed=user_input
                    if seed.isdigit()==False: #Validation for seed
                        seed=random.randrange(1,100000)
                    #Opens SeedsPlayed text file, appends the used seed
                    with open('SeedsPlayed.txt', 'a') as file:
                        file.write(str(seed) + '\n')
                    return (int(seed), ClassChoice)

            #Button enables manual seed input
                if SeedInputButton_rect.collidepoint(pygame.mouse.get_pos()):
                    input_active=True
                    user_input=""
                
            #Button that reads a file and loads a seed from the file
                if LoadSeedButton_rect.collidepoint(pygame.mouse.get_pos()):
                    with open('SeedsPlayed.txt', 'r') as file:
                        lines = file.readlines()
                        if len(lines)==0:
                            user_input="No Previous Seed"
                        else:
                            user_input=lines[PositionInFile].strip()
                            PositionInFile+=1
                            if PositionInFile==len(lines):    # Prevents index Error
                                PositionInFile=0
                if BackButton_rect.collidepoint(pygame.mouse.get_pos()):
                    return
                if WarriorClassButton_rect.collidepoint(pygame.mouse.get_pos()):
                    ClassChoice=1
                    print("Warrior Class Selected")
                if MageClassButton_rect.collidepoint(pygame.mouse.get_pos()):
                    ClassChoice=2
                    print("Mage Class Selected")
                if AssassinClassButton_rect.collidepoint(pygame.mouse.get_pos()):
                    ClassChoice=3
                    print("Assassin Class Selected")
                            
            #Input Detection for Manually entering Seed.
            if event.type==pygame.KEYDOWN and input_active==True:
                if event.key==pygame.K_RETURN:
                    #Stops the Player from continuing to type into the seed, sets the new seed
                    print("Seed Input: ", user_input)
                    input_active=False
                elif event.key==pygame.K_BACKSPACE:
                    user_input= user_input[:-1] #Player removes character from seed
                elif event.unicode.isdigit():
                    user_input += event.unicode #Player enters Character for seed

#------------ Game Over
def GameOver(RealPlayer, Condition):
    screen.fill("black")
    BackButton_rect=create_button("Assets/OtherAssets/BlankButton.png", (80,550),"Back", font, Text_Colour)
    GameOverimg=pygame.image.load("Assets/OtherAssets/GameOverDisplay.png")
    screen.blit(GameOverimg, (400,100))
    #-- PowerUps
    screen.blit(font.render(str(RealPlayer.SPU), True, (255,255,255)), (500, 295))
    screen.blit(font.render(str(RealPlayer.ASPU), True, (255,255,255)), (500, 350))
    screen.blit(font.render(str(RealPlayer.DPU), True, (255,255,255)), (500, 410))
    #--
    screen.blit(font.render(str(Condition), True, (255,255,255)), (700, 205))
    #-- Other Stats Measured
    screen.blit(font.render(str(RealPlayer.currentfloor), True, (255,255,255)), (880, 260))
    pygame.display.flip()
    BackButtonLoop=True
    #Loops inputs to navigate away from Controls State
    while BackButtonLoop==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                if BackButton_rect.collidepoint(pygame.mouse.get_pos()):
                    return "menu"

#------------       All Modules within the Play State       ------------
#KeyDown + KeyUp actions dictate the player's ability to move
KeyDown_actions={   # Dictionary of KeyDown actions (PlayState)
    pygame.K_e: lambda player: player.check_interact(), 
    pygame.K_w: lambda player: setattr(player, 'Upress', True),
    pygame.K_s: lambda player: setattr(player, 'Dpress', True),
    pygame.K_a: lambda player: setattr(player, 'Lpress', True),
    pygame.K_d: lambda player: setattr(player, 'Rpress', True)
}

KeyUp_actions={ # Dictionary of KeyUp actions (PlayState)
    pygame.K_w:lambda player:setattr(player,'Upress',False),
    pygame.K_s:lambda player:setattr(player,'Dpress',False),
    pygame.K_a:lambda player:setattr(player,'Lpress',False),
    pygame.K_d:lambda player:setattr(player,'Rpress',False)
}

#displays the map on screen. PMove X and Y act as an offset value
market_offset=0
def render_map(seed, PMove_X, PMove_Y, market_offset, RealPlayer):
    screen.fill("black")  # Ensures old floor is not rendered
    if generated_rooms:  # Only render if there's a valid layout
        for room, pos in generated_rooms:
            room_offset_x, room_offset_y = pos
            room_offset_x += PMove_X
            room_offset_y += PMove_Y

            # Draw only visible rooms
            if -(len(room[1]) * 40) <= room_offset_x <= ScreenWidth and -(len(room) * 40) <= room_offset_y <= ScreenHeight:
                for y, row in enumerate(room):
                    for x, tile_type in enumerate(row):
                        screen_x = x * Rooms.Tile_Size + room_offset_x
                        screen_y = y * Rooms.Tile_Size + room_offset_y
                        if tile_type == Rooms.F or tile_type == Rooms.D or tile_type == Rooms.E:
                            screen.blit(Rooms.F_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.W:
                            screen.blit(Rooms.W_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.C_C:
                            screen.blit(Rooms.CC_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.O_C:
                            screen.blit(Rooms.OC_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.L_C:
                            screen.blit(Rooms.LC_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.St:
                            screen.blit(Rooms.S_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.M:
                            marketchoice = int(RealPlayer.base_seed) + x + y + RealPlayer.currentfloor
                            random.seed(marketchoice)
                            powerup = random.choice(["SpeedPowerUp", "DamagePowerUp", "AttackSpeedPowerUp"])
                            market_offset += 1
                            # Draw market tile image
                            market_image = pygame.image.load(f"Assets/Tiles/Market_{powerup}.png").convert_alpha()
                            market_image = pygame.transform.scale(market_image, (Rooms.Tile_Size, Rooms.Tile_Size))
                            screen.blit(market_image, (screen_x, screen_y))
                            cost = 4 + RealPlayer.currentfloor
                            # Draw cost text centered over the tile
                            cost_font = pygame.font.Font(None, 20)
                            cost_text = cost_font.render(str(cost), True, (255, 255, 0))  # Yellow for visibility
                            cost_rect = cost_text.get_rect(center=(screen_x + Rooms.Tile_Size // 2, screen_y + Rooms.Tile_Size // 2))
                            screen.blit(cost_text, cost_rect)

                        elif tile_type == Rooms.TrapA:
                            screen.blit(Rooms.TrapA_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.TrapB:
                            screen.blit(Rooms.TrapB_Image, (screen_x, screen_y))
                        elif tile_type == Rooms.TrapC:
                            screen.blit(Rooms.TrapC_Image, (screen_x, screen_y))

def spawn_enemies_and_traps(rooms, player, seed):
    from Classes import Enemies, TrapTile, EnemyTiers
    Enemies.empty()
    Classes.EnemyProjectiles.empty()
    Classes.Projectiles.empty()
    trap_tiles = []
    for room, pos in rooms:
        room_offset_x, room_offset_y = pos
        # Detect if this is the boss room based on known dimensions and wall layout
        is_boss_room = False
        if len(room) == 13 and len(room[0]) == 13:
            # Check for corner walls in known boss room positions
            try:
                has_corner_walls = all(room[y][x] == Rooms.W for y, x in [(4, 4), (4, 9), (9, 4), (9, 9)])
                if has_corner_walls:
                    is_boss_room = True
                    print("Boss room detected!")
            except IndexError:
                pass  # Failsafe

        for y, row in enumerate(room):
            for x, tile in enumerate(row):
                if tile in [Rooms.TrapA, Rooms.TrapB, Rooms.TrapC]:
                    trap_tiles.append(TrapTile(room, x, y, pos))

                elif tile == Rooms.E:
                    enemy_x = room_offset_x + x * Rooms.Tile_Size
                    enemy_y = room_offset_y + y * Rooms.Tile_Size

                    if is_boss_room:
                        if x == 6 and y == 6:
                            print("Spawning Skeleton_Warlock in boss room center.")
                            enemy_class = Classes.Skeleton_Warlock
                            enemy = enemy_class((enemy_x, enemy_y), player)
                            Enemies.add(enemy)
                    else:
                        if player.currentfloor <= 2:
                            tier = "easy"
                        elif player.currentfloor <= 4:
                            tier = "medium"
                        elif player.currentfloor <= 6:
                            tier = "hard"
                        else:
                            tier = "very_hard"
                        tile_seed = hash(f"{seed}-{player.currentfloor}-{x}-{y}")
                        random.seed(tile_seed)
                        enemy_class = random.choice(EnemyTiers[tier])
                        enemy = enemy_class((enemy_x, enemy_y), player)
                        Enemies.add(enemy)

    player.set_rooms(rooms)
    return trap_tiles


def PlayState(seed, class_choice, RealPlayer=None):
    from Classes import Enemies
    global generated_rooms

    # --- Create or reuse player instance ---
    SelectableClass = [Classes.Player, Classes.Warrior, Classes.ArmouredMage, Classes.Assassin]
    if RealPlayer is None:
        RealPlayer = SelectableClass[class_choice](ScreenWidth // 2, ScreenHeight // 2)
        RealPlayer.base_seed = int(seed)
        RealPlayer.currentfloor = 1

    # --- Generate new dungeon floor based on current floor ---
    screen.fill("black")
    floor_seed = RealPlayer.base_seed + RealPlayer.currentfloor
    Boss = RealPlayer.currentfloor % 5 == 0  # Boss every 5 floors
    generated_rooms = Rooms.GenRooms(floor_seed, Boss)

    # --- Spawn traps and enemies ---
    trap_tiles = spawn_enemies_and_traps(generated_rooms, RealPlayer, seed)

    # --- Position player in new spawn room ---
    for room, pos in generated_rooms:
        if room == Rooms.SpawnRoom:
            start_x = pos[0] + (len(room[0]) // 2) * Rooms.Tile_Size
            start_y = pos[1] + (len(room) // 2) * Rooms.Tile_Size
            RealPlayer.rect.topleft = (start_x, start_y)
            break

    RealPlayer.set_rooms(generated_rooms)
    RealPlayer.PMove_X, RealPlayer.PMove_Y = 0, 0
    RealPlayer.update()

    GameActive = True
    while GameActive:
        dt = clock.tick(144)
        # Trap logic
        for trap in trap_tiles:
            trap.update(dt, RealPlayer)
        # --- Check player death ---
        if RealPlayer.Hp <= 0:
            GameOver(RealPlayer, "Defeat")
            return "defeat", RealPlayer
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                action = KeyDown_actions.get(event.key)
                if action:
                    result = action(RealPlayer)
                    if result == "next_floor":
                        return "next_floor", RealPlayer
            if event.type == pygame.KEYUP:
                action = KeyUp_actions.get(event.key)
                if action:
                    action(RealPlayer)
        # --- Render loop ---
        screen.fill("black")
        render_map(seed, RealPlayer.PMove_X, RealPlayer.PMove_Y, market_offset, RealPlayer)

        PlayerHealth_Image = pygame.image.load(RealPlayer.HealthBarSprites[RealPlayer.Hp])
        screen.blit(pygame.transform.scale(PlayerHealth_Image, (260, 30)), (10, 10))
        screen.blit(font.render(str(RealPlayer.Gold), True, (255, 255, 255)), (80, 65))
        screen.blit(font.render(str(RealPlayer.SPU), True, (255, 255, 255)), (270, 15))
        screen.blit(font.render(str(RealPlayer.DPU), True, (255, 255, 255)), (370, 15))
        screen.blit(font.render(str(RealPlayer.ASPU), True, (255, 255, 255)), (470, 15))

        # Update player and projectiles
        RealPlayer.update()
        Classes.Projectiles.update(RealPlayer.PMove_X, RealPlayer.PMove_Y)
        Enemies.update(RealPlayer.PMove_X, RealPlayer.PMove_Y)
        # If boss is defeated, place stairs in boss room
        if RealPlayer.currentfloor % 5 == 0 and len(Enemies) == 0:
            for idx, (room, pos) in enumerate(generated_rooms):
                # Detect boss room by dimensions and layout (not by object identity)
                if len(room) == 13 and len(room[0]) == 13:
                    # Confirm boss layout by wall tiles in the corners
                    if all(room[y][x] == Rooms.W for (y, x) in [(4,4), (4,9), (9,4), (9,9)]):
                        center_x = len(room[0]) // 2
                        center_y = len(room) // 2

                        if room[center_y][center_x] != Rooms.St:
                            room[center_y][center_x] = Rooms.St
                            print("Stairs have been spawned in the boss room!")


        Classes.EnemyProjectiles.update(RealPlayer.PMove_X, RealPlayer.PMove_Y)

        # Handle collisions
        for projectile in list(Classes.Projectiles):
            hit_enemies = pygame.sprite.spritecollide(projectile, Enemies, False)
            for enemy in hit_enemies:
                if projectile.type_name == "poison":
                    enemy.take_damage(projectile.damage)  # initial hit
                    enemy.apply_poison(projectile.damage)
                else:
                    enemy.take_damage(projectile.damage)
                projectile.kill()

        # Poison ticking logic
        for projectile in list(Classes.Projectiles):
            if projectile.type_name == "poison" and projectile.poison_applied:
                now = pygame.time.get_ticks()
                if now - projectile.spawn_time >= projectile.tick_interval:
                    projectile.spawn_time = now
                    if projectile.poison_ticks > 0 and projectile.target and projectile.target.alive:
                        projectile.target.take_damage(projectile.damage // 5)
                        projectile.poison_ticks -= 1
                    else:
                        projectile.kill()

        for enemy_proj in Classes.EnemyProjectiles:
            player_rect = pygame.Rect(ScreenWidth // 2, ScreenHeight // 2, RealPlayer.rect.width, RealPlayer.rect.height)
            if enemy_proj.rect.colliderect(player_rect):
                RealPlayer.take_damage(1)
                enemy_proj.kill()

        pygame.display.flip()

        # Mouse click = shoot
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            RealPlayer.shoot(mouse_x, mouse_y)

    # If player somehow escapes loop
    GameOver(RealPlayer, "Defeat")
    return "defeat", RealPlayer


if __name__ == "__main__":
    pygame.display.set_caption("Cursed Crypts")
    main_loop()