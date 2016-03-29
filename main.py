#Contains the entry point into the game.

import checkersgui

if __name__ == "__main__":
    b = checkersgui.CheckersBoard(cpu_opp="Random Randy", allow_forced_piece_hls=False)
    b.start()
