from tkinter import *
import random

# Game Constants
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100  # Initial speed
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#32CD32"
FOOD_COLOR = "#FF4500"
BACKGROUND_COLORS = ["#0f0c29", "#302b63", "#24243e"]  # Gradient effect
FONT = ("Arial", 20, "bold")

is_paused = False  # Game pause state


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([100 - (i * SPACE_SIZE), 100])

        for x, y in self.coordinates:
            square = canvas.create_oval(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


def next_turn():
    global direction, SPEED, is_paused

    if is_paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_oval(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        SPEED = max(50, SPEED - 3)  # Increase speed (min cap at 50)
        label.config(text=f"Score: {score}")

        canvas.delete("food")
        food.__init__()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = "left"
    elif new_direction == "right" and direction != "left":
        direction = "right"
    elif new_direction == "up" and direction != "down":
        direction = "up"
    elif new_direction == "down" and direction != "up":
        direction = "down"


def toggle_pause(event=None):
    global is_paused

    if is_paused:
        is_paused = False
        next_turn()
    else:
        is_paused = True


def check_collisions():
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 40,
        font=("Arial", 50, "bold"),
        text="GAME OVER",
        fill="red",
        tag="gameover",
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 20,
        font=FONT,
        text=f"Final Score: {score}",
        fill="white",
        tag="gameover",
    )

    restart_button.place(x=GAME_WIDTH / 2 - 50, y=GAME_HEIGHT / 2 + 80)


def restart_game():
    global snake, food, score, direction, SPEED, is_paused

    canvas.delete("all")
    
    score = 0
    SPEED = 100
    direction = "down"
    label.config(text="Score: 0")
    is_paused = False

    snake = Snake()
    food = Food()

    restart_button.place_forget()
    next_turn()


# Main application window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(
    window,
    text="Score: 0",
    font=("Arial", 20, "bold"),
    fg="white",
    bg=BACKGROUND_COLORS[0],
)
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLORS[0], height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}+100+50")

# Animated background effect
def animate_background():
    global BACKGROUND_COLORS
    new_color = BACKGROUND_COLORS.pop(0)
    BACKGROUND_COLORS.append(new_color)
    canvas.config(bg=new_color)
    window.after(5000, animate_background)

animate_background()

# Restart Button
restart_button = Button(
    window,
    text="Restart Game",
    font=FONT,
    bg="gray",
    fg="white",
    command=restart_game,
)

# Initialize game objects
snake = Snake()
food = Food()

# Key bindings for both **Arrow Keys** and **WASD**
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.bind("a", lambda event: change_direction("left"))
window.bind("d", lambda event: change_direction("right"))
window.bind("w", lambda event: change_direction("up"))
window.bind("s", lambda event: change_direction("down"))

window.bind("<p>", toggle_pause)  # Press 'P' to pause/resume

next_turn()

window.mainloop()
