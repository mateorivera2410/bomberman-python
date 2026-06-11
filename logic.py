import objects as obb
import time
import random 
import json,os
def establish_world (rows:int,cols:int):
    """ establsih the bombberman map

    args: 
    -num_rows (int): the numbers of rows in the world
    -num_cols: numbers of cols in the world

    return: 

    list[list]: The bomberman world   
    
    """

    response = []

    for i in range (rows): 
            response.append([])
            for j in range (cols):
                response[i].append(obb.SPACE)

    return response
def show_world (world,cols):
    upper_border = "╔" + ("═"*cols) + "╗"
    print (upper_border)
    for i in range (len(world)):
        print ( "║" +"" .join(world[i]) + "║")
    lower_border =  "╚" + ("═"*cols) + "╝"
    print (lower_border) 
    
def available_positions (world,rows:int,cols:int):
    available_positions = []
    for i in range (rows):
        for j in range (cols):
            if world [i][j] == obb.SPACE:
                available_positions.append((i,j))
    return available_positions 
player_pos=[]
def add_player (world,available_positions): 
    player_pos = random.randint(0,len(available_positions)-1)
    pos = available_positions.pop(player_pos)
    world[pos[0]][pos[1]] = obb.PLAYER_ICON
    return world, available_positions,pos

def add_enemies (world,available_positions):
    random_pos = random.randint(0,len(available_positions)-1)
    pos = available_positions.pop(random_pos)
    world[pos[0]][pos[1]] = "O"

    return world, available_positions

def move_enemies (world,rows,cols): 
    directions= [(1,0), (-1,0), (0,1), (0,-1)]
    new_enemies_position = []

    for i in range (rows):
        for j in range (cols):
            if world [i][j] == "O":
                random_direction = random.choice(directions)
                new_pos_enemie_x = i + random_direction[0]
                new_pos_enemie_y = j + random_direction[1]
                if not (0 <= new_pos_enemie_x < rows and 0 <= new_pos_enemie_y < cols):
                    new_enemies_position.append((i, j))
                    continue
                    
                if (0 <= new_pos_enemie_x < rows and 0 <= new_pos_enemie_y < cols and world [new_pos_enemie_x][new_pos_enemie_y] in (obb.SPACE, obb.PLAYER_ICON)):
                    if world [new_pos_enemie_x][new_pos_enemie_y] == obb.PLAYER_ICON:
                        print ("you died by an enemy")
                        return "you_died"
                    world [i][j] = obb.SPACE
                    world [new_pos_enemie_x][new_pos_enemie_y] = "O"
                    new_enemies_position.append((new_pos_enemie_x,new_pos_enemie_y))
            else: 
                new_enemies_position.append((i,j))
    return "continue"

def explote_bomb (world,bomb_pos,rows,cols):
    explosion_area = [
        bomb_pos,
        (bomb_pos[0]-1, bomb_pos[1]),
        (bomb_pos[0]+1, bomb_pos[1]),
        (bomb_pos[0], bomb_pos[1]-1),
        (bomb_pos[0], bomb_pos[1]+1)
    ]
    
    for(i,j) in explosion_area:
        if 0 <= i < rows and 0 <= j < cols:
            if world [i][j] == obb.PLAYER_ICON:

                world[i][j] = obb.FLAME
                return "you_died"
            elif world [i][j]!= (obb.WALLS, obb.BOX):
                world [i][j] = obb.FLAME

    show_world(world,cols)
    time.sleep(0.7)

    

    for (x, y) in explosion_area:
        if 0 <= x < rows and 0 <= y < cols:
            if world [x][y] in (obb.BOX, obb.WALLS, obb.BOMB,obb.FLAME,"O"): 
                world [x][y] = obb.SPACE   
 
         
def move_player (world,pos,rows,cols): 
    movements = {
        "W": (-1,0),
        "S": (1,0),
        "A": (0,-1),
        "D": (0,1)
    }
    last_direction = (0,1)
    flag1= True
    active_bombs = []
    while flag1:
        show_world(world,cols)

        
        current_time = time.time()
        for bomb_pos, placed_time in active_bombs[:]:
            if current_time - placed_time >= 0.5:  
                world [bomb_pos[0]][bomb_pos[1]] = obb.FLAME
                result=explote_bomb(world, bomb_pos, rows, cols)
                print(f"Bomb at {bomb_pos} exploded!")
                active_bombs.remove((bomb_pos, placed_time))
                if result == "you_died":
                    return "you_died",pos
        instruccion = input ("""
        -W: UP
        -S: DOWN
        -A: LEFT
        -D: RIGHT
        -B: BOMB
        -E: EXIT

    Option: """).upper()
        if movements.get(instruccion):
            move = movements[instruccion]
            last_direction = move
            new_pos = (pos[0]+ move [0], pos [1] + move [1])
            if (0 <= new_pos[0] < rows) and (0 <= new_pos[1]<cols):
        
                    
                if world [new_pos[0]][new_pos[1]] in obb.DOOR:
                    print ("you found the door, next level")
                    return "next_level",pos
                elif  world [new_pos[0]][new_pos[1]] in "O":
                    
                    print ("you died")
                    return "you_died",pos
                elif world[new_pos[0]][new_pos[1]] in "+":
                    print ("you died")
                    return "you_died",pos
                if world [new_pos[0]][new_pos[1]] not in (obb.BOX,obb.WALLS): 
                    world[pos[0]][pos[1]] = obb.SPACE
                    pos = new_pos
                    world[new_pos[0]][new_pos[1]] = obb.PLAYER_ICON
                    print (f"nueva posicion: {pos}")
                
                               
                else: 
                    print (f"No puedes pasar, hay un obstaculo.")
            else: 
                print (f"movimiento fuera del mapa")
        elif instruccion  == "B":
            bomb_pos = (pos[0] + last_direction[0], pos[1] + last_direction[1])
            if 0 <= bomb_pos [0] < rows and 0 <= bomb_pos [1] < cols:
                if world [bomb_pos[0]][bomb_pos[1]]== obb.SPACE:
                 world [bomb_pos[0]][bomb_pos [1]] = obb.BOMB 

                 print (f"You put a bomb") 
                 active_bombs.append((bomb_pos,time.time())) 
                 show_world(world,cols)
                 
                 print (f"bomb exploted") 
                if world [bomb_pos[0]][bomb_pos[1]]== obb.PLAYER_ICON:
                    print ("you died")
                    return "you_died",pos
                 #show_world(world,cols)
                 

                else:
                    print (f"you cant put a bomb here") 
            else: 
                print (f"you cant put a bomb outside the map")
        elif instruccion == "E" :
            flag1 = False 
            return "exit",pos
        
        enemy_result = move_enemies(world,rows,cols)
        if enemy_result == "you_died":
            return "you_died",pos
    return "continue",pos



def add_boxes (world,available_positions):
    random_pos = random.randint(0,len(available_positions)-1)
    pos = available_positions.pop(random_pos)
    world[pos[0]][pos[1]] = obb.BOX
    
    return world,available_positions
def add_walls (world,available_positions): 
    
    random_pos = random.randint(0,len(available_positions)-1)
    pos = available_positions.pop(random_pos)
    world[pos[0]][pos[1]] = obb.WALLS
    return world,available_positions
def add_door (world,available_positions): 
    for i in range (1): 
        random_pos = random.randint(0,len(available_positions)-1)
        pos = available_positions.pop(random_pos)
        world[pos[0]][pos[1]] = obb.DOOR
    return world,available_positions

def save_game (username,level,world,player_pos,rows,cols):
    save_data ={
        "level" : level,
        "rows" : rows,
        "cols" : cols,
        "player_pos" : player_pos,
        "world" : world
    }
    os.makedirs("saves", exist_ok = True)
    number = 1
    while os.path.exists(f"saves/{username}_{number}.json"):
        number += 1
    filepath = f"saves/{username}_{number}.json"
    with open(filepath, "w") as f:
        json.dump (save_data,f,indent = 4)
    print (f"the game was saved for {username}")
def list_user_saves(username):
    if not os.path.exists("saves"):
        return []
    saves = [f for f in os.listdir("saves") if f.startswith(username)]
    return saves
def load_specific_save (filename):
    filepath = f"saves/{filename}"
    if not os.path.exists(filepath):
        print ("that game does not exist")
        return None
    with open(filepath, "r") as f:
        data = json.load(f)
    return data
def delete_save (filename):
    filepath = f"saves/{filename}"
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print (f"the game does not exist")
def load_game(username):
    return list_user_saves(username)
         
    