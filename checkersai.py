#Contains the classes that represent the AIs for the game (at the
#moment, only random_randy is working properly).
import checkers, random

#For your AIs, try to focus on returning moves only. Leave the
#process of how the move changes the gamestate to the GUI code.



#TODO: The GameOverException isn't being thrown when the human
#      player's piece count reaches 0 and the game stops responding
#      if the CPU player's piece count reaches 0. FIX THIS.
def random_randy(gs, cpu_color):
    """
    Function representing an AI that performs random moves. Takes a
    gamestate and the cpu's color and returns a valid random move.
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



#TODO: I suspect that the GameOverException is being
#      raised within the MiniMax tree traversel. FIX THIS.
def minimax(gamestate, cpu_color, depth):
    """
    Executes a cpu move based on a depth-limited minimax algorithm.
    @gamestate: The game state of a checkers match. The game state is
                altered as the minimax search progresses down the tree
                of possible move outcomes.
    @cpu_color: The color of the CPU
    @depth: An int indicating how deep to traverse down the tree of
            possible move outcomes
    type gamestate: Checkers
    type cpu_color: str
    type depth: int
    """
    best_move = None    
    node_type = ""

    #Base case of Mini Max
    if depth == 0 or gamestate.get_winner() != None:
        node_type = "terminal"
        print("TERMINAL NODE REACHED (depth: {})".format(depth))
        print("EVALUATING THIS BOARD:")
        gamestate.print_board()
        print("**********")
        print("GOING BACK UP FROM {} NODE\n".format(node_type))

        return (minimax_eval(gamestate, cpu_color), None)

    if gamestate.get_turn() == cpu_color:
        node_type = "max"
        print("AT ^_MAX_^ NODE ({})".format(gamestate.get_turn()))
        print("CURRENT BOARD CONFIG (depth: {}):".format(depth), end="")
        gamestate.print_board()

        best_val = float("-inf")
        valid_moves = gamestate._valid_moves_exist(
                        gamestate.get_turn(), check_for_cpu=True)

        for move in valid_moves:
            #move is a 4-tuple: (start_row, start_col, target_row, target_col)
            dummy_game = checkers.Checkers(init_config = gamestate.get_board(),
                                           init_turn = gamestate.get_turn())

            #NOTE: make_move() will switch turns
            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1)
            print("MOVE MADE BY ^_MAX_^ NODE ({}, depth: {}):".\
                  format(gamestate.get_turn(), depth))
            print((move[0]+1, move[1]+1), (move[2]+1, move[3]+1))
            dummy_game.print_board() #FOR TESTING
            print("")

            (val, move_made) = minimax(dummy_game, cpu_color, depth-1)
            if val > best_val:
                best_move, best_val = move, val

    else: #If it's the minimizing player's turn to move...
        node_type = "min"
        print("AT v_MIN_v NODE KHOA ({})".format(gamestate.get_turn()))
        print("CURRENT BOARD CONFIG (depth: {}):".format(depth), end="")
        gamestate.print_board()

        best_val = float("inf")
        valid_moves = gamestate._valid_moves_exist(
                        gamestate.get_turn(), check_for_cpu=True)

        for move in valid_moves:
            dummy_game = checkers.Checkers(init_config = gamestate.get_board(),
                                           init_turn = gamestate.get_turn())

            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1)
            print("MOVE MADE BY v_MIN_v NODE ({}, depth: {}):".\
                  format(gamestate.get_turn(), depth))
            print((move[0]+1, move[1]+1), (move[2]+1, move[3]+1))
            dummy_game.print_board()
            print("")

            (val, move_made) = minimax(dummy_game, cpu_color, depth-1)
            if val < best_val:
                best_move, best_val = move, val

    print("GOING BACK UP FROM {} NODE\n".format(node_type))
    return (best_val, best_move)



#TODO: I suspect that the GameOverException is being
#      raised within the MiniMax tree traversel. FIX THIS.
def minimax_abp(gamestate, cpu_color, depth, alpha, beta):
    """
    Executes a cpu move based on a depth-limited minimax
    algorithm with alpha-beta pruning.
    @gamestate: The game state of a checkers match. The game state is
                altered as the minimax search progresses down the tree
                of possible move outcomes.
    @cpu_color: The color of the CPU
    @depth: An int indicating how deep to traverse down the tree of
            possible move outcomes
    @alpha: The maximum lower bound for an AB-prune
    @beta: The minimum upper bound for an AB-prune
    type gamestate: Checkers
    type cpu_color: str
    type depth: int
    type alpha: float
    type beta: float
    return: A tuple whose first component is a utility value and
            whose second component is the the move associated with
            that utility value
    rtype: tuple
    """
    best_move = None    
    node_type = ""

    print("ALPHA-BETA PRUNING IN EFFECT")

    #Base case of Mini Max
    if depth == 0 or gamestate.get_winner() != None:
        node_type = "terminal"
        print("TERMINAL NODE REACHED (depth: {})".format(depth))
        print("EVALUATING THIS BOARD:")
        gamestate.print_board()
        print("**********")
        print("GOING BACK UP FROM {} NODE\n".format(node_type))

        return (minimax_eval(gamestate, cpu_color), None)

    if gamestate.get_turn() == cpu_color:
        node_type = "max"
        print("AT ^_MAX_^ NODE ({})".format(gamestate.get_turn()))
        print("CURRENT BOARD CONFIG (depth: {}):".format(depth), end="")
        gamestate.print_board()

        best_val = float("-inf")
        valid_moves = gamestate._valid_moves_exist(
                        gamestate.get_turn(), check_for_cpu=True)

        for move in valid_moves:
            #move is a 4-tuple: (start_row, start_col, target_row, target_col)
            dummy_game = checkers.Checkers(init_config = gamestate.get_board(),
                                           init_turn = gamestate.get_turn())

            #NOTE: make_move() will switch turns
            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1)
            print("MOVE MADE BY ^_MAX_^ NODE ({}, depth: {}):".\
                  format(gamestate.get_turn(), depth))
            print((move[0]+1, move[1]+1), (move[2]+1, move[3]+1))
            dummy_game.print_board() #FOR TESTING
            print("")

            (val, move_made) = minimax_abp(dummy_game,
                                cpu_color, depth-1, alpha, beta)
            if val > best_val:
                best_move, best_val = move, val

            if best_val > alpha:
                alpha = best_val

            if beta <= alpha:
                print("PRUNING!!!")
                break

    else:
        node_type = "min"
        print("AT v_MIN_v NODE ({})".format(gamestate.get_turn()))
        print("CURRENT BOARD CONFIG (depth: {}):".format(depth), end="")
        gamestate.print_board()

        best_val = float("inf")
        valid_moves = gamestate._valid_moves_exist(
                        gamestate.get_turn(), check_for_cpu=True)

        for move in valid_moves:
            dummy_game = checkers.Checkers(init_config = gamestate.get_board(),
                                           init_turn = gamestate.get_turn())

            dummy_game.make_move(move[0]+1, move[1]+1, move[2]+1, move[3]+1)
            print("MOVE MADE BY v_MIN_v NODE ({}, depth: {}):".\
                  format(gamestate.get_turn(), depth))
            print((move[0]+1, move[1]+1), (move[2]+1, move[3]+1))
            dummy_game.print_board()
            print("")

            (val, move_made) = minimax_abp(dummy_game,
                                cpu_color, depth-1, alpha, beta)
            if val < best_val:
                best_move, best_val = move, val

            if best_val < beta:
                beta = best_val

            if beta <= alpha:
                print("xxxxxPRUNINGxxxxx!!!")
                break

    print("GOING BACK UP FROM {} NODE\n".format(node_type))
    return (best_val, best_move)




#TODO: Implement a stronger evaluation function
def minimax_eval(gamestate, cpu_color):
    """
    The evaluation function for a Chceckers minimax AI.
    @gamestate: A Checkers game state to evaluate
    @cpu_color: The color of the CPU ("B" or "G")
    type gamestate: Checkers
    type cpu_color: str
    return: A score for the given gamestate
    rtype: int
    """
    score = 0
    score += gamestate.get_red_count() - gamestate.get_black_count() if cpu_color == "R" else\
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
