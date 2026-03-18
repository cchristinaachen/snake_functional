import tkinter as tk
from tkinter import messagebox
import random
# ==================== Global Variables ====================
# Game configuration
GRID_SIZE = 20
CELL_SIZE = 25
INITIAL_GAME_SPEED = 600  # Start slower (higher value = slower)
MIN_GAME_SPEED = 50  # Fastest speed
SPEED_DECREASE = 15  # Speed up by this amount each food eaten

# Game state
snake = []
food_pos = None
direction = (1, 0)  # Right
next_direction = (1, 0)
score = 0
game_over = False
paused = False
current_speed = INITIAL_GAME_SPEED

# Direction constants
DIRECTIONS = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

# GUI components (global variables)
root = None
canvas = None
score_label = None

def create_gui():
    global root, canvas, score_label   
    root = tk.Tk()
    root.title("Snake Game - Functional Version")
    root.geometry("600x700")
    root.resizable(False, False)

    # Title and score
    header_frame = tk.Frame(root, bg="#2c3e50", height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    title_label = tk.Label(
        header_frame,
        text="🐉 Snake Game (Functional)",
        font=("Arial", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=(2, 2))
                    

# main routine
def main():
    global root

    create_gui()
    root.mainloop()


if __name__ == "__main__":
    main()