import pygame
import random
import copy
pygame.display.set_mode((1280, 720))
#Dungeon rooms generated via tiles
MaxRooms=10
Tile_Size = 40
B,F,W,D,E,St,M = -1,0,1,2,3,4,5  #Blank/Floor/Wall/Door/Enemy/Stairs/Market
O_C,C_C,L_C = 6,7,8 # all chest states
TrapA, TrapB, TrapC = 9,10,11 # all trap states
S,G = 0,1   #Defines if the generation is Single (S) or Group (G)
#Images representing tiles
F_Image = pygame.image.load('Assets/Tiles/Floor1.png').convert_alpha()
W_Image = pygame.image.load('Assets/Tiles/Wall1.png').convert_alpha()
CC_Image = pygame.image.load('Assets/Tiles/ChestClosed.png').convert_alpha()
OC_Image = pygame.image.load('Assets/Tiles/ChestLoot.png').convert_alpha()
LC_Image = pygame.image.load('Assets/Tiles/ChestEmpty.png').convert_alpha()
S_Image = pygame.image.load('Assets/Tiles/StairTile.png').convert_alpha()
TrapA_Image = pygame.image.load('Assets/Trap/TrapInactive.png').convert_alpha()
TrapB_Image = pygame.image.load('Assets/Trap/TrapArmed.png').convert_alpha()
TrapC_Image = pygame.image.load('Assets/Trap/TrapActive.png').convert_alpha()
Images = [F_Image, W_Image, CC_Image, OC_Image, LC_Image, TrapA_Image, TrapB_Image, TrapC_Image]
for Image in Images:
    Image= pygame.transform.scale(Image,(Tile_Size,Tile_Size))
#Rooms
def CreateRoom(RoomNameSys, DimensionsOfRoom, OtherTilePos):
    for y in range(DimensionsOfRoom[0]): # Height of Room
        RoomNameSys.append([])
        for x in range(DimensionsOfRoom[1]): #Length of Room
            if y==0 or y==DimensionsOfRoom[0]-1:
                RoomNameSys[y].append(W)
            elif x==0 or  x==DimensionsOfRoom[1]-1:
                RoomNameSys[y].append(W)
            else:
                RoomNameSys[y].append(F)
    for Positions in OtherTilePos:
        Tile=Positions[2]
        if Positions[3]==G:
            for y in range(Positions[4]):
                for x in range(Positions[5]):
                    RoomNameSys[Positions[0]+y-1][Positions[1]+x-1]=Tile
            # e.g (RoomNameSys,  (7,7),[(7,4,D,S),(3,3,B,G,3,3)]) would be a 7x7 room, a single door placed at 7,4. Blank tiles set as a group 3x3 area beginning at 3,3.
        elif Positions[3]==S:
            RoomNameSys[Positions[0]-1][Positions[1]-1]=Tile
    return RoomNameSys
SpawnRoom, StairRoom_End, Boss_Room, HRoom, VRoom, TpedC, BigRoom, TRoom1, TRoom2, QuadRoom, Corridor_H, Corridor_V, Corridor_T, Corridor_CornerL, Market =[],[],[],[],[],[],[],[],[],[],[],[],[],[], []
#RoomNameSys / Dimensions of room / every tile change after floors and walls (exterior)
SpawnRoom=CreateRoom(SpawnRoom, (7,7), [(7,4,D,S), (4,7,D,S)])
StairRoom_End=CreateRoom(StairRoom_End, (7,7), [(7,4,D,S), (4,7,D,S), (1,4,D,S), (4,1,D,S), (4,4,St,S)])
Boss_Room=CreateRoom(Boss_Room, (13,13), [(7,1,D,S), (13,7,D,S), (1,4,D,S), (8,13,D,S), (4,4,W,G,2,2), (7,7,E,S), (9,4,W,G,2,2), (4,9,W,G,2,2), (9,9,W,G,2,2)])
HRoom=CreateRoom(HRoom, (7,10), [(4,1,D,S), (4,10,D,S),(1,3,D,S),(7,8,D,S), (4,5,E,S)])
VRoom=CreateRoom(VRoom, (7,7), [(1,4,D,S), (7,4,D,S), (4,4,E,S)])
BigRoom=CreateRoom(BigRoom, (8,12), [(4,1,D,S), (8,8,D,S), (4,6,E,S)])
TRoom1=CreateRoom(TRoom1, (7,7), [(1,4,D,S),(4,7,D,S),(7,4,D,S), (4,4,E,S)])
TRoom2=CreateRoom(TRoom2, (7,7), [(1,4,D,S),(7,4,D,S),(4,7,D,S), (3,3,E,S)])
QuadRoom=CreateRoom(QuadRoom, (7,7), [(1,4,D,S),(4,1,D,S),(4,7,D,S),(7,4,D,S), (4,4,E,S)])
Corridor_H=CreateRoom(Corridor_H, (5,9), [(3,1,D,S),(3,9,D,S),(3,3,E,S),(3,7,E,S)])
Corridor_V=CreateRoom(Corridor_V, (9,5), [(1,3,D,S),(9,3,D,S),(3,3,E,S),(7,3,E,S)])
TpedC=CreateRoom(TpedC, (10,12), [(3,1,D,S), (8,12,D,S), (7,4,W,G,3,1), (2,5,W,G,3,1),(2,9,W,G,3,1),(4,6,TrapA,G,1,3),(2,7,C_C,S), (5,5,E,S)])
Corridor_T=CreateRoom(Corridor_T, (9,9), [(3,1,D,S),(3,9,D,S),(9,5,D,S),(5,1,W,G,5,3),(6,1,B,G,4,2),(5,7,W,G,5,3),(6,8,B,G,4,2), (4,5,E,S)])
Corridor_CornerL=CreateRoom(Corridor_CornerL, (9,9), [(1,3,D,S),(7,9,D,S),(1,5,W,G,5,5),(1,6,B,G,4,4), (5,3,E,S)])
Market=CreateRoom(Market, (9,9), [(5,0,D,S),(5,9,D,S),(0,5,D,S),(9,5,D,S),(5,5,M,S)])
#Rooms that can be selected during generation
AllRooms = [HRoom, VRoom, BigRoom, TpedC, QuadRoom, TRoom1, TRoom2, Corridor_V, Corridor_H, Corridor_CornerL, Corridor_T,Market]
screen_width, screen_height = 1280, 720
spawn_room_width = len(SpawnRoom[0]) * Tile_Size
spawn_room_height = len(SpawnRoom) * Tile_Size
center_x = (screen_width - spawn_room_width) // 2
center_y = (screen_height - spawn_room_height) // 2
# Room Generating - using backtracking to ensure all rooms can generate
def GenRooms(seed, Boss, attempt=0, max_attempts=10):
    if attempt >= max_attempts:  # Stop recursion if it fails too many times
        print("Failed to generate dungeon after multiple attempts.")
        return [(copy.deepcopy(SpawnRoom), (center_x, center_y))]  # Default fallback
    random.seed(seed)
    rooms = [(copy.deepcopy(SpawnRoom), (center_x, center_y))]
    room_stack = [(copy.deepcopy(SpawnRoom), (center_x, center_y))]  
    placed_rooms = 1
    Current_Pos = (center_x, center_y)

    while placed_rooms < MaxRooms:
        if placed_rooms == MaxRooms - 1:
            if Boss==True:
                NRoom = copy.deepcopy(Boss_Room)
            else:
                NRoom = copy.deepcopy(StairRoom_End)  # Ensure Stairs Room is last
        else:
            NRoom = copy.deepcopy(random.choice(AllRooms))
        backtrack = False  
        for attempt in range(10):  
            New_Pos = FindNRoomPos(NRoom, Current_Pos, rooms[-1][0], rooms)
            if New_Pos is not None:  
                rooms.append((NRoom, New_Pos))  
                room_stack.append((NRoom, New_Pos))  
                Current_Pos = New_Pos  
                placed_rooms += 1
                print(f"Room {NRoom} placed at {New_Pos}")
                break  
        else:  # If all attempts fail, backtrack
            print(f"Failed to place room at {New_Pos}")
            if len(room_stack) > 1:
                print(f"Backtracking, removing room at {room_stack[-1][1]}")
                room_stack.pop()
                rooms.pop()
                Current_Pos = room_stack[-1][1]
                placed_rooms -= 1
    ReplaceUnusedDoors(rooms)
    return rooms  

def ReplaceUnusedDoors(rooms):
    # Create a set to store door positions globally
    door_positions = set()
    room_positions = {}
    #Collect all door positions
    for room, (room_x, room_y) in rooms:
        for y in range(len(room)):
            for x in range(len(room[0])):
                if room[y][x] == D:
                    door_x = room_x + x * Tile_Size
                    door_y = room_y + y * Tile_Size
                    door_positions.add((door_x, door_y))
                    room_positions[(door_x, door_y)] = (room, x, y)  # Store room reference
    #Replace unused doors
    for (door_x, door_y), (room, local_x, local_y) in room_positions.items():
        adjacent_positions = {
            "top": (door_x, door_y - Tile_Size),
            "bottom": (door_x, door_y + Tile_Size),
            "left": (door_x - Tile_Size, door_y),
            "right": (door_x + Tile_Size, door_y)
        }
        connected = any(pos in door_positions for pos in adjacent_positions.values())
        #If door is not connected, turn it into a wall
        if not connected:
            room[local_y][local_x] = W

def FindNRoomPos(NRoom, Current_Pos, CurrentRoom, rooms):
    current_room_Doors, current_doorpos = GetDoorPosition(CurrentRoom)  # Get doors from current room
    new_room_Doors, new_doorpos = GetDoorPosition(NRoom)  # Get doors from the new room
    if not current_room_Doors or not new_room_Doors:
        return None  # No valid doors to connect
    for current_Door in current_room_Doors:
        for new_Door in new_room_Doors:
            new_pos = None
            if current_Door == "top" and new_Door == "bottom":
                for x in range(len(CurrentRoom[0])):
                    if CurrentRoom[0][x] == D:
                        for new_x in range(len(NRoom[0])):
                            if NRoom[-1][new_x] == D:
                                new_pos = (Current_Pos[0] + (x - new_x) * Tile_Size, Current_Pos[1] - len(NRoom) * Tile_Size)
                                break
            elif current_Door == "bottom" and new_Door == "top":
                for x in range(len(CurrentRoom[0])):
                    if CurrentRoom[-1][x] == D:
                        for new_x in range(len(NRoom[0])):
                            if NRoom[0][new_x] == D:
                                new_pos = (Current_Pos[0] + (x - new_x) * Tile_Size, Current_Pos[1] + len(CurrentRoom) * Tile_Size)
                                break
            elif current_Door == "left" and new_Door == "right":
                for y in range(len(CurrentRoom)):
                    if CurrentRoom[y][0] == D:
                        for new_y in range(len(NRoom)):
                            if NRoom[new_y][-1] == D:
                                new_pos = (Current_Pos[0] - len(NRoom[0]) * Tile_Size, Current_Pos[1] + (y - new_y) * Tile_Size)
                                break
            elif current_Door == "right" and new_Door == "left":
                for y in range(len(CurrentRoom)):
                    if CurrentRoom[y][-1] == D:
                        for new_y in range(len(NRoom)):
                            if NRoom[new_y][0] == D:
                                new_pos = (Current_Pos[0] + len(CurrentRoom[0]) * Tile_Size, Current_Pos[1] + (y - new_y) * Tile_Size)
                                break

            if new_pos is not None:
                # Create a Rect for the new room
                new_room_rect = pygame.Rect(
                    new_pos[0], new_pos[1], 
                    len(NRoom[0]) * Tile_Size, 
                    len(NRoom) * Tile_Size
                )
                # Check for collisions with existing rooms
                collision = any(
                    new_room_rect.colliderect(pygame.Rect(pos[0], pos[1], len(room[0]) * Tile_Size, len(room) * Tile_Size))
                    for room, pos in rooms
                )
                if not collision:
                    print(f"New room position: {new_pos}")
                    return new_pos  # Found a valid position
                else:
                    print(f"Collision Detected: {new_room_rect} with {CurrentRoom}")
    return None  # No valid position found, backtracking needed
#Used to check for available Door positions + branch rooms in different directions
def GetDoorPosition(CurrentRoom):
    AvailableDoors = []
    DoorPositions = {"top": [None,None], "bottom": [None,None], "left": [None,None], "right": [None,None]}
    for y in range(len(CurrentRoom)):
        for x in range(len(CurrentRoom[0])):
            if CurrentRoom[y][x] == D:
                #Checks roughly where the Door is located to determine what side of the room it is on
                #Allows it to be later called to in order to align and generate rooms in suitable directions.
                if y == 0:
                    AvailableDoors.append("top")
                    DoorPositions["top"]=(x,y)
                elif y == len(CurrentRoom) - 1:
                    AvailableDoors.append("bottom")
                    DoorPositions["bottom"]=(x,y)
                elif x == 0:
                    AvailableDoors.append("left")
                    DoorPositions["left"]=(x,y)
                elif x == len(CurrentRoom[0]) - 1:
                    AvailableDoors.append("right")
                    DoorPositions["right"]=(x,y)
    if len(AvailableDoors) == 0:
        #No Available Doors -Shouldn't be possible but acts as validation
        return None
    else:
        random.shuffle(AvailableDoors) #Randomly selects 1 of the available Doors and returns it.
        #Enables the same room type to generate in different directions.
        return AvailableDoors, DoorPositions