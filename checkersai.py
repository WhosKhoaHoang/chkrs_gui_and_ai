#Contains the classes that represent the AIs for the game (at the
#moment, only random_randy is working properly).

import checkers, random

#For your AIs, try to focus on returning moves only. Leave the process of how the move changes
#the gamestate to the GUI code.

def random_randy(gs, cpu_color):
    """
    Function representing an AI that performs random moves. Takes a gamestate and
       the cpu's color and returns a valid random move.
    @cpu_color: The color of the CPU opponent ("R" or "B")
    type cpu_color: str
    return: A 4-tuple that represents the move to be made:
            (start_row, start_col, target_row, target_col)
    rtype: tuple
    """
    valid_moves = gs._valid_moves_exist(cpu_color, check_for_cpu=True)
    jump_moves = [move for move in valid_moves if move[-1] == "jump"]
    #Recall that if there's a jump available, the jump must be made no matter what.
    if len(jump_moves) > 0:
        return random.choice(jump_moves)
    if len(valid_moves) == 0:
        return None

    return random.choice(valid_moves)
    #Note how a move is a 4-tuple consisting of:
    #(start_row, start_col, target_row, target_col)


#FOCUS HERE
def minimax(gamestate, cpu_player, depth):
    """
    Executes a cpu move based on a depth-limited minimax algorithm.
    @gamestate: The game state of a checkers match. The game state is
                altered as the minimax search progresses down the tree
                of possible move outcomes.
    @cpu_player: The color of the CPU
    @depth: An int indicating how deep to traverse down the tree of
            possible move outcomes
    type gamestate: Checkers
    type cpu_player: str
    type depth: int
    """

    print("\n\n")
    print("IN minimax")
    print(depth)
    print(gamestate)
    print(cpu_player)
    print("\n\n")

    best_move = None
    player_color = "B" if cpu_player == "R" else "B"

    #Base case of Mini Max
    if depth == 0 or gamestate.get_winner() != None:

        print("\n\n")
        print("IN if")
        print(depth)
        print("\n\n")

        return (minimax_eval(gamestate, cpu_player), None)
    elif gamestate.get_turn() == cpu_player:

        print("\n\n")
        print("IN elif")
        print("\n\n")

        best_val = float("-inf")
        valid_moves = gamestate._valid_moves_exist(cpu_player, check_for_cpu=True)
        print("\n\n")
        print(valid_moves)
        print("\n\n")

        for move in valid_moves:
            #move is a 4-tuple: (start_row, start_col, target_row, target_col)
            dummy_game = checkers.Checkers(player_color, gamestate.get_board(), cpu_player)

            print("\nMove made:")
            print(move[0], move[1], move[2], move[3])

            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1) #TODO: Figure out why +1 is needed...
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1)
            if val > best_val:
                best_move = move
                best_val = val

        return (best_val, best_move)

    else: #If it's the minimizing player's turn to move...

        print("\n\n")
        print("IN else")
        print("\n\n")

        best_val = float("inf")
        valid_moves = gamestate._valid_moves_exist(player_color, check_for_cpu=True)
        print("\n\n")
        print(valid_moves)
        print("\n\n")

        for move in valid_moves:
            dummy_game = checkers.Checkers(cpu_player, gamestate.get_board(), player_color)

            print("\nMove made:")
            print(move[0], move[1], move[2], move[3])

            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1) #TODO: Figure out why +1 is needed...
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1)
            if val < best_val:
                best_move = move
                best_val = val

        return (best_val, best_move)


#TODO: Implement a stronger evaluation function
def minimax_eval(gamestate, cpu_player):
    '''The evaluation function of a minimax algorithm.'''
    score = 0
    score += gamestate.get_red_count() - gamestate.get_black_count() if cpu_player == "R" else\
             gamestate.get_black_count() - gamestate.get_red_count()

    return score























#RUN THIS MODULE (checkersai.py) FOR TESTING
if __name__ == "__main__":
#Objectives:
#Find a way to list all of the valid moves for a player...*CHECK*
#Perform each of those moves on a dummy board...*CHECK*
    
    gs = checkers.Checkers("B")
    #gs._draw_gameboard()
    lst = gs._valid_moves_exist("B", check_for_cpu=True)

    '''
    for i in range(len(lst)):
        print()
        dummy = checkers.Checkers("B", gs.get_board())
        dummy.make_move(lst[i][0]+1, lst[i][1]+1, lst[i][2]+1, lst[i][3]+1)
        #^recall that moves are performed according to "user-friendly" coordinates.
        dummy._draw_gameboard() #FOR TESTING
    '''


    #Have an evaluation function that evaluates the goodness of a board configuration
