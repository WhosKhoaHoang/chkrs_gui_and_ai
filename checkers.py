#Contains all of the classes corresponding to a checkers gamestate.
from copy import deepcopy




class InvalidMoveError(Exception):
    """ An error that represents an invalid move. """
    pass


class OutOfBoundsError(Exception):
    """ An error that represents a move that has gone out of bounds. """
    pass
#We can't assume that this gamestate will be used by one particular kind of UI.
#The UI could be a console UI or a GUI. This type of exception probably won't be an
#issue for GUIs, but could be for console UIs.


class GameOverError(Exception):
    """ An error that represents a game over. """
    pass




#This gamestate corresponds to standard U.S. Rules,
#which means that you can only jump backwards IF you're a king.
class Checkers:
    """ A class that represents a checkers gamestate. """

    def __init__(self, init_config = [], init_turn="B"):
        """
        Initializes a checkers gamestate.
        @init_config: The initial configuration of the gameboard
        @init_turn: Indicates which player ("B" or "R") goes first
        type initial_config: list
        type init_turn: str
        """
        #self._player = player_color
        self._num_rows = 8
        self._num_cols = 8
        self._red_count = 12
        self._black_count = 12
        #self._turn = "B" #Black goes first
        #self._turn = "R"  #FOR TESTING GUI!!!
        self._turn = init_turn

        if init_config == []:
            self._board = self._make_gameboard()
            #self._board = self._make_test_board() #FOR TESTING GUI!!!
        else:
            self._board = deepcopy(init_config)
        self._test_board = self._make_test_board() #FOR TESTING!!!
        self._game_over = False
        self._winner = None
        self._checking_opp_valid_moves = False

        #For forced situations involving player (e.g., combo jumps):
        self._must_move_again = False
        self._must_move_again_piece = None
        #Perhaps this^ variable can control a
        #highlighted piece in the GUI version...
        self._forced_jumps = []

        #For forced situations involving opponent:
        self._opp_forced = False
        self._opp_forced_pieces = []
        #Perhaps this^ variable can control
        #highlighted pieces in the GUI version...
        self._opp_forced_jumps = []
        
        self._ts_cells = [(0, c) for c in range(self._num_cols)]   #For king'ing situations
        self._bs_cells = [(self._num_rows-1, c) for c in range(self._num_cols)]   #For king'ing situations

        '''
        #TEST PIECE ARRANGEMENTS
        self._board[0][3] = Piece("B", 0, 3)
        self._board[1][4] = Piece("B", 1, 4)
        #self._board[3][0] = Piece("B", 3, 0)
        self._board[2][1] = Piece("R", 2, 1)
        self._board[6][5] = Piece("R", 6, 5)
        '''

    """
    def get_player_color(self):
        '''Returns the color of the human player.'''
        return self._player
    """

    def get_winner(self):
        """
        Returns the winner of the game.
        return: The winner of the game ("B" or "R")
        type: str
        """
        return self._winner


    def need_to_move_again(self):
        """
        Returns a boolean specifying if the player must
        move again to make a combo jump.
        return: A boolean specifying if the player must
                move again to make a combo jump
        rtype: bool
        """
        return self._must_move_again        


    #TODO: Consider renaming this method to must_move_again_pos?
    def must_move_piece(self):
        """
        Returns the 0-based (row, col) that a piece must make
        another move to (after having already made a move. E.g.,
        for double-jumping situations).
        return: A 2-tuple whose components represent the
                0-based (row, col) that a piece must perform
                another move to
        rtype: tuple
        """
        return self._must_move_again_piece


    def opp_is_forced(self):
        """
        Returns a boolean specifying if the opponent is forced to move on
        the next turn (after the player had already moved).
        return: A boolean specifying if the opponent is forced to move on
                the next turn (after the player had already moved).
        rtype: bool
        """
        return self._opp_forced


    def opps_forced_pieces(self):
        '''Returns a list of the pieces that could be moved in the event of
           a forced jump.'''
        return self._opp_forced_pieces


    def _switch_turn(self, cur_turn):
        """
        Switches the player turn in a Checkers game.
        @cur_turn: The current turn ("B" or "R")
        type cur_turn: str
        return: None
        rtype: None
        """
        if cur_turn == "R":
            self._turn = "B"
        else:
            self._turn = "R"


    def _make_test_board(self):
        """
        Makes an empty test board that you can fill in
        to test a particular method.
        return: None
        rtype: None
        """
        board = []
        for i in range(self._num_rows):
            board.append([])
            for j in range(self._num_cols):
                board[-1].append(" ")

        return board


    def print_board(self):
        """
        Prints a board for testing on the console.
        return: None
        rtype: None
        """
        for row in self._board:
            print("")
            for col in row:
                print(".", end=" ") if col == " " else print(col.get_color(), end=" ")
        print() 


    def get_row_num(self):
        """
        Returns the number of rows.
        return: The number of rows
        rtype: int
        """
        return self._rows


    def get_col_num(self):
        """
        Returns the number of cols.
        return: The number of cols
        rtype: int
        """
        return self._cols


    def get_board(self):
        """
        Returns a list representation of a checkers board.
        return: A list representation of a checkers board
        rtype: list
        """
        return self._board


    def get_red_count(self):
        """
        Returns the number of red pieces on the board.
        return: The number of red pieces on the board.
        rtype: int
        """
        return self._count_colors("R")


    def get_black_count(self):
        """
        Returns the number of black pieces on the board.
        return: The number of black pieces on the board.
        rtype: int
        """
        return self._count_colors("B")


    def get_turn(self):
        """
        Returns the current turn.
        return: The current turn ("B" or "R")
        rtype: str
        """
        return self._turn


    def set_winner(self, player):
        """
        Sets the winner of a Checkers game
        to the given player.
        @player: The winning player
        return: None
        rtype: None
        """
        self._winner = player


    def _count_colors(self, color):
        """
        Counts the number of pieces corresponding to the given color.
        @color: The color ("B" or "R") to count pieces for
        type color: str
        return: The number of pieces corresponding to the given color.
        rtype: int
        """
        count = 0
        for row in self._board:
            for col in row:
                if type(col) == Piece and col.get_color() == color:
                    count += 1
        return count


    def make_move(self, p_row, p_col, t_row, t_col):
        """
        Updates a Checkers game state by moving a piece at some starting position to
        a target position. p in p_row and p_col stands for 'piece' and t in t_row and
        t_col stands for 'target'. An i preceding these letters stands for "index" --
        that is, these row and column values are list-index friendly (i.e., 0-based).
        The function is called using non
        0-based indexing.
        @p_row: A checkers piece's starting row before a move
        @p_col: A checkers piece's starting col before a move
        @t_row: A checker piece's target row to move to
        @t_col: A chekcer piece's target col to move to
        type p_row: int
        type p_col: int
        type t_row: int
        type t_col: int
        return: None
        rtype: None
        """
        ip_row, ip_col = p_row-1, p_col-1   
        it_row, it_col = t_row-1, t_col-1

        #THINK: If an exception is thrown in _check_if_valid_piece, nothing
        #       else in this method will be executed...
        self._check_if_valid_piece(ip_row, ip_col)
        jumped_piece, move_type = self._check_if_valid_move(ip_row, ip_col, it_row, it_col)
        #If all of ^those^ checks pass, then go ahead and update the gamestate's board.
        
        self._relocate_piece(ip_row, ip_col, it_row, it_col, jumped_piece)        
        self._check_if_need_to_king(it_row, it_col)

        # - GameOverError is raised in _check_if_opp_can_move
        #Check if opponent has any valid moves left
        self._check_if_opp_can_move()

        self._forced_jumps = [] #(re)set this instance variable to an empty list
        adj_opp_cells = self._board[it_row][it_col].get_adj_opps(it_row, it_col, self._board)
        self._get_forced_jumps(move_type, it_row, it_col, adj_opp_cells)
        #This^ function will append to the _forced_jumps list.
        
        #If self._forced_jumps is empty, then switch turns. Else, it's still the current player's turn and
        #they MUST make a choice (on the next move) of which cells to jump over in the self._forced_jumps list.
        if self._forced_jumps == []:
            self._must_move_again = False
            self._opp_forced_jumps = []
            self._opp_forced_pieces = []
            self._switch_turn(self._turn)
            self._check_if_opp_forced_to_move()
        else:
            self._opp_forced = False
            #^Set to false because the forced move would have already been made at this point
            self._must_move_again = True
            self._must_move_again_piece = (it_row, it_col)


    def _get_forced_jumps(self, move_type, it_row, it_col, adj_opp_cells):
        """
        Gets the jumps that must be made by the current player by
        updating a Checker instance's _forced_jumps attribute.
        @move_type: "jump" or "step"
        @it_row: A 0-based index of a piece's target row to move to
        @it_col: A 0-based index of a piece's target col to move to
        @adj_opp_cells: A list of adjacent cells containing the opponent's pieces.
        type it_row: int
        type it_col: int
        type adj_opp_cells: [str]
        return: None
        rtype: None
        """
        if move_type == "jump":
            for cell in adj_opp_cells:
                if self._board[it_row][it_col].jump_is_possible(
                    it_row, it_col, cell[0], cell[1], self._board):
                    self._forced_jumps.append((2*cell[0]-it_row, 2*cell[1]-it_col))


    def _check_if_opp_forced_to_move(self):
        """
        Determines if the opponent is forced to move when the turn switches to
        theirs by updating a Checkers intance's _opp_forced attribute.
        return: None
        rtype: None
        """
        for i in range(self._num_rows):
            adj_opp_cells = []
            for j in range(self._num_cols):
                if self._board[i][j] != " " and self._board[i][j].get_color() == self._turn:
                    adj_opp_cells = self._board[i][j].get_adj_opps(i, j, self._board)
                    for cell in adj_opp_cells:
                        if self._board[i][j].jump_is_possible(i, j, cell[0], cell[1], self._board):
                            self._opp_forced_jumps.append((2*cell[0]-i, 2*cell[1]-j))
                            self._opp_forced_pieces.append((i, j))

        if self._opp_forced_jumps != []: #There are jumps opponent can make on next turn...
            self._opp_forced = True
        else:
            self._opp_forced = False


    def _check_if_opp_can_move(self):
        """
        Determines if the opposing player can perform anymore
        moves. If not, then the opposing player loses.
        return: None
        rtype: None
        """
        self._checking_opp_valid_moves = True
        (valid_moves_exist, checked_player) = self._valid_moves_exist(
                                                self._opp_player(self._turn))

        #if not valid_moves_exist:
        if not valid_moves_exist or self._count_colors(checked_player) == 0:
            self._set_winner_after_checking(checked_player)
            raise GameOverError
        self._checking_opp_valid_moves = False


    def _relocate_piece(self, ip_row, ip_col, it_row, it_col, jumped_piece):
        """
        Relocates a piece and "captures" an opposing piece if a jumped piece exists.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        @it_row: A 0-based index of a target square's row
        @it_col: A 0-based index of a target square's col
        type ip_row: int
        type ip_col: int
        type it_row: int
        type it_col: int
        return: None
        rtype: None
        """
        #replace targ position with chosen piece:
        self._board[it_row][it_col] = self._board[ip_row][ip_col]
        #set new position:
        self._board[it_row][it_col].set_new_pos(it_row, it_col)
        self._board[ip_row][ip_col] = " "
        
        if jumped_piece != None:
            self._board[jumped_piece[0]][jumped_piece[1]] = " " 


    def _check_if_need_to_king(self, it_row, it_col):
        """
        Determines if a piece that was just placed in a
        target (row, column) needs to be king'd.
        @it_row: A 0-based index of a target square's row
        @it_col: A 0-based index of a target square's col
        type it_row: int
        type it_col: int
        return: None
        rtype: None
        """
        red_to_other_side = self._turn == "R" and (it_row, it_col) in self._ts_cells and \
                            not self._board[it_row][it_col].piece_is_king()
        black_to_other_side = self._turn == "B" and (it_row, it_col) in self._bs_cells and \
                              not self._board[it_row][it_col].piece_is_king()

        if (red_to_other_side or black_to_other_side):
            self._board[it_row][it_col].set_to_king()


    def _set_winner_after_checking(self, checked_player):
        """
        Sets the winner of the game after checking if
        the opponent had any moves left.
        return: None
        rtype: None
        """
        self._winner = self._opp_player(checked_player)


    def _opp_player(self, cur_player):
        """
        Returns the opposite player of the one passed in as an argument.
        @cur_player: The player to get the opposite player for
        type player: str
        return: "B" if cur_player is "R", else "R"
        rtype: None
        """
        return "B" if cur_player == "R" else "R"


    def _check_if_valid_piece(self, ip_row, ip_col):
        """
        Determines if the selected (row, column) contains a valid piece.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        type ip_row: int
        type ip_col: int
        return: None
        rtype: None
        """
        if (not self._within_row_nums(ip_row) or not self._within_col_nums(ip_col)
            or not self._piece_matches_turn(ip_row, ip_col)):
            print("IN _check_if_valid_piece's if 1:")
            print((ip_row, ip_col))
            print(not self._within_row_nums(ip_row))
            print(not self._within_col_nums(ip_col))
            print(not self._piece_matches_turn(ip_row, ip_col))
            raise InvalidMoveError("valid piece not selected")

        if self._must_move_again and (ip_row, ip_col) != self._must_move_again_piece:
            print("IN _check_if_valid_piece's if 2:")
            raise InvalidMoveError("valid piece not selected")

        if self._opp_forced and (ip_row, ip_col) not in self._opp_forced_pieces:
            print("IN _check_if_valid_piece's if 3:")
            raise InvalidMoveError("valid piece not selected")


    def _within_row_nums(self, i_row):
        """
        Returns a boolean indicating if a given row is within
        the appropriate range of row numbers (0 through 7).
        @i_row: A 0-based index for a row
        type i_row: int
        return: A boolean indicating if a given row is within
                the appropriate range of row numbers (0 through 7).
        rtype: bool
        """
        return 0 <= i_row <= self._num_rows-1


    def _within_col_nums(self, i_col):
        """
        Returns a boolean indicating if a given col is within
        the appropriate range of column numbers (0 through 7).
        @i_col: A 0-based index for a col
        type i_col: int
        return: A boolean indicating if a given col is within
                the appropriate range of column numbers (0 through 7).
        rtype: bool
        """
        return 0 <= i_col <= self._num_cols-1


    def _piece_matches_turn(self, ip_row, ip_col):
        """
        Determines if the piece selected matches the current turn.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        type ip_row: int
        type ip_col: int
        return: True if the selected piece matches the current
                turn ("B" or "R") or False otherwise.
        rtype: bool
        """
        return (self._board[ip_row][ip_col] != " "
                and self._board[ip_row][ip_col].get_color() == self._turn)


    def _check_if_valid_move(self, ip_row, ip_col, it_row, it_col):
        """
        Determines if the target (row, column) represents a valid
        movement. If no exceptions were raised, a list of cell pos-
        itions to flip as well as the type of move just performed
        (jump or step) is returned.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        @it_row: A 0-based index of a target square's row
        @it_col: A 0-based index of a target square's col
        return: If no exceptions were raised, a tuple whose first
                component is the position of a piece that was jumped
                and whose second component is the type of move just
                performed (jump or step).
        rtype: list
        """
        #Is it out of bounds?
        if not self._within_row_nums(it_row) or not self._within_col_nums(it_col):
            raise OutOfBoundsError
        
        #Is it onto another piece?
        if self._board[it_row][it_col] != " ":
            raise InvalidMoveError("cannot move onto another piece.")

        if not self._checking_opp_valid_moves and self._must_move_again and (it_row, it_col) not in self._forced_jumps:
            raise InvalidMoveError("didn't make a valid jump")

        if not self._checking_opp_valid_moves and self._opp_forced and (it_row, it_col) not in self._opp_forced_jumps:
            raise InvalidMoveError("didn't make a valid jump")

        if self._move_is_jump(ip_row, ip_col, it_row, it_col):
            if not self._board[ip_row][ip_col].valid_jump(it_row, it_col, self._board):
                raise InvalidMoveError("was not a valid jump")
            jumped_piece = self._board[ip_row][ip_col].get_jumped_piece_coord(
                                    ip_row, ip_col, it_col, it_row)
            return (jumped_piece, "jump")
        elif self._move_is_step(ip_row, ip_col, it_row, it_col):
            if ((it_row, it_col) not in self._board[ip_row][ip_col].possible_step_dirs()):
                raise InvalidMoveError("was not a valid step")
            return (None, "step")           
        else:
            raise InvalidMoveError("move was just straigt up invalid")


    def _move_is_jump(self, ip_row, ip_col, it_row, it_col):
        """
        Determines if a move is a jump.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        @it_row: A 0-based index of a target square's row
        @it_col: A 0-based index of a target square's col
        return: True if the move performed is a jump or False otherwise
        rtype: boolean
        """
        return ((it_row, it_col) == (ip_row-2, ip_col-2) or   #Upper-left jump
                (it_row, it_col) == (ip_row-2, ip_col+2) or   #Upper-right jump
                (it_row, it_col) == (ip_row+2, ip_col+2) or   #Lower-right jump
                (it_row, it_col) == (ip_row+2, ip_col-2))     #Lower-left jump 


    #Code Refactoring Idea: Perhaps this method wouldn't be necessary
    #if you you simply put "not obj._move_is_jump" in its place?
    def _move_is_step(self, ip_row, ip_col, it_row, it_col):
        """
        Determines if a move is a step.
        @ip_row: A 0-based index of a player's row
        @ip_col: A 0-based index of a player's col
        @it_row: A 0-based index of a target square's row
        @it_col: A 0-based index of a target square's col
        return: True if the move performed is a step or False otherwise
        rtype: bool
        """
        return ((it_row, it_col) == (ip_row-1, ip_col-1) or   #Upper-left step
                (it_row, it_col) == (ip_row-1, ip_col+1) or   #Upper-right step
                (it_row, it_col) == (ip_row+1, ip_col+1) or   #Lower-right step
                (it_row, it_col) == (ip_row+1, ip_col-1))     #Lower-left step


    def _make_gameboard(self):
        """
        Creates a list representation of a checkers board.
        return: A list representation of a checkers board with
                game pieces in their proper positions.
        type: list
        """
        board = []
        for i_row in range(self._num_rows):
            board.append([])
            for i_col in range(self._num_cols):
                if 0 <= i_row <= 2:
                    self._init_start_pos("B", board, i_row, i_col)
                elif 5 <= i_row <= 7:
                    self._init_start_pos("R", board, i_row, i_col)
                else:
                    board[-1].append(" ")
                
        return board


    def _init_start_pos(self, color, board, i_row, i_col):
        """
        Establishes the initial arrangements of the red or black pieces.
        Note that no return type has been specified because the game
        board being modified (a list) has pass-by-reference characteristics.
        @color: The color of the pieces to arrange
        @board: A list representation of a gameboard
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        type i_row: int
        type i_col: int
        return: None
        rtype: None
        """
        if ((i_row % 2 == 0 and i_col % 2 != 0) or
            (i_row % 2 != 0 and i_col % 2 == 0)):
            board[-1].append(Piece(color, i_row, i_col))
        else:
            board[-1].append(" ")    


    def _valid_moves_exist(self, turn, check_for_cpu=False):
        """
        Determines if any moves exist for the given player. If check_for_cpu
        is False, then returns a 2-tuple whose first component is a boolean
        specifying if moves and whose second component is the player color for
        which this check was carried out for. If check_for_cpu is True, then
        a list of valid moves is returned (used in implementing the AI).
        @turn: The turn (i.e., "B" or "R") to check the existence of valid moves for
        @check_for_cpu: A boolean indicating if this check for valid moves
                        was for the CPU's turn.
        type turn: str
        type check_for_cpu: bool
        return: If check_for_cpu is False, then returns a 2-tuple whose first
                component is a boolean specifying if moves and whose second
                component is the player color for which this check was carried
                out for. If check_for_cpu is True, then a list of valid moves
                is returned (used in implementing the AI).
        """
        valid_moves = []        
        if not self._opp_forced:
            tr_cell = (0, len(self._board[0])-1) #No need for top LEFT cuz no piece is ever gonna be there
            bl_cell = (len(self._board)-1, 0) #No need for bottom RIGHT cuz no piece is ever gonna be there
            ls_cells = [(c, 0) for c in range(1, len(self._board)-2, 2)] 
            rs_cells = [(c, len(self._board[0])-1) for c in range(2, len(self._board)-1, 2)] 
            ts_cells = [(0, c) for c in range(1, len(self._board[0])-1, 2)] 
            bs_cells = [(len(self._board)-1, c) for c in range(2, len(self._board[0])-1, 2)]

            #Loop through each of the cells. If there's a piece there, see if it can do a jump or a
            #step (with self._check_if_valid_move)
            for i_row in range(self._num_rows):
                for i_col in range(self._num_cols):
                    piece = self._board[i_row][i_col]
                    if piece != " " and piece.get_color() == turn and (i_row, i_col) == tr_cell:
                        self._check_moves_in_tr_cell(i_row, i_col, valid_moves)                    
                    elif piece != " " and piece.get_color() == turn and (i_row, i_col) == bl_cell:
                        self._check_moves_in_bl_cell(i_row, i_col, valid_moves)                    
                    elif piece != " " and piece.get_color() == turn and (i_row, i_col) in ls_cells:
                        self._check_moves_in_ls_cells(i_row, i_col, valid_moves, turn, piece.piece_is_king())                    
                    elif piece != " " and piece.get_color() == turn and (i_row, i_col) in rs_cells:
                        self._check_moves_in_rs_cells(i_row, i_col, valid_moves, turn, piece.piece_is_king())                
                    elif piece != " " and piece.get_color() == turn and (i_row, i_col) in ts_cells:
                        self._check_moves_in_ts_cells(i_row, i_col, valid_moves, turn)                    
                    elif piece != " " and piece.get_color() == turn and (i_row, i_col) in bs_cells:
                        self._check_moves_in_bs_cells(i_row, i_col, valid_moves, turn)                    
                    elif piece != " " and piece.get_color() == turn:
                        self._check_moves_in_nb_cells(i_row, i_col, valid_moves, turn, piece.piece_is_king())
        else:
            #NOTE: In checkers, IT'S REQUIRED that you make a jump if a jump is available.
            for i in range(len(self._opp_forced_pieces)):
                valid_moves.append(self._opp_forced_pieces[i]+self._opp_forced_jumps[i]+("jump",))
                
        return (valid_moves != [], turn) if not check_for_cpu else valid_moves


    def _check_moves_in_tr_cell(self, i_row, i_col, valid_moves):
        """
        Determines what moves can be done in the top-right cell.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the piece
                      in the top-right corner of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        self._try_move(i_row, i_col, i_row+1, i_col-1, valid_moves) #down-left step
        self._try_move(i_row, i_col, i_row+2, i_col-2, valid_moves) #down-left jump


    def _check_moves_in_bl_cell(self, i_row, i_col, valid_moves):
        """
        Determines what moves can be done in the bottom-left cell.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the piece
                      in the bottom-left corner of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        self._try_move(i_row, i_col, i_row-1, i_col+1, valid_moves) #up-right step
        self._try_move(i_row, i_col, i_row-1, i_col+1, valid_moves) #up-right step
        self._try_move(i_row, i_col, i_row-2, i_col+2, valid_moves) #up-right jump
        

    def _check_moves_in_ls_cells(self, i_row, i_col, valid_moves, turn, is_king):
        """
        Determines what moves can be done in the left side of the gameboard.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the pieces
                      in the left side of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        if turn == "R" or is_king:
            self._try_move(i_row, i_col, i_row-1, i_col+1, valid_moves) #up-right step
            self._try_move(i_row, i_col, i_row-2, i_col+2, valid_moves) #up-right jump
        if turn == "B" or is_king:
            self._try_move(i_row, i_col, i_row+1, i_col+1, valid_moves) #down-right step
            self._try_move(i_row, i_col, i_row+2, i_col+2, valid_moves) #down-right jump


    def _check_moves_in_rs_cells(self, i_row, i_col, valid_moves, turn, is_king):
        """
        Determines what moves can be done in the right side of the gameboard.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the pieces
                      in the right side of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        if turn == "R" or is_king:
            self._try_move(i_row, i_col, i_row-1, i_col-1, valid_moves) #up-left step
            self._try_move(i_row, i_col, i_row-2, i_col-2, valid_moves) #up-left jump
        if turn == "B" or is_king:
            self._try_move(i_row, i_col, i_row+1, i_col-1, valid_moves) #down-left step
            self._try_move(i_row, i_col, i_row+2, i_col-2, valid_moves) #down-left jump


    def _check_moves_in_ts_cells(self, i_row, i_col, valid_moves, turn):
        """
        Determines what moves can be done in the top side of the gameboard.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the pieces
                      in the top side of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        self._try_move(i_row, i_col, i_row+1, i_col+1, valid_moves) #down-right step        
        self._try_move(i_row, i_col, i_row+2, i_col+2, valid_moves) #down-right jump        
        self._try_move(i_row, i_col, i_row+1, i_col-1, valid_moves) #down-left step        
        self._try_move(i_row, i_col, i_row+2, i_col-2, valid_moves) #down-left jump


    def _check_moves_in_bs_cells(self, i_row, i_col, valid_moves, turn):
        """
        Determines what moves can be done in the bottom side of the gameboard.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the pieces
                      in the bottom side of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        self._try_move(i_row, i_col, i_row-1, i_col-1, valid_moves) #up-left step
        self._try_move(i_row, i_col, i_row-2, i_col-2, valid_moves) #up-left jump
        self._try_move(i_row, i_col, i_row-1, i_col+1, valid_moves) #up-right step
        self._try_move(i_row, i_col, i_row-2, i_col+2, valid_moves) #up-right jump
    

    def _check_moves_in_nb_cells(self, i_row, i_col, valid_moves, turn, is_king):
        """
        Determines what moves can be done in the
        non-boundary cells of the gameboard.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        @valid_moves: A list to append valid moves to for the pieces
                      in the non-boundary cells of the gameboard
        type i_row: int
        type i_col: int
        type valid_moves: [tuple]
        return: None
        rtype: None
        """
        if turn == "R" or is_king:
            self._try_move(i_row, i_col, i_row-1, i_col-1, valid_moves) #up-left step
            self._try_move(i_row, i_col, i_row-2, i_col-2, valid_moves) #up-left jump
            self._try_move(i_row, i_col, i_row-1, i_col+1, valid_moves) #up-right step
            self._try_move(i_row, i_col, i_row-2, i_col+2, valid_moves) #up-right jump
        if turn == "B" or is_king:
            self._try_move(i_row, i_col, i_row+1, i_col+1, valid_moves) #down-right step
            self._try_move(i_row, i_col, i_row+2, i_col+2, valid_moves) #down-right jump
            self._try_move(i_row, i_col, i_row+1, i_col-1, valid_moves) #down-left step
            self._try_move(i_row, i_col, i_row+2, i_col-2, valid_moves) #down-left jump


    def _try_move(self, ip_row, ip_col, it_row, it_col, valid_moves):
        """
        Tries executing a move and appends the move to a list if
        successful (i.e., no exceptions are thrown). A move is a
        4-tuple of the following format:
            (starting row, starting column,
             targ row, targ column,
             move type (e.g., "step", "jump"))
        @ip_row: A 0-based index of a piece's starting row
        @ip_col: A 0-based index of a piece's starting col
        @it_row: A 0-based index of a target position's row
        @it_col: A 0-based index of a target position's col
        @valid_moves: A list to append the 4-tuple:
                        (ip_row, ip_col, it_row,
                         it_col, move_type)
                      to if the move is valid.
        type ip_row: int
        type ip_col: int
        type it_row: int
        type it_col: int
        type valid_moves: list
        return: None
        rtype: None
        """
        try:
            dummy, move_type = self._check_if_valid_move(ip_row, ip_col, it_row, it_col)
            valid_moves.append((ip_row, ip_col, it_row, it_col, move_type)) #need move_type for AI
            #Example move: (0, 3, 1, 4, 'step')
        except:
            pass




class Piece:
    """ Represents a checkers piece. """

    def __init__(self, color, ip_row, ip_col):
        """
        Initializes the attributes of a Piece.
        @color: The color of the piece ("R" or "B")
        @ip_row: A 0-based index of a piece's starting row
        @ip_col: A 0-based index of a piece's starting col
        type ip_row: int
        type ip_col: int
        """
        self._color = color
        self._opp = self.opp_piece()
        self._is_king = False
        self._pos = (ip_row, ip_col)


    def piece_is_king(self):
        """
        Determines if this Piece is a king.
        return: True if the piece if a king or false otherwise
        rtype: bool
        """
        return self._is_king


    def set_to_king(self):
        """
        Sets this Piece to a king piece.
        return: None
        rtype: None
        """
        self._is_king = True


    def set_new_pos(self, i_row, i_col):
        """
        Sets a new row and column position for a piece.
        @i_row: A 0-based row index
        @i_col: A 0-based col index
        type i_row: int
        type i_col: int
        """
        self._pos = (i_row, i_col)


    def get_color(self):
        """
        Returns the color of a Piece.
        return: The color of the piece ("B" or "R")
        rtype: str
        """
        return self._color


    def possible_step_dirs(self):
        """
        Returns all the possible directions a particular type of piece can step in.
        return: A tuple containing all the possible directions (in the form of 2-tuples
                the represent a board position) that a piece can perform a step in.
        rtype: tuple
        """
        if self._is_king:
            return ((self._pos[0]-1, self._pos[1]+1),   #upper-right
                    (self._pos[0]-1, self._pos[1]-1),   #upper-left
                    (self._pos[0]+1, self._pos[1]-1),   #lower-left
                    (self._pos[0]+1, self._pos[1]+1))   #lower-right
        
        elif self._color == "R":
            return ((self._pos[0]-1, self._pos[1]+1),   #upper-right
                    (self._pos[0]-1, self._pos[1]-1))   #upper-left

        elif self._color == "B":
            return ((self._pos[0]+1, self._pos[1]-1),   #lower-left
                    (self._pos[0]+1, self._pos[1]+1))   #lower-right


    def valid_jump(self, it_row, it_col, board):
        """
        Determines if a Piece in a cell can perform the targeted jump.
        @it_row: A 0-based index of a target position's row
        @it_col: A 0-based index of a target position's col
        @board: A 2D list that represents a gameboard
        type it_row: int
        type it_col: int
        type board: list
        return: True if a Piece can perform the targeted (it_row, it_col)
                jump or False otherwise.
        rtype: bool
        """
        if self._is_king:
            #(upper-right jump and upper-right pos) or (upper-left jump and upper-left pos)
            #or (lower-left jump and lower-left pos) or (lower-right jump and lower-right pos)
            return ((self._jump_is_diagonal(self._pos[0]-2, self._pos[1]+2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]-1, self._pos[1]+1, board)) or\
                    (self._jump_is_diagonal(self._pos[0]-2, self._pos[1]-2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]-1, self._pos[1]-1, board)) or\
                    (self._jump_is_diagonal(self._pos[0]+2, self._pos[1]-2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]+1, self._pos[1]-1, board)) or\
                    (self._jump_is_diagonal(self._pos[0]+2, self._pos[1]+2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]+1, self._pos[1]+1, board)))
        elif self._color == "R":
            return ((self._jump_is_diagonal(self._pos[0]-2, self._pos[1]+2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]-1, self._pos[1]+1, board)) or\
                    (self._jump_is_diagonal(self._pos[0]-2, self._pos[1]-2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]-1, self._pos[1]-1, board)))
        elif self._color == "B":
            return ((self._jump_is_diagonal(self._pos[0]+2, self._pos[1]-2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]+1, self._pos[1]-1, board)) or\
                    (self._jump_is_diagonal(self._pos[0]+2, self._pos[1]+2, it_row, it_col) and\
                    self._jumped_piece_is_opp(self._pos[0]+1, self._pos[1]+1, board)))
        

    def _jump_is_diagonal(self, ip_row, ip_col, it_row, it_col):
        """
        Determines if the jump movement of a chosen piece is diagonal
        (in cases where a user may erroneously attempt a jump that
        is not diagonal)
        @ip_row: A 0-based index of a piece's starting row
        @ip_col: A 0-based index of a piece's starting col
        @it_row: A 0-based index of a target position's row
        @it_col: A 0-based index of a target position's col
        type ip_row: int
        type ip_col: int
        type it_row: int
        type it_col: int
        return: True if the jump movement of a Piece is diagonal
                or False otherwise
        rtype: bool
        """
        return (it_row, it_col) == (ip_row, ip_col)


    def _jumped_piece_is_opp(self, ijp_row, ijp_col, board):
        """
        Determines if a piece that is jumped over belongs to the opponent.
        @ijp_row: A 0-based index row of a piece that is to be jumped
        @ijp_col: A 0-based index row of a piece that is to be jumped
        @board: A 2D list that represents a gameboard
        type ijp_row: int
        type ijp_col: int
        type board: list
        return: True if a piece that is jumped over belongs to the
                opponent or False otherwise
        rtype: bool
        """
        return board[ijp_row][ijp_col] != " " and board[ijp_row][ijp_col].get_color() == self._opp
    

    def get_jumped_piece_coord(self, ip_row, ip_col, it_col, it_row):
        """
        Returns the (row, col) of a Piece that was just jumped.
        @ip_row: A 0-based index of a piece's starting row
        @ip_col: A 0-based index of a piece's starting col
        @it_row: A 0-based index of a target position's row
        @it_col: A 0-based index of a target position's col
        type ip_row: int
        type ip_col: int
        type it_row: int
        type it_col: int
        return: The (row, col) of a Piece that was jumped
        rtype: tuple
        """
        return (int((ip_row+it_row)/2), int((ip_col+it_col)/2))


    def get_adj_opps(self, i_row, i_col, board):
        """
        Returns a list of all cells that are adjacent to the
        given cell and contain an opposing piece.
        @i_row: A 0-based row index of the current Piece's cell
        @i_col: A 0-based col index of the current Piece's cell
        type i_row: int
        type i_col: int
        return: A list of all cells that are adjacent to
                the current Piece
        rtype: [tuple]
        """
        adj_opp_cells = []
        tr_cell = (0, len(board[0])-1) #No need for top LEFT cuz no piece is ever gonna be there
        bl_cell = (len(board)-1, 0) #No need for bottom RIGHT cuz no piece is ever gonna be there
        ls_cells = [(c, 0) for c in range(1, len(board)-2, 2)] 
        rs_cells = [(c, len(board[0])-1) for c in range(2, len(board)-1, 2)] 
        ts_cells = [(0, c) for c in range(1, len(board[0])-1, 2)] 
        bs_cells = [(len(board)-1, c) for c in range(2, len(board[0])-1, 2)]
        
        if (i_row, i_col) == tr_cell:
            self._adjacency_check(i_row+1, i_col-1, board, adj_opp_cells) #diagonally down-left
        elif (i_row, i_col) == bl_cell:
            self._adjacency_check(i_row-1, i_col+1, board, adj_opp_cells) #diagonally up-right
        elif (i_row, i_col) in ls_cells: #If in left side cells...
            if self._color == "R" or self._is_king:
                self._adjacency_check(i_row-1, i_col+1, board, adj_opp_cells) #diagonally up-right
            if self._color == "B" or self._is_king:
                self._adjacency_check(i_row+1, i_col+1, board, adj_opp_cells) #diagonally down-right
        elif (i_row, i_col) in rs_cells: #If in right side cells...
            if self._color == "R" or self._is_king:
                self._adjacency_check(i_row-1, i_col-1, board, adj_opp_cells) #diagonally up-left
            if self._color == "B" or self._is_king:
                self._adjacency_check(i_row+1, i_col-1, board, adj_opp_cells) #diagonally down-left
        elif (i_row, i_col) in ts_cells: #If in top side cells...
            self._adjacency_check(i_row+1, i_col+1, board, adj_opp_cells) #diagonally down-right
            self._adjacency_check(i_row+1, i_col-1, board, adj_opp_cells) #diagonally down-left
        elif (i_row, i_col) in bs_cells: #If in bottom side cells...
            self._adjacency_check(i_row-1, i_col-1, board, adj_opp_cells) #diagonally up-left
            self._adjacency_check(i_row-1, i_col+1, board, adj_opp_cells) #diagonally up-right
        else: #Piece is in non-boundary
            if self._color == "R" or self._is_king:
                self._adjacency_check(i_row-1, i_col-1, board, adj_opp_cells) #diagonally up-left
                self._adjacency_check(i_row-1, i_col+1, board, adj_opp_cells) #diagonally up-right
            if self._color == "B" or self._is_king:
                self._adjacency_check(i_row+1, i_col+1, board, adj_opp_cells) #diagonally down-right
                self._adjacency_check(i_row+1, i_col-1, board, adj_opp_cells) #diagonally down-left

        return adj_opp_cells
    

    def opp_piece(self):
        """
        Returns the opposite color of this Piece.
        return: The opposite color of this Piece ("B" or "R").
                I.e., this Piece's opponent.
        rtype: str
        """
        return "B" if self._color=="R" else "R"


    def _adjacency_check(self, iadj_row, iadj_col, board, lst):
        """
        Determines if the given adjacent cell contains an opposing
        piece and appends it to the provided list if True.
        @iadj_row: A 0-based index of the adjacent cell's row
        @iadj_col: A 0-based index of the adjacent cell's col
        @board: A 2D list that represents a gameboard
        @lst: The list to append the given adjacent cell to if
              the adjacent cell contains an opposing piece.
        type iadj_row: int
        type iadj_col: int
        type board: list
        type lst: list
        """
        if board[iadj_row][iadj_col] != " " and board[iadj_row][iadj_col].get_color() == self._opp:
            lst.append((iadj_row, iadj_col))


    def jump_is_possible(self, ip_row, ip_col, iadj_row, iadj_col, board):
        """
        Determines if a jump can be made given a Piece's position
        and a position adjacent to it.
        @ip_row: A 0-based index of a piece's starting row
        @ip_col: A 0-based index of a piece's starting col
        @iadj_row: A 0-based index of the adjacent cell's row
        @iadj_col: A 0-based index of the adjacent cell's col
        @board: A 2D list that represents a gameboard
        type ip_row: int
        type ip_col: int
        type iadj_row: int
        type iadj_col: int
        type board: list
        return: True if a jup can be made given a Piece's position
                and a position adjacent to it or False otherwise.
        rtype: bool
        """
        #The following is derived from the midpoint formula. Note how an empty
        #space between two other spaces A and B on the same diagonal is the
        #midpoint between A and B.
        cand_targ_row = 2*iadj_row - ip_row
        cand_targ_col = 2*iadj_col - ip_col
        
        #check if out of bounds...
        if not 0 <= cand_targ_row <= len(board)-1:
            return False
        if not 0 <= cand_targ_col <= len(board[0])-1:
            return False

        return board[cand_targ_row][cand_targ_col] == " "




if __name__ == "__main__":
    pass


    
