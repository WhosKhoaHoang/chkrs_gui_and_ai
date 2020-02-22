#Contains the class for the checkerboard GUI.

import tkinter, checkers, math, scoreboardgui, time, checkersai
_INIT_CELL_WIDTH = 50
_INIT_CELL_HEIGHT = 50

class CheckersBoard:

    def __init__(self, hum_player = "B", cpu_opp = "None", allow_forced_piece_hls=True):
        '''Initializes the attributes of a Checkers GUI game.'''
        self._root = tkinter.Tk()
        self._root.configure(background="black")
        self._root.wm_title("Checkers")

        self._gamestate = checkers.Checkers(init_turn="B")
        self._num_rows = 8
        self._num_cols = 8

        self._canvas = tkinter.Canvas(master = self._root,
                                      height = self._num_rows*_INIT_CELL_HEIGHT-5,
                                      width = self._num_cols*_INIT_CELL_WIDTH-5)
        
        self._canvas.grid(row=1, column=0, padx=30, pady=30,
                          sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E)
                          #^NEED TO SPECIFY sticky OPTION FOR RESIZING!!!
        
        self._canvas.configure(highlightbackground="yellow")
        self._root.rowconfigure(1, weight=1) #NEED THIS FOR RESIZING
        self._root.columnconfigure(0, weight=1) #NEED THIS FOR RESIZING

        self._canvas.bind("<Configure>", self._on_canvas_resize) #NEED THIS FOR RESIZING
        self._canvas.bind("<Button-1>", self._on_canvas_click)
        self._tl_br_corners = []
        self._corner_mappings = dict() #Basically used to access the squares on your board.
        self._cur_piece_id = 0 #For deleting highlights
        self._chosen_cell = None #In particular, the tl and br corners of the highlighted cell
        self._targ_pos = None
        self._cell_chosen_yet = False
        self._invalid_move_made = False
        self._allow_forced_piece_hls = allow_forced_piece_hls

        self._hum_player = hum_player
        self._cpu_player = "B" if hum_player == "R" else "R"
        self._cpu_opp = cpu_opp

        self._must_move_cell = None
        self._must_move_cell_id = 0
        
        self._must_move_cell_lst = []
        self._must_move_cell_id_lst = []

        self._scoreboard = scoreboardgui.ScoreBoardGUI(self._root, self._gamestate, background="gray",
                                                       borderwidth=5, relief=tkinter.RAISED)
        self._scoreboard.grid(row=0, column=0,
                               sticky=tkinter.N+tkinter.S+tkinter.W+tkinter.E, padx=20, pady=(20,0))


    def start(self):
        '''Runs the mainloop on the root window.'''
        self._root.mainloop()


    def _on_canvas_click(self, event):
        '''An event handler that processes left mouse button clicks.'''
        self._canvas.delete(self._cur_piece_id)
        midpoint_mappings = self._get_mappings(self._tl_br_corners, "midpoints")
        self._corner_mappings = self._get_mappings(self._tl_br_corners, "corners")
        #In Othello, this was an instance variable so that you didn't have to pass it around?

        if self._gamestate.get_winner() == None:
            if self._cpu_opp == "None":
                self._player_move(event, midpoint_mappings)
            else:
                if self._gamestate.get_turn() == self._hum_player:
                    self._player_move(event, midpoint_mappings)
                if self._gamestate.get_turn() == self._cpu_player:
                    self._cpu_move(event, midpoint_mappings)
        else:
            self._root.destroy()


    def _player_move(self, event, midpoint_mappings):
        '''Executes a human player's move.'''
        self._invalid_move_made = False #False for now. If you put this after the try/except block,
        #then the invalid move indication wouldn't show up on the scoreboard GUI!
        if not self._cell_chosen_yet:
            self._highlight_clicked_piece(event, midpoint_mappings)
        else:
            i_row, i_col = self._chosen_cell[0], self._chosen_cell[1]
            self._targ_pos = self._find_nearest_cell(event, midpoint_mappings)
            self._try_move(event, midpoint_mappings)

            #The code in _update_GUI board was originally exclusively in this function in this section


    #FOCUS HERE
    def _cpu_move(self, event, midpoint_mappings):
        '''Executes a CPU player's move.'''        
        while (self._gamestate.get_turn() == self._cpu_player
               and self._gamestate.get_winner() == None):
            if self._cpu_opp == "Random Randy":
                move_made = checkersai.random_randy(self._gamestate, self._cpu_player)
                #move_made is a 4-tuple: (ip_row, ip_col, it_row, it_col)
                print("Move that was made:")
                print(move_made)
            elif self._cpu_opp == "Mini Max":
                
                print("\n\n")
                print("IN Mini Max BLOCK")
                print(self._gamestate)
                print(self._hum_player)
                print("\n\n")

                #move_made = checkersai.minimax(self._gamestate, self._cpu_player, 3)
                move_made = checkersai.minimax(self._gamestate, self._cpu_player, 3)[1]
                print("Move that was made:")
                print(move_made)

            #I think these lines of code should only be executed if a valid move exists...
            if move_made != None:
                self._highlight_clicked_piece(event, midpoint_mappings, for_cpu=True,
                                              cpu_row_col = (move_made[0], move_made[1]))
                self._root.update()
                time.sleep(0.5) #To give time for human to see what move was selected.
                self._try_move(event, midpoint_mappings, for_cpu=True,
                               cpu_row_col = (move_made[2], move_made[3]))

            else: #If a move does exist...
                #Switch turns?
                pass


    def _try_move(self, event, midpoint_mappings, for_cpu=False, cpu_row_col=None):
        '''Tries to perform a move executed by a player.'''
        self._targ_pos = cpu_row_col if for_cpu else self._find_nearest_cell(event, midpoint_mappings)
        i_row, i_col = self._chosen_cell[0], self._chosen_cell[1]
        
        #Without the try and except, the game logic will crash (you wouldn't be able to play anymore,
        #but the GUI window will still be up)
        try:
            self._gamestate.make_move(i_row+1, i_col+1, self._targ_pos[0]+1, self._targ_pos[1]+1)
        except checkers.GameOverError:
            self._cell_chosen_yet = False #Get rid of highlights
            self._chosen_cell = None #Get rid of highlights
            self._scoreboard.indicate_result(self._gamestate)
        except checkers.InvalidMoveError:
            #If I want the ability to turn off invalid move indications, I could add an if statement
            #here along the lines of if self._highlight_invalid_move_on or something?
            self._scoreboard.indicate_invalid(self._gamestate)
            self._invalid_move_made = True

        #The following code being in this function is basically equivalent in effect to if we had the
        #code in _player_move. The code being here makes things work for the CPU.
        self._update_GUI_board()


    def _update_GUI_board(self):
        '''Updates the graphical representation of the checkers board.'''        
        self._cell_chosen_yet = False
        self._chosen_cell = None 
        self._draw_board()

        if not self._invalid_move_made and self._gamestate.get_winner() == None:
            self._scoreboard.update_turn_label(self._gamestate)
            self._scoreboard.update_score_label(self._gamestate)


    def _highlight_clicked_piece(self, event, midpoint_mappings, for_cpu=False, cpu_row_col=None):
        '''Highlights the piece clicked on by the player.'''
        if for_cpu:
            self._chosen_cell = cpu_row_col
            i_row, i_col = cpu_row_col[0], cpu_row_col[1]
        else:
            self._chosen_cell = self._find_nearest_cell(event, midpoint_mappings)
            i_row, i_col = self._chosen_cell[0], self._chosen_cell[1]
        self._cur_piece_id = self._draw_selection_highlight(self._corner_mappings)
        self._draw_piece_in_cell(i_row, i_col, self._corner_mappings)
        self._cell_chosen_yet = True

        
    def _on_canvas_resize(self, event):
        '''An event handler that processes window resizes.'''
        self._draw_board()


    def _draw_board(self):
        '''Draws the board and piece arrangements corresponding to a Checkers game state.'''
        self._canvas.delete(tkinter.ALL)
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        delta_x, delta_y = 0, 0
        row, col = 0, 0
        self._tl_br_corners = [] #Reset this to the empty list every time you redraw the board
        
        #DRAW THE SQUARES
        self._draw_squares(row, col, delta_x, delta_y, width, height)
        new_corner_mappings = self._get_mappings(self._tl_br_corners, "corners") #For drawing the pieces
        #^Note how it's this new_corner_mappings that allows any element on the canvas to resize along
        #with the window!!
        
        #DRAW THE PIECES
        self._draw_pieces(new_corner_mappings)

        #DRAW THE SELECTED PIECE HIGHLIGHTS (if any)...
        if self._chosen_cell != None:
            #Make the highlight
            self._cur_piece_id = self._draw_selection_highlight(new_corner_mappings)
            i_row, i_col = self._chosen_cell[0], self._chosen_cell[1]
            self._draw_piece_in_cell(i_row, i_col, new_corner_mappings)
            

        if self._cpu_opp == "None" and self._allow_forced_piece_hls:
            self._check_forced_piece_highlights(new_corner_mappings)
        

    def _check_forced_piece_highlights(self, corner_mappings):
        '''Determines if any highlights need to be made to indicate pieces that must be moved.'''
        if self._gamestate.need_to_move_again() and self._gamestate.get_winner() == None:  #Combo jump situation
            #highlight the piece that needs to move again.
            self._canvas.delete(self._must_move_cell_id)
            #^I don't think deleting makes any difference visually since you're always redrawing,
            #but delete anyway to clear up space.
            self._must_move_cell = self._gamestate.must_move_piece()
            i_row, i_col = self._must_move_cell[0], self._must_move_cell[1]
            self._must_move_cell_id = self._draw_forced_piece_highlight(corner_mappings, i_row, i_col)
            self._draw_piece_in_cell(i_row, i_col, corner_mappings)

        #If opponent is forced to make jump on next turn...
        elif self._gamestate.opp_is_forced() and self._gamestate.get_winner() == None: 
            #highlight the pieces that the opponent could move.
            for num in self._must_move_cell_id_lst:
                self._canvas.delete(num)
            self._must_move_cell_lst = self._gamestate.opps_forced_pieces()
            self._must_move_cell_id_lst = []
            for cell in self._must_move_cell_lst:
                self._must_move_cell_id_lst.append(
                    self._draw_forced_piece_highlight(corner_mappings, cell[0], cell[1]))
                self._draw_piece_in_cell(cell[0], cell[1], corner_mappings)


    def _draw_selection_highlight(self, corner_mappings):
        '''Draws the highlighted cell corresponding to the one selected by the player.'''
        return self._canvas.create_rectangle(corner_mappings[self._chosen_cell][0][0],
                                              corner_mappings[self._chosen_cell][0][1],
                                              corner_mappings[self._chosen_cell][1][0],
                                              corner_mappings[self._chosen_cell][1][1],
                                              outline="yellow", fill = "lightblue", width=4)


    def _draw_forced_piece_highlight(self, corner_mappings, i_row, i_col):
        '''Draws the highlighted cell corresponding to a piece that must be moved.'''
        return self._canvas.create_rectangle(corner_mappings[(i_row, i_col)][0][0],
                                              corner_mappings[(i_row, i_col)][0][1],
                                              corner_mappings[(i_row, i_col)][1][0],
                                              corner_mappings[(i_row, i_col)][1][1],
                                              outline="yellow", fill="green", width=3)


    def _draw_squares(self, row, col, delta_x, delta_y, width, height):
        '''Draws the squares on the board.'''
        for i in range(self._num_rows):
            delta_x = 0 #set x to 0 to restart on the leftmost side of the board
            col = 0
            for j in range(self._num_cols):
                brx, bry = width*(1/self._num_rows)+delta_x, height*(1/self._num_cols)+delta_y
                if (row % 2 == 0 and col % 2 == 0) or (row % 2 != 0 and col % 2 != 0):
                    self._canvas.create_rectangle(delta_x, delta_y, brx, bry,
                                                   outline="yellow", width=3, fill="red")
                    self._tl_br_corners.append([(delta_x, delta_y), (brx, bry)])
                elif row % 2 == 0 and col % 2 != 0 or (row % 2 != 0 and col % 2 == 0):
                    self._canvas.create_rectangle(delta_x, delta_y, brx, bry,
                                                  outline="yellow", width=3, fill="black")
                    self._tl_br_corners.append([(delta_x, delta_y), (brx, bry)])
                col += 1
                delta_x += width*(1/self._num_rows) #x changes as we move across the columns/the board
            row += 1
            delta_y += height*(1/self._num_cols) #delta_y is for moving down the board


    def _get_mappings(self, corners, mode):
        '''Takes a list of the top left and bottom right corners of all the squares on the
           board and maps these corners to their corresponding (i,j)th cell (if mode is "corners")
           or maps the midpoint between these corners to the corresponding (i,j)th cell (if mode is
           "midpoints"). The mapping is represented as a dictionary.'''
        mappings = dict() #recall that dictionaries are not ordered!!!!
        k = 0
        for i in range(self._num_rows):
            for j in range(self._num_cols):
                if mode == "corners":
                    mappings[(i,j)] = corners[k]
                elif mode == "midpoints":
                    mappings[(i,j)] = ((corners[k][0][0]+corners[k][1][0])/2,
                                              (corners[k][0][1]+corners[k][1][1])/2)
                k += 1
                
        return mappings


    def _draw_pieces(self, corner_mappings):
        '''Takes a mapping of cell positions to top left and bottom right corners and draws pieces
           according to how they are arranged for a particular gamestate.'''
        for (i, j) in corner_mappings:
            self._draw_piece_in_cell(i, j, corner_mappings)            


    def _draw_piece_in_cell(self, i_row, i_col, corner_mappings):
        '''Draws the piece within a particular cell.'''
        oval_coords = (corner_mappings[(i_row,i_col)][0][0]+6,
                       corner_mappings[(i_row,i_col)][0][1]+6,
                       corner_mappings[(i_row,i_col)][1][0]-6,
                       corner_mappings[(i_row,i_col)][1][1]-6,)
        if (self._gamestate.get_board()[i_row][i_col] != " "
            and self._gamestate.get_board()[i_row][i_col].get_color() == "B"):
            self._canvas.create_oval(oval_coords, fill="#555", width=3)
            if self._gamestate.get_board()[i_row][i_col].piece_is_king():
                    self._draw_crown(oval_coords[0], oval_coords[1],
                                     oval_coords[2], oval_coords[3])
        elif (self._gamestate.get_board()[i_row][i_col] != " "
              and self._gamestate.get_board()[i_row][i_col].get_color() == "R"):
            self._canvas.create_oval(oval_coords, fill="#d11", width=3)
            if self._gamestate.get_board()[i_row][i_col].piece_is_king():
                    self._draw_crown(oval_coords[0], oval_coords[1],
                                     oval_coords[2], oval_coords[3])


    def _draw_crown(self, tlx, tly, brx, bry):
        '''Takes the corner coordinates of an oval's bounding box and draws a crown inside
           the oval (which represents a checkers piece).'''
        self._canvas.create_polygon([tlx+0.20*(brx-tlx), tly+0.80*(bry-tly),
                                     tlx+0.80*(brx-tlx), tly+0.80*(bry-tly),
                                     tlx+0.80*(brx-tlx), tly+0.20*(bry-tly),

                                     tlx+0.60*(brx-tlx), tly+0.50*(bry-tly),
                                     tlx+0.50*(brx-tlx), tly+0.20*(bry-tly),
                                     tlx+0.40*(brx-tlx), tly+0.50*(bry-tly),
                                     tlx+0.20*(brx-tlx), tly+0.20*(bry-tly),

                                     tlx+0.20*(brx-tlx), tly+0.80*(bry-tly)
                                     ], fill="yellow", width=3, outline="black")
        #^Note how the calculation depends on the difference between the tl and br corners


    def _find_nearest_cell(self, event, midpoint_mappings):
        '''Finds the nearest cell to a mouse click made on the game board.'''
        min_dist = float("inf")
        nearest_cell = (0, 0)
        for item in midpoint_mappings.items():
            dist = math.sqrt((event.x-item[1][0])**2 + (event.y-item[1][1])**2)
            if dist < min_dist:
                nearest_cell = (item[0][0], item[0][1])
                min_dist = dist

        return nearest_cell



#For testing
if __name__ == "__main__":
    #b = CheckersBoard(cpu_opp="Random Randy")
    #b = CheckersBoard(cpu_opp="Random Randy", allow_forced_piece_hls=False)
    b = CheckersBoard(cpu_opp="Mini Max", allow_forced_piece_hls=False)

    b.start()
