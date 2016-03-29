#Contains the classes that represent the AIs for the game (at the
#moment, only random_randy is working properly).

import checkers, random

#For your AIs, try to focus on returning moves only. Leave the process of how the move changes
#the gamestate to the GUI code.

def random_randy(gs, cpu_color):
    '''Function representing an AI that performs random moves. Takes a gamestate and
       the cpu's color and returns a valid random move.'''
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

def minimax(gamestate, cpu_player, depth):
    '''Executes a cpu move based on a depth-limited minimax algorithm.'''
    best_move = None
    player_color = "B" if cpu_player == "R" else "B"
    if depth == 0 or gamestate.get_winner() != " ":
        return (minimax_eval(gamestate, cpu_player), None)
    elif gamestate.get_turn() == cpu_player:
        best_val = float("-inf")
        valid_moves = gamestate._valid_moves_exist(cpu_player, check_for_cpu=False)
        for move in valid_moves:
            #move is a 4-tuple: (start_row, start_col, target_row, target_col)
            dummy_game = checkers.Checkers(player_color,
                                           gamestate.get_board())

            dummy_game.make_move(move[0], move[1], move[2], move[3])
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1)
            if val > best_val:
                best_move = move
                best_val = val

        return (best_val, best_move)
    else: #If it's the minimizing player's turn to move...
        best_val = float("inf")
        valid_moves = gamestate._valid_moves_exist(player_color, check_for_cpu=False)
        for move in valid_moves:
            dummy_game = checkers.Checkers(player_color,
                                           gamestate.get_board())

            dummy_game.make_move(move[0], move[1], move[2], move[3])
            (val, move_made) = minimax(dummy_game, cpu_player, depth-1)
            if val < best_val:
                best_move = move
                best_val = val

        return (best_val, best_move)

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
