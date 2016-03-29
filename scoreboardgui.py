#Contains the class for the scoreboard GUI.

import tkinter

class ScoreBoardGUI(tkinter.Frame):
    
    def __init__(self, root, gamestate, *args, **kwargs):
        '''Initializes the state of a ScoreBoardGUI object.'''
        tkinter.Frame.__init__(self, root, *args, **kwargs)

        #Note how the master of all these labels is self -- i.e., the Frame itSELF.
        #In the act of extending, we're essentially adding stuff onto a Frame.

        self._turn_text = tkinter.StringVar()
        self._turn_text.set("{}'s turn to move".format("BLACK" if gamestate.get_turn()=="B" else "RED"))
        self._turn_indicator = tkinter.Label(master=self,
                                    textvariable=self._turn_text,
                                    background="gray", font="Arial 15 bold")
        self._turn_indicator.pack(side=tkinter.TOP)

        self._black_score_text = tkinter.StringVar()
        self._black_score_text.set("Black Pieces: {}".format(gamestate.get_black_count()))
        self._black_score = tkinter.Label(master=self, textvariable=self._black_score_text, background="gray")
        self._black_score.pack()

        self._red_score_text = tkinter.StringVar()
        self._red_score_text.set("Red Pieces: {}".format(gamestate.get_red_count()))
        self._red_score = tkinter.Label(master=self, textvariable=self._red_score_text, background="gray")
        self._red_score.pack(side=tkinter.BOTTOM)

        
    def update_turn_label(self, gamestate):
        '''Updates the label indicating whose turn it is.'''
        self._turn_text.set("{}'s turn to move".format("BLACK" if gamestate.get_turn()=="B" else "RED"))

        

    def update_score_label(self, gamestate):
        '''Updates the label indicating the scores.'''
        self._black_score_text.set("Black Pieces: {}".format(gamestate.get_black_count()))
        self._red_score_text.set("Red Pieces: {}".format(gamestate.get_red_count()))


    def indicate_invalid(self, gamestate):
        '''Creates a label to notify the player of an invalid move.'''
        self._turn_text.set("{}'s move invalid. Try again.".format\
                            ("BLACK" if gamestate.get_turn()=="B" else "RED"))



    def indicate_result(self, gamestate):
        '''Creates a label to show the results of a completed game.'''
        if gamestate.get_winner() != None:
            self._turn_text.set("GAME OVER! The winner is {}".format\
                            ("BLACK" if gamestate.get_winner()=="B" else "RED"))
        else:
            self._turn_text.set("GAME OVER! The game is a draw")
        self.update_score_label(gamestate)

        
