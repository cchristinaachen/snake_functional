"""
Snake Game - Functional Programming Version
Using functions and global variables to demonstrate functional programming style
"""

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


# ==================== Utility Functions ====================
def get_opposite_direction(direction):
    """Get the opposite direction"""
    opposites = {
        (0, -1): (0, 1),   # up -> down
        (0, 1): (0, -1),   # down -> up
        (-1, 0): (1, 0),   # left -> right
        (1, 0): (-1, 0)    # right -> left
    }
    return opposites.get(direction, direction)


def is_valid_direction(new_dir, current_dir):
    """Check if direction is valid (cannot reverse)"""
    return new_dir != get_opposite_direction(current_dir)


def generate_food_position():
    """Generate random food position (apple)"""
    global snake
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in snake:
            return (x, y)  # Random position, not on snake


def init_game():
    """Initialize game"""
    global snake, food_pos, direction, next_direction, score, game_over, current_speed
    
    # Snake starts from center with initial length of 3
    center_x = GRID_SIZE // 2
    center_y = GRID_SIZE // 2
    snake = [
        (center_x, center_y),
        (center_x - 1, center_y),
        (center_x - 2, center_y)
    ]
    
    food_pos = generate_food_position()  # Random apple position
    direction = (1, 0)
    next_direction = (1, 0)
    score = 0
    game_over = False
    current_speed = INITIAL_GAME_SPEED  # Reset speed


def check_collision(head_x, head_y):
    """Check collision"""
    global snake
    
    # Check boundaries
    if head_x < 0 or head_x >= GRID_SIZE or head_y < 0 or head_y >= GRID_SIZE:
        return True
    
    # Check if hit itself
    if (head_x, head_y) in snake[1:]:
        return True
    
    return False


def move_snake():
    """Move snake"""
    global snake, direction, next_direction, food_pos, score, game_over, current_speed
    
    if game_over or paused:
        return
    
    # Update direction
    direction = next_direction
    
    # Calculate new head position
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)
    
    # Check collision
    if check_collision(new_head[0], new_head[1]):
        game_over = True
        return
    
    # Add new head
    snake.insert(0, new_head)
    
    # Check if food (apple) is eaten
    if new_head == food_pos:
        score += 1  # Score increases by 1 for each apple
        food_pos = generate_food_position()  # Generate new random apple position
        # Increase speed (decrease delay) each time food is eaten
        current_speed = max(MIN_GAME_SPEED, current_speed - SPEED_DECREASE)
    else:
        # Remove tail if food not eaten
        snake.pop()


def change_direction(new_dir):
    """Change direction"""
    global next_direction, direction
    
    if is_valid_direction(new_dir, direction):
        next_direction = new_dir


def draw_apple(x, y):
    """Draw apple (red apple emoji)"""
    center_x = x * CELL_SIZE + CELL_SIZE // 2
    center_y = y * CELL_SIZE + CELL_SIZE // 2
    canvas.create_text(
        center_x, center_y,
        text="🍎",
        font=("Arial", CELL_SIZE - 4)
    )

def draw_snake_head(x, y, direction):
    """Draw snake head (green with direction)"""
    x1 = x * CELL_SIZE + 2
    y1 = y * CELL_SIZE + 2
    x2 = (x + 1) * CELL_SIZE - 2
    y2 = (y + 1) * CELL_SIZE - 2
    
    # Draw green rounded head
    canvas.create_oval(
        x1, y1, x2, y2,
        fill="#2ecc71",  # Green
        outline="#27ae60",
        width=2
    )
    
    # Draw eyes based on direction
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    eye_size = 3
    
    if direction == (1, 0):  # Right
        eye_x1, eye_x2 = center_x + 3, center_x + 3
        eye_y1, eye_y2 = center_y - 2, center_y + 2
    elif direction == (-1, 0):  # Left
        eye_x1, eye_x2 = center_x - 3, center_x - 3
        eye_y1, eye_y2 = center_y - 2, center_y + 2
    elif direction == (0, -1):  # Up
        eye_x1, eye_x2 = center_x - 2, center_x + 2
        eye_y1, eye_y2 = center_y - 3, center_y - 3
    else:  # Down
        eye_x1, eye_x2 = center_x - 2, center_x + 2
        eye_y1, eye_y2 = center_y + 3, center_y + 3
    
    canvas.create_oval(eye_x1 - eye_size, eye_y1 - eye_size, eye_x1 + eye_size, eye_y1 + eye_size, fill="black")
    canvas.create_oval(eye_x2 - eye_size, eye_y2 - eye_size, eye_x2 + eye_size, eye_y2 + eye_size, fill="black")

def draw_snake_body(x, y):
    """Draw snake body (green rounded rectangle)"""
    x1 = x * CELL_SIZE + 2
    y1 = y * CELL_SIZE + 2
    x2 = (x + 1) * CELL_SIZE - 2
    y2 = (y + 1) * CELL_SIZE - 2
    
    canvas.create_oval(
        x1, y1, x2, y2,
        fill="#27ae60",  # Darker green
        outline="#229954",
        width=2
    )

def draw_snake_tail(x, y):
    """Draw snake tail (smaller green circle)"""
    x1 = x * CELL_SIZE + 4
    y1 = y * CELL_SIZE + 4
    x2 = (x + 1) * CELL_SIZE - 4
    y2 = (y + 1) * CELL_SIZE - 4
    
    canvas.create_oval(
        x1, y1, x2, y2,
        fill="#229954",  # Darkest green
        outline="#1e8449",
        width=2
    )


def draw_grid():
    """Draw grid lines"""
    for i in range(GRID_SIZE + 1):
        x = i * CELL_SIZE
        canvas.create_line(
            x, 0, x, GRID_SIZE * CELL_SIZE,
            fill="#2c3e50", width=1
        )
        y = i * CELL_SIZE
        canvas.create_line(
            0, y, GRID_SIZE * CELL_SIZE, y,
            fill="#2c3e50", width=1
        )


def draw_game():
    """Draw game screen"""
    global canvas, snake, food_pos, score, game_over, direction
    
    canvas.delete("all")
    
    # Draw grid
    draw_grid()
    
    # Draw apple (red apple emoji)
    if food_pos:
        draw_apple(food_pos[0], food_pos[1])
    
    # Draw snake (green with head, body, tail)
    for i, pos in enumerate(snake):
        if i == 0:
            # Snake head (green with eyes)
            draw_snake_head(pos[0], pos[1], direction)
        elif i == len(snake) - 1:
            # Snake tail (smaller green circle)
            draw_snake_tail(pos[0], pos[1])
        else:
            # Snake body (green circles)
            draw_snake_body(pos[0], pos[1])
    
    # Update score display
    score_label.config(text=f"Score: {score}")
    
    # Game over message
    if game_over:
        canvas.create_text(
            GRID_SIZE * CELL_SIZE // 2,
            GRID_SIZE * CELL_SIZE // 2 - 20,
            text="Game Over!",
            font=("Arial", 24, "bold"),
            fill="#e74c3c"
        )
        canvas.create_text(
            GRID_SIZE * CELL_SIZE // 2,
            GRID_SIZE * CELL_SIZE // 2 + 20,
            text=f"Final Score: {score}",
            font=("Arial", 16),
            fill="#ecf0f1"
        )


def game_loop():
    """Main game loop"""
    global current_speed
    move_snake()
    draw_game()
    
    if not game_over:
        root.after(current_speed, game_loop)  # Use dynamic speed
    else:
        messagebox.showinfo(
            "Game Over",
            f"Game Over!\nFinal Score: {score}\n\nClick 'Restart' to start a new game"
        )


def on_key_press(event):
    """Handle keyboard input"""
    global paused
    
    key = event.keysym.lower()
    
    key_mapping = {
        'up': DIRECTIONS['up'],
        'w': DIRECTIONS['up'],
        'down': DIRECTIONS['down'],
        's': DIRECTIONS['down'],
        'left': DIRECTIONS['left'],
        'a': DIRECTIONS['left'],
        'right': DIRECTIONS['right'],
        'd': DIRECTIONS['right']
    }
    
    if key in key_mapping:
        change_direction(key_mapping[key])
    elif key == 'space':
        toggle_pause()


def restart_game():
    """Restart game"""
    global paused
    init_game()
    paused = False
    draw_game()
    game_loop()


def toggle_pause():
    """Toggle pause/resume"""
    global paused
    if not game_over:
        paused = not paused
        if not paused:
            game_loop()


def create_gui():
    """Create GUI interface"""
    global root, canvas, score_label
    
    root = tk.Tk()
    root.title("Snake Game - Functional Version")
    root.geometry("600x700")
    root.resizable(False, False)
    
    # Bind keyboard events
    root.bind("<KeyPress>", on_key_press)
    root.focus_set()
    
    # Title and score
    header_frame = tk.Frame(root, bg="#2c3e50", height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(
        header_frame,
        text="🐍 Snake Game (Functional)",
        font=("Arial", 24, "bold"),
        bg="#2c3e50",
        fg="white"
    )
    title_label.pack(pady=(2, 2))
    
    score_label = tk.Label(
        header_frame,
        text="Score: 0",
        font=("Arial", 14),
        bg="#2c3e50",
        fg="#ecf0f1"
    )
    score_label.pack()
    
    # Game canvas
    canvas_width = GRID_SIZE * CELL_SIZE
    canvas_height = GRID_SIZE * CELL_SIZE
    
    canvas = tk.Canvas(
        root,
        width=canvas_width,
        height=canvas_height,
        bg="#34495e",
        highlightthickness=2,
        highlightbackground="#2c3e50"
    )
    canvas.pack(pady=20)
    
    # Control buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    restart_btn = tk.Button(
        button_frame,
        text="Restart",
        command=restart_game,
        font=("Arial", 12, "bold"),
        bg="#ecf0f1",  # Light gray background
        fg="#2c3e50",  # Dark text for better visibility
        width=12,
        height=2,
        cursor="hand2",
        relief=tk.RAISED,
        bd=2
    )
    restart_btn.pack(side=tk.LEFT, padx=5)
    
    pause_btn = tk.Button(
        button_frame,
        text="Pause/Resume",
        command=toggle_pause,
        font=("Arial", 12, "bold"),
        bg="#ecf0f1",  # Light gray background
        fg="#2c3e50",  # Dark text for better visibility
        width=12,
        height=2,
        cursor="hand2",
        relief=tk.RAISED,
        bd=2
    )
    pause_btn.pack(side=tk.LEFT, padx=5)
    
    # Instructions
    info_label = tk.Label(
        root,
        text="Use arrow keys or WASD to control the snake",
        font=("Arial", 10),
        fg="#7f8c8d"
    )
    info_label.pack(pady=5)
    
    return root


def main():
    """Main function"""
    global root
    
    root = create_gui()
    init_game()
    draw_game()
    game_loop()
    root.mainloop()


if __name__ == "__main__":
    main()
