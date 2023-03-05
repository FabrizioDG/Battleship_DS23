#functions
from board import Board 
import numpy as np
from constants import *


def welcome():
    """
    Print welcome message
    """
    print("""
                88                                     88                        88          88   
                88                       ,d      ,d    88                        88          ""  
                88                       88      88    88                        88              
                88,dPPYba,  ,adPPYYba, MM88MMM MM88MMM 88  ,adPPYba,  ,adPPYba,  88,dPPYba,  88  8b,dPPYba,  
                88P'    "8a ""     `Y8   88      88    88 a8P_____88  I8[    ""  88P'    "8a 88  88P'    "8a
                88       d8 ,adPPPPP88   88      88    88 8PP'''''''   `"Y8ba,   88       88 88  88       d8 
                88b,   ,a8" 88,    ,88   88,     88,   88 "8b,   ,aa  aa    ]8I  88       88 88  88b,   ,a8"
                8Y"Ybbd8"'  `"8bbdP"Y8   "Y888   "Y888 88  `"Ybbd8"'  `"YbbdP"'  88       88 88  88`YbbdP"' 
                                                                                                 88
                                                     |__                                         88
                                                     |\/                                         88
                                                     ---                                         
                                                     / | [
                                              !      | |||
                                            _/|     _/|-++'
                                        +  +--|    |--|--|_ |-
                                     { /|__|  |/\__|  |--- |||__/
                                    +---------------___[}-_===_.'____                 /\ 
                                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _
                 __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
                |                                                                     BB-61/
                 \_________________________________________________________________________|

                                                                    Credits ASCII Art:   Matthew Bace https://ascii.co.uk/art/battleship
    """
    )


def show_rules():
    """ 
    Show the rules of the game
    Output:
    1) bool
      True: player wants to play
      False: player doesn't want to play
    """
    import time
    from IPython.display import HTML, display


    #display(HTML("""<img src="/home/fabrizio/Documenti/DataScience_Course/Battleship_DS23/battleship.jpg"
    #            width="500" height="300" align="center">"""))

    string = """    
    How does the game work?

    1. There are two players: you and the machine.
    2. A board of 10 x 10 positions where the ships will be placed.
    3. The first thing you do is to place the ships. For this game the ships are placed randomly, and ships cannot touch each other (not even diagonally).
       The ships are:
        * 4 ships of 1 length position.
        * 3 ships of 2 positions of length
        * 2 boats of 3 positions of length
        * 1 boat of 4 length positions   
    4. Both you and the machine have a board with boats, and the goal is to "shoot" and sink the opponent's boats until one player runs out of boats,
       and therefore loses.
    5. It works by turns and a coin is flipped to decide who starts.
    6. In each turn you shoot at a coordinate (X, Y) of the opponent's board. If you hit, it's your turn again. Otherwise, it is the machine's turn.
    7. In the machine's turns, if it hits, it's its turn again. Where does the machine shoot? The machine shoots randomly, unless it already hit a boat.
       In this case it will shoot close to the already hit boat to try to sink it. Moreover, the machine won't shoot close to already sunk boats,
       as the game rules don't allow you to put boats there.
    8. If all the ships of one player are sunk, the game ends and the other player wins.
    """

    for s in string:
        print(s,end="", flush=True)
        time.sleep(0.03)
    while True:
        ready = input("Are you ready to play? ('yes' or 'no'): ")
        if ready.lower()=='yes':
            return True
        elif ready.lower()=='no':
            return False
        else: 
            print("You must write either 'yes' or 'no'")

def print_boats(board : Board):
    """ 
    Print how many boats you already sunk
    Input:
    1) board: Board
        an object Board
    """
    boats = board.get_sunk_boats()
    print("List of sunk boats:")
    for key,value in boats.items():
        print(f"{key}-dimensional boat: {np.abs(value)}")
    
def check_victory(board : Board):
    """
    Check the victory condition.
    Inputs:
    1) board : Board
        an object Board
    Outputs:
    1) bool
        True: victory, False: Not yet victory
    """
    return np.array([x!=1 for x in board.get_board()]).all()



def show_board(board : Board):
    """
    Print a nicer visualization of the board
    Inputs:
    1) board : Board
    """
    b = board.get_board()
    tot_string = ""
    new_board = np.full((2*board.xdim + 1, board.ydim)," "*5)
    indices_water = (1+2*np.where(b==0)[0], np.where(b==0)[1])
    indices_boat = (1+2*np.where(b==1)[0], np.where(b==1)[1])
    indices_hit = (1+2*np.where((b==2) | (b==3) | (b==4))[0], np.where((b==2) | (b==3) | (b==4))[1])

    #print(indices_water)
    new_board[indices_water] = "| * |"
    new_board[indices_boat] =  "< B >"
    new_board[indices_hit] = "( X )"
    new_board[0::2,:] = "-----"
    #print(new_board)
    for i in range(new_board.shape[0]):
        for j in range(new_board.shape[1]):
            tot_string += new_board[i][j]+" "
        tot_string += "\n"
    return tot_string
    
def show_hits(my_board : Board, cpu_board : Board):
    """
    Print the board with all the places where the player fired
    Inputs:
    1) board : Board
    """
    tot_string = ""
    shape = my_board.get_shape()
    b = my_board.get_board()
    b_cpu = cpu_board.get_board()

    new_board = np.full((shape[0]*2+3,shape[1]*2 + 4)," "*5)

    indices_not_hit = (3+2*np.where((b==0) | (b==1) | (b==5))[0], shape[1] + 4 + np.where((b==0) | (b==1)| (b==5))[1])
    indices_hit_water = (3+2*np.where(b==2)[0],  shape[1] + 4 + np.where(b==2)[1])
    indices_hit_boat = (3+2*np.where((b==3))[0],  shape[1] + 4 + np.where((b==3))[1])
    indices_hit_sunk = (3+2*np.where((b==4))[0],  shape[1] + 4 + np.where((b==4))[1])

    indices_not_hit_cpu = (3+2*np.where((b_cpu==0) | (b_cpu==1) | (b_cpu==5))[0], 2 + np.where((b_cpu==0) | (b_cpu==1) | (b_cpu==5))[1])
    indices_hit_water_cpu = (3+2*np.where(b_cpu==2)[0], 2 + np.where(b_cpu==2)[1])
    indices_hit_boat_cpu = (3+2*np.where((b_cpu==3))[0], 2 + np.where((b_cpu==3))[1])
    indices_hit_sunk_cpu = (3+2*np.where((b_cpu==4))[0], 2 + np.where((b_cpu==4))[1])

    new_board[indices_not_hit] = "| * |"
    new_board[indices_hit_sunk] =  "< H >"
    new_board[indices_hit_boat] = "( X )"
    new_board[indices_hit_water] = "| O |"
    new_board[indices_not_hit_cpu] = "| * |"
    new_board[indices_hit_sunk_cpu] =  "< H >"
    new_board[indices_hit_boat_cpu] = "( X )"
    new_board[indices_hit_water_cpu] = "| O |"

    new_board[2::2,2:shape[1]+2] = "-----"
    new_board[2::2,shape[1]+4:] = "-----"
    for i in range(0,10):
        new_board[1,i+2] = f"  {i}  "
        new_board[1,shape[1] + 4 + i] = f"  {i}  "    
        new_board[2*(i+1)+1, 1] = f"  {i}  "
        new_board[2*(i+1)+1,shape[1] + 3] = f"  {i}  "
#AGGIUNGERE LA PARTE DI DIRECTION X E DIRECTION Y
        str_y = "    YAXIS "
        dir_x = "X AXIS"
        dir_y = [str_y[i:i+5] for i in range(0, len(str_y), 5)]
        for i,char in enumerate(dir_y):
            new_board[0,6+i] = f"{char}"
            new_board[0,18+i] = f"{char}"
        for i,char in enumerate(dir_x):
            new_board[9+i,0] = f"    {char}"
            new_board[9+i,12] = f"    {char}"


    print(f"""
    This is the board of {cpu_board.player}.                                                  This is the board of {my_board.player}. 
    Legend: ( X ) : hit but not sunk                                                Legend: ( X ) : hit but not sunk
            ( H ) : hit and sunk                                                            ( H ) : hit and sunk
            | * | : not yet fired                                                           | * | : not yet fired
            | O | : fired but water                                                         | O | : fired but water
    """)

    for i in range(new_board.shape[0]):
        for j in range(new_board.shape[1]):
            tot_string += new_board[i][j]+" "
        tot_string += "\n"
    return tot_string


def hit(my_board : Board, enemy_board : Board, coord : tuple):
    """
    Function to fire on a specific coordinate coord.
    Inputs:
    1) my_board : Board
        board of the player who is firing
    2) enemy_board : Board
        board of the enemy being fired
    3) coord : tuple of int
        the (x,y) coordinate where you want to fire
    Outputs:
    1) bool
        True if you hit something (water or boat)
        False if you tried to hit a position already hit or out of the board
    2) is_sunk : bool
        True if the boat has been sunk
        False if not
    """
    import os

    b = enemy_board.get_board()
    shape = enemy_board.get_shape()
    is_sunk = False
    if coord[0]>=shape[0] or coord[1]>=shape[1]:
        print(f"ERROR: the point {coord} is out of of the board with dimension {shape}")
        return None, None
    if b[coord[0],coord[1]] not in [0,1]:
        print(f"{my_board.player}, you already fired the point {coord}, please choose another point")
        return None, None
    elif b[coord[0],coord[1]] == 0:
        print(f"{my_board.player} attack hit the water at the point {coord}")
        b[coord[0],coord[1]] = 2
        return False, is_sunk
    elif b[coord[0],coord[1]] == 1:
        print(f"{my_board.player} hit a boat at the point {coord}")
        b[coord[0],coord[1]] = 3
        is_sunk = check_if_sunk(my_board, enemy_board, coord)
        return True, is_sunk
    


def check_if_sunk(my_board : Board, enemy_board : Board, coord : tuple):
    """
    Function to check if a boat hit at coordinate coord was sunk. It print a message
    explaining if the boat was sunk with the last hit or not.
    Inputs:
    1) my_board : Board
        board of the player who fired
    2) enemy_board : Board
        board of the enemy being fired
    1) coord : tuple of int
        the (x,y) coordinate where you fired last time
    Outputs:
    1) sunk : bool
        True if the boat is sunk
        False if the boat is not sunk
    """
    b = enemy_board.get_board()
    b_boats = enemy_board.get_board_boats()
    dim_boat = b_boats[coord[0],coord[1]][0]
    orientation = b_boats[coord[0],coord[1]][1]
    index_pos = b_boats[coord[0],coord[1]][2]
    shape = enemy_board.get_shape()
    boat_coords = []
    #I call this function only if I hit a boat. If there are no '1' closeby it means the boat is sunk
    

    if dim_boat==1: #1-dim boat is sunk for sure
        sunk = True
        enemy_board.add_sunk_boat(dim_boat)
        b[coord[0],coord[1]] = 4 # sunk boat
        print(f"{my_board.player} sank a boat of dimension {dim_boat}!!")

    else:
        if orientation == 1: #horizontal orientation
            for i in range (0,dim_boat):
                boat_coords.append([coord[0],coord[1]-index_pos+i])
        elif orientation == 0: #vertical orientation
            for i in range (0,dim_boat):
                boat_coords.append([coord[0]-index_pos+i,coord[1]])
        if all([b[x[0],x[1]]==3 for x in boat_coords]): #if all pieces of boat are '3' then it's sunk
            for c in boat_coords:
                b[c[0],c[1]] = 4 #sunk boat

            sunk = True
            enemy_board.add_sunk_boat(dim_boat)
            print(f"{my_board.player} sank a boat of dimension {dim_boat}!!")
        else:
            print(f"{my_board.player} didn't sink the boat yet!")
            sunk = False
    return sunk


def get_neighbours(board : Board, coord : tuple):
    """
    Return a list of tuples with the coordinates of the neighbours
    of the cell at the point coord (only horizontal and vertical neighbours)
    """
    shape = board.get_shape()
    tmp = ([(coord[0]+i,coord[1]) for i in [-1,1]] 
                + [(coord[0],coord[1]+i) for i in [-1,1]])
    neighbours = []    
    for x in tmp:
        if x[0] in range(0,shape[0]) and x[1] in range(0,shape[1]):
            neighbours.append(x)
    return neighbours

#Other functions for main!

def player_turn(my_board : Board, cpu_board : Board):
    """ 
    Function for the turn of the player
    Inputs:
    1) my_board : Board
       the player board
    1) enemy_board : Board
      The Board object of the computer (enemy)
    """
    import os

    is_hit = None
    print("So far you sank the following boats:")
    print(f"{cpu_board.get_sunk_boats()}")
    print("So far the AI sank the following boats on your board:")
    print(f"{my_board.get_sunk_boats()}")

    while is_hit==None:

        str = input(f"""Provide the coordinates where you want to fire in the format x,y.
                    Remember the board size is {BOARD_SIZE}: """)
        if len(str)!=3:
            print(f"You wrote {str}, you should write x,y where x,y are between 0 and 9 included")            
        else:
            try:
                x = int(str[0])
                y = int(str[2])
            except:
                print(f"x,y must be integer numbers between 0 and 9 included!!")
                continue
            if x not in range(0,10) or y not in range(0,10):
                print(f"x and y must be between 0 and 9 included!")
            else:
                if not (x>=cpu_board.get_shape()[0] or y>=cpu_board.get_shape()[0] or cpu_board.get_board()[x,y] not in [0,1]):
                    os.system('cls' if os.name == 'nt' else "printf '\033c'")
                is_hit, _ = hit(my_board, cpu_board,(x,y))    
    return is_hit

def cpu_turn(cpu_board : Board, player_board : Board):
    """
    
    """
    b = player_board.get_board()

    #if cpu already hit and not sunk some boats fire close to hit places
    if np.array([el==3 for el in b]).any():
        coords_hit = np.where(b==3) #find all coords where cpu hit, and take the first one
        x = coords_hit[0][0]
        y = coords_hit[1][0]
        neighbours = get_neighbours(player_board,(x,y))
        hit_boat_close =[]
        hit_water_close=[]
        for z in neighbours:
            if b[z[0],z[1]]==3:
                hit_boat_close.append(z)
            elif b[z[0],z[1]]==2 or b[z[0],z[1]]==5:
                hit_water_close.append(z)

        if len(hit_boat_close)==0: #I COULD CHANGE THIS TO BE RANDOM
            for elem in neighbours:
                if elem not in hit_water_close:
                    coord_fire = elem
        elif len(hit_boat_close)==1:
            if hit_boat_close[0][0] == x: # -> the boat is horizontal
                # if the other neighbour which is horizontal was water and cpu knows or if the point where I hit
                # is at the left/right border (y==0 or y==9), then cpu search on the other direction
                # but same orientation where to fire to sink the boat

                #If I'm at the border search for the new point which is not out of the board

                #if I'm not at the border and I already shot on the water closeby
                if len(hit_water_close)!=0:
                    if any([z[0]==x for z in hit_water_close]) or y in [0,9]:
                        i=1
                        while True:
                            coord_fire = (x, y - (y-hit_boat_close[0][1])*i)
                            if b[coord_fire[0],coord_fire[1]]!=3:
                                break
                            i+=1
                    #if cpu didn't hit yet on the other neighbour that is horizontal, 
                    # and it is not out of border hit there
                    else:
                        i=1
                        while True:
                            coord_fire = (x, y + (y-hit_boat_close[0][1])*i)
                            if b[coord_fire[0],coord_fire[1]]!=3:
                                break
                            i+=1 
                #if cpu didn't hit yet on the other neighbour that is horizontal, 
                # and it is not out of border hit there
                else:
                    i=1
                    while True:
                        if y not in [0,9]:
                            coord_fire = (x, y + (y-hit_boat_close[0][1])*i)
                        else:
                            coord_fire = (x, y - (y-hit_boat_close[0][1])*i)
                        if b[coord_fire[0],coord_fire[1]]!=3:
                            break
                        i+=1  
                
            else: # -> the boat is vertical 
                if len(hit_water_close)!=0:
                    if any([z[1]==y for z in hit_water_close]) or x in [0,9]:
                        i=1 
                        while True:
                            coord_fire = (x - (x-hit_boat_close[0][0])*i, y)
                            if b[coord_fire[0],coord_fire[1]]!=3:
                                break
                            i+=1
                    #if cpu didn't hit yet on the other neighbour that is horizontal, 
                    # and it is not out of border hit there
                    else:
                        i=1
                        while True:
                            coord_fire = (x + (x-hit_boat_close[0][0])*i, y)
                            if b[coord_fire[0],coord_fire[1]]!=3:
                                break
                            i+=1  
                    #if cpu didn't hit yet on the other neighbour that is horizontal, 
                    # and it is not out of border hit there
                else:
                    i=1
                    while True:
                        if x not in [0,9]:
                            coord_fire = (x + (x-hit_boat_close[0][0])*i, y)
                        else:
                            coord_fire = (x - (x-hit_boat_close[0][0])*i, y)
                        if b[coord_fire[0],coord_fire[1]]!=3:
                            break
                        i+=1  

            #I think this can never happen, cause the first coords in np.where will always be the first occurrence
            # where board==3 so it's impossible that I choose a point in the middle of a boat
        elif len(hit_boat_close)==2:
            pass     



    #if there are no hits on the board, just choose randomly in all the points where cpu didn't fire yet
    else:
        possible_coords = np.where((b!=3) & (b!=2) & (b!=4) & (b!=5))
        if len(possible_coords)>0:
            index = np.random.randint(0,len(possible_coords[0]))
            coord_fire = (possible_coords[0][index], possible_coords[1][index])

    is_hit, is_sunk = hit(cpu_board, player_board, coord_fire)
    #set a mask around sunk boat to avoid firing there!
    if is_sunk:
        b_boats = player_board.get_board_boats()
        dim_boat = b_boats[coord_fire[0],coord_fire[1]][0]
        orientation = b_boats[coord_fire[0],coord_fire[1]][1]
        pos = b_boats[coord_fire[0],coord_fire[1]][2]

        if orientation==1: #horizontal
            coord_head = (coord_fire[0], coord_fire[1] - pos)
            coord_tail = (coord_fire[0], coord_fire[1] - pos + dim_boat)
        elif orientation==0: #vertical
            coord_head = (coord_fire[0] - pos, coord_fire[1])
            coord_tail = (coord_fire[0] - pos + dim_boat, coord_fire[1])
        player_board.set_mask(coord_head, coord_tail, orientation, 5, exception=2)

    return is_hit