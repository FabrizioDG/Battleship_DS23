#El plan es que en las coordenadas con agua ponemos '0', en las coordenadas con barcos ponemos '1'
# y en las coordenadas donde se ha disparado ponemos 2 si el disparo fue en el agua o 3 si el disparo fue a un barco
# y 4 si el barco está hundido

#self.barcos es un diccionario con llaves la dimension del barco y valor cuanto barcos te quedan

#set_boats: select which boat from the dictionary barcos, select a random orientation (horizontal or vertical), then 
# set the boat at random in the allowed area, considering that position is the head of the boat
#  (the rest of the boat follows either right if orientation==horizontal or down if orientation==vertical)

#the allowed area have zeros, I set with '2' the area close to the boats already set before, so that they don't touch.
#When all the boats are set, I will reset all the '2' with '0'

#barcos = {1 : 4, 2 : 3 , 3 : 2 , 4 : 1}


#set_mask
# I pad the matrix with an extra border, not to be worried if the boat is at the border or not. I set the mask and then I 
# delete the extra padding I put.

#CONSTANTS:
#BOARD_SIZE = (10,10)

import numpy as np

class Board:
    """
    class Board that set a board (a matrix) with boats placed randomly and with random orientation,
    which can be used to play Battleship

    Arguments:
    1) self.player : string
        name of the player
    2) self.board : numpy matrix with integers
        Board notation: 0 -> water
                        1 -> boat
                        2 -> hit on water
                        3 -> hit on boat
                        4 -> boat sunk
    3) self.board_boats : numpy matrix with integers
        This boat is to save what type of boat there is in each coordinate
                        0 -> water (no boat)
                        1 -> 1-dim boat
                        2 -> 2-dim boat
                        3 -> 3-dim boat
                        4 -> 4-dim boat
    3) self.xdim : int
        board first dimension (vertical)
    4) self.ydim : int
        board second dimension (horizontal)
    5) self.boats : dict
        a dictionary with (keys = dimension of the boat, values = how many boats at start)
    6) self.sunk_boats : dict
        a dictionary with (keys = dimension of the boat, values = how many sunk boats)
    Methods:

    1) __init__(self, player : string, board_size : tuple, boats : dict) -> None
        Constructor of the class, it initialize the board with boats placed randomly
    2) set_boat (self, dim_boat : int) -> None
        set a boat of dimension dim_boat with random orientation in a random spot of the board
        without touching other boats
    3) set_mask(self, coord1 : tuple, coord2 : tuple, is_horizontal : bool, value : int) -> None
        take the position of the boat which goes from coord1 to coord2, and set
        all the cells around the boat equal to value
    4) polish_board(self) -> None
        Set to 0  all the values in the initial board which are not 0 or 1. Print that the board is ready.
    5) get_board(self) -> numpy matrix
        Return the board
    6) get_board_boats(self) -> numpy matrix
        Return the board with the dimensions of the boats
    7) get_sunk_boats(self) -> dict
        Return the dictionary with the sunk boats
    8) get_shape(self) -> tuple of int
        Return (self.xdim, self.ydim) 
    """
    
    def __init__(self, player, board_size, boats):
        """
        Constructor of the class, it initialize the board with boats placed randomly.
        
        Inputs:
        1) player : string
            name of the player
        2) board_size : tuple of int
            (xdim, ydim) dimension of the board
        3) boats : dict
            a dictionary with (keys = dimension of the boat, values = how many boats)
        """
        self.player = player
        self.board = np.zeros(board_size)
        self.board_boats = np.full(board_size + (3,),(0,0,0))
        self.xdim = board_size[0]
        self.ydim = board_size[1]
        self.boats = boats.copy()
        self.sunk_boats = {key : 0 for key in boats}

        flag = []
        #I put this while because sometimes (very rare) there is no space for the last boat
        #So if that's the case, it will reconstruct the board from zero again
        while True:
            self.clear_board()
            for boat, num in boats.items():
                for j in range(num):
                    flag.append(self.set_boat(boat))
            if all(flag)==True:
                break
        #reset the boats in the dictionary
        self.boats = boats.copy()
        self.polish_board()


    def set_boat(self, dim_boat):
        """
        set a boat of dimension dim_boat with random orientation in a random spot of the board
        without touching other boats

        Inputs:
        1) dim_boat : int
            dimension of the boat you want to place
        Output:
        1) bool
            True if it was possible to set the boat
            False if it was not possible to set the boat
        """
        flag = True
        if dim_boat not in self.boats:
            print(f"ERROR: There is no boat with dimension {dim_boat}")
            return None
        if self.boats[dim_boat]>0:
           self.boats[dim_boat]-=1 #substract the boat you already put
        else:
            print(f"Warning: you already put all the boats of dimension {dim_boat}")
            return None
        counter = 0
        while flag and counter<200:
            is_horizontal = np.random.randint(0,2)>0
            if is_horizontal: # horizontal
                coord1 = (np.random.randint(0,self.xdim),np.random.randint(0,self.ydim-dim_boat+1))
                coord2 = (coord1[0], coord1[1] + dim_boat)

                #if all the points where I want to put the boat are free (zeros)
                # +1 is because if not the slicing is empty
                if (self.board[coord1[0],coord1[1]:coord2[1]] == 0).all():
                    self.board[coord1[0],coord1[1]:coord2[1]] = 1
                    for i, coord in enumerate(range(coord1[1],coord2[1])):
                        self.board_boats[coord1[0],coord] = (dim_boat, 1, i)
                    self.set_mask(coord1, coord2, is_horizontal, 2)
                    flag = False
            else: #vertical
                coord1 = (np.random.randint(0,self.xdim-dim_boat+1),np.random.randint(0,self.ydim))
                coord2 = (coord1[0] + dim_boat, coord1[1])

                if (self.board[coord1[0]:coord2[0],coord1[1]]==0).all():
                    self.board[coord1[0]:coord2[0],coord1[1]] = 1
                    for i, coord in enumerate(range(coord1[0],coord2[0])):
                        self.board_boats[coord,coord1[1]] = (dim_boat, 0 ,i)
                    self.set_mask(coord1, coord2, is_horizontal, 2)
                    flag = False
            counter +=1
        if counter >=200:
            return False
        return True


    def set_mask(self, coord1, coord2, is_horizontal, value, exception=None):
        """
        take the position of the boat which goes from coord1 to coord2, and set
        all the cells around the boat equal to value

        Inputs:
        1) coord1 : tuple of a pair of int
            coordinate (x,y) of the head of the boat
        2) coord2 : tuple of a pair of int
            coordinate (x,y) of the space after the tail of the boat
        3) is_horizontal : bool
            True : horizontal , False : vertical
        4) value : int
            The value you want to set in the mask
        5) exception: int
            Optional value you don't want to print on with the mask

        """
        #pad the matrix:
        new_board = np.zeros((self.xdim+2, self.ydim+2))
        new_board[1:-1,1:-1] = self.board
        #add one to coordinates
        coord1 = [c+1 for c in coord1]
        coord2 = [c+1 for c in coord2]

        coords = [(1,7),(1,4)]
        for i in range(4,7+1):
            coords.append((1-1,i))
            coords.append((1+1,i))

        if is_horizontal: #horizontal
            coords = [(coord1[0], coord1[1]-1), (coord2[0], coord2[1])]
            for i in range(coord1[1]-1,coord2[1]+1):
                coords.append((coord1[0]-1, i))
                coords.append((coord1[0]+1, i))

            for coord in coords:
                if new_board[coord[0], coord[1]]!=exception:
                    new_board[coord[0], coord[1]] = value

            #new_board[coord1[0],coord1[1]-1] = value
            #new_board[coord2[0],coord2[1]] = value
            #new_board[coord1[0]-1, coord1[1]-1:coord2[1]+1] = value
            #new_board[coord1[0]+1, coord1[1]-1:coord2[1]+1] = value
        else:
            coords = [(coord1[0]-1, coord1[1]), (coord2[0], coord1[1])]
            for i in range(coord1[0]-1,coord2[0]+1):
                coords.append((i, coord1[1]-1))
                coords.append((i, coord1[1]+1))
            for coord in coords:
                if new_board[coord[0], coord[1]]!=exception:
                    new_board[coord[0], coord[1]] = value

            #new_board[coord1[0]-1,coord1[1]] = value
            #new_board[coord2[0],coord1[1]] = value
            #new_board[coord1[0]-1:coord2[0]+1, coord1[1]-1] = value
            #new_board[coord1[0]-1:coord2[0]+1, coord1[1]+1] = value

        #delete padding
        self.board = new_board[1:-1,1:-1]
              
    def polish_board(self):
        """
        Set to 0 all the values in the initia board which are not 1 or 0. Print that the board is ready.
        """
        self.board[np.where((self.board!=0) & (self.board!=1))] = 0
        #print(f"The board for player {self.player} is ready")

    def clear_board(self):
        """
        Set to 0 all the board
        """
        self.board =np.zeros((self.xdim, self.ydim))

    def get_board(self):
        """
        Return the board
        Output:
        1) self.board : numpy matrix
        """
        return self.board
    
    def get_board_boats(self):
        """
        Return the board with boats dimensions
        Output:
        1) self.board : numpy matrix
        """
        return self.board_boats
    
    def get_sunk_boats(self):
        """
        Return the dictionary with the sunk boats
        Output:
        1) self.boats : dict
        """
        dictio = { key : (str(list(self.sunk_boats.values())[i]) + r"/" + str(list(self.boats.values())[i])) 
                 for i,key in enumerate(self.boats.keys())}

        return dictio
    
    def add_sunk_boat(self, dim_boat):
        """ 
        Add a sunk boat in the counting of boats
        """
        self.sunk_boats[dim_boat]+=1
    
    def get_shape(self):
        """
        Return the shape of the board
        Output:
        1) (self.xdim, self.ydim) : tuple of int
        """
        return (self.xdim, self.ydim)

 
        