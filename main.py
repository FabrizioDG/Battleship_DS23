#main code for the game!
import numpy as np
import os
from functions import *
from board import Board
from constants import *

def main():
    welcome()
    name = input("Set the name for the player: ").strip()
    print(f"Welcome {name} to this Battleship game!")

    while True:
        rule = input("Do you want me to remind you the rules? ('yes' or 'no'): ").strip()
        if rule.lower() =='yes':
            playing = show_rules()
            break
        elif rule.lower() =='no':
            playing = True
            break
        else:
            print("Please reply either 'yes' or 'no'")

    os.system('cls' if os.name == 'nt' else "printf '\033c'") #this should work on terminal to flush output!

    if playing:
        print("Good! Let's start with the game!")
    else:
        print("Ok, so maybe next time!")
        return None
    my_board = Board(name, BOARD_SIZE, BOATS)

    cpu_board = Board("Computer",BOARD_SIZE, BOATS)

    print("""     
    This is your board with boats set randomly 
    Notation: | * | is water
            < B > is a boat piece
            ( X ) is a spot hit by the enemy
    """)
    print(show_board(my_board))
    #flip a coin to decide who starts
    coin_dict = {0 : "head", 1 : "tail"}
    player_starts = False
    while True:
        coin = input("Choose head or tail: ").strip()
        if coin.lower() not in ["head", "tail"]:
            print(f"You must write either 'head' or 'tail' but you wrote {coin}")
        else:
            break
    if coin_dict[np.random.randint(0,2)]==coin.lower():
        player_starts = True

    os.system('cls' if os.name == 'nt' else "printf '\033c'") #this should work on terminal to flush output!

    #player starts
    while True:
        if player_starts:
            is_hit = True
            #player turn
            print(f"*********** {my_board.player}'s turn starts now'! ***********")

            while is_hit: 
                print(show_hits(my_board, cpu_board))
                is_hit = player_turn(my_board, cpu_board)
                #os.system('cls' if os.name == 'nt' else "printf '\033c'") #this should work on terminal to flush output!

                victory_player = check_victory(cpu_board)
                if victory_player:
                    break

            if victory_player:
                pattern = """\/"""
                string = f"---- Congratulations {my_board.player}, you won!!!! ----"
                print(show_hits(my_board, cpu_board))
                print(" You sank all the boats!")
                print("The Computer only sank these boats:")
                print(f"{my_board.get_sunk_boats()}\n")
                print(f"""
                          {pattern*int(len(string)/2)}
                          {string}
                          {pattern*int(len(string)/2)}  
                            """)                                                                 
                break
            is_hit = True
            #cpu turn
            print("*********** The turn of the Computer starts now! ***********")

            while is_hit: 
                is_hit = cpu_turn(cpu_board, my_board)
                victory_cpu = check_victory(my_board)
                if victory_cpu:
                    break

            if victory_cpu:
                pattern = """\/"""
                string = f"---- Game Over! The Computer won!!!! ----"
                print(show_hits(my_board, cpu_board))
                print(" The Computer sank all the boats!")
                print("You only sank these boats:")
                print(f"{my_board.get_sunk_boats()}\n")
                print(f"""
                          {pattern*int(len(string)/2)}
                          {string}
                          {pattern*int(len(string)/2)}  
                            """)
                break
        else:
            is_hit = True
            #cpu turn
            print("*********** The turn of the Computer starts now! ***********")

            while is_hit: 
                is_hit = cpu_turn(cpu_board, my_board)
                victory_cpu = check_victory(my_board)
                if victory_cpu:
                    break

            if victory_cpu:
                pattern = """\/"""
                string = f"---- Game Over! The Computer won!!!! ----"
                print(show_hits(my_board, cpu_board))
                print(show_hits(my_board, cpu_board))
                print(" The Computer sank all the boats!")
                print("You only sank these boats:")
                print(f"{my_board.get_sunk_boats()}\n")
                print(f"""
                          {pattern*int(len(string)/2)}
                          {string}
                          {pattern*int(len(string)/2)}  
                            """)
                break
            is_hit = True
            #player turn
            print(f"*********** {my_board.player}'s turn starts now! ***********")

            while is_hit: 
                print(show_hits(my_board, cpu_board))
                is_hit = player_turn(my_board, cpu_board)
                #os.system('cls' if os.name == 'nt' else "printf '\033c'") #this should work on terminal to flush output!

                victory_player = check_victory(cpu_board)
                if victory_player:
                    break

            if victory_player:
                pattern = """\/"""
                string = f"---- Congratulations {my_board.player}, you won!!!! ----"
                print(show_hits(my_board, cpu_board))
                print(" You sank all the boats!")
                print("The Computer only sank these boats:")
                print(f"{my_board.get_sunk_boats()}\n")
                print(f"""
                          {pattern*int(len(string)/2)}
                          {string}
                          {pattern*int(len(string)/2)}  
                            """)   
                break

main()
