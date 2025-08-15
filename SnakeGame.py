import turtle
import time
import random
import winsound

delay = 0.1
paused = False

# Score
score = 0
high_score = 0

# Colors
food_colors = ["red", "yellow", "blue", "orange", "purple", "pink"]
segment_colors = ["#A9A9A9", "#808080", "#696969", "#778899", "#B0C4DE"]

# Set up the screen
wn = turtle.Screen()
wn.title("Welcome to Snake Game")
wn.bgcolor("black")
wn.setup(width=620, height=620)
wn.tracer(0)

# Set background image (must be GIF and in project folder)
try:
    wn.bgpic("tenor.gif")  # Place your GIF in the project folder
except:
    wn.bgcolor("black")       # Fallback if GIF not found

# Draw border
border = turtle.Turtle()
border.hideturtle()
border.speed(0)
border.color("white")
border.pensize(4)
border.penup()
border.goto(-300, 300)
border.pendown()
for _ in range(4):
    border.forward(600)
    border.right(90)
border.penup()

# Snake head (rounded, with eyes and tongue)
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("lime")
head.penup()
head.goto(0,0)
head.direction = "stop"

# Eyes
eye1 = turtle.Turtle()
eye1.shape("circle")
eye1.color("white")
eye1.shapesize(0.3, 0.3)
eye1.penup()
eye1.hideturtle()

eye2 = turtle.Turtle()
eye2.shape("circle")
eye2.color("white")
eye2.shapesize(0.3, 0.3)
eye2.penup()
eye2.hideturtle()

# Tongue
tongue = turtle.Turtle()
tongue.hideturtle()
tongue.color("red")
tongue.pensize(2)
tongue.penup()

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color(random.choice(food_colors))
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "bold"))

# Game Over message
game_over = turtle.Turtle()
game_over.hideturtle()
game_over.color("red")
game_over.penup()
game_over.goto(0, 0)

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def pause_game():
    global paused
    paused = not paused
    if paused:
        game_over.clear()
        game_over.write("Paused", align="center", font=("Courier", 36, "bold"))
    else:
        game_over.clear()

def move():
    # Move the segments in a smooth, following manner
    if len(segments) > 0:
        for index in range(len(segments)-1, 0, -1):
            x = segments[index-1].xcor()
            y = segments[index-1].ycor()
            segments[index].goto(x, y)
        segments[0].goto(head.xcor(), head.ycor())

    # Move the head in the current direction
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

    # Draw eyes and tongue
    draw_head_details()

def draw_head_details():
    # Eyes position based on direction
    head_x, head_y = head.xcor(), head.ycor()
    eye_offset = 7
    if head.direction == "up":
        eye1.goto(head_x - eye_offset, head_y + 10)
        eye2.goto(head_x + eye_offset, head_y + 10)
        tongue.goto(head_x, head_y + 15)
        tongue.setheading(90)
    elif head.direction == "down":
        eye1.goto(head_x - eye_offset, head_y - 10)
        eye2.goto(head_x + eye_offset, head_y - 10)
        tongue.goto(head_x, head_y - 15)
        tongue.setheading(270)
    elif head.direction == "left":
        eye1.goto(head_x - 10, head_y + eye_offset)
        eye2.goto(head_x - 10, head_y - eye_offset)
        tongue.goto(head_x - 15, head_y)
        tongue.setheading(180)
    elif head.direction == "right":
        eye1.goto(head_x + 10, head_y + eye_offset)
        eye2.goto(head_x + 10, head_y - eye_offset)
        tongue.goto(head_x + 15, head_y)
        tongue.setheading(0)
    else:
        eye1.goto(head_x - eye_offset, head_y + 10)
        eye2.goto(head_x + eye_offset, head_y + 10)
        tongue.goto(head_x, head_y + 15)
        tongue.setheading(90)
    eye1.showturtle()
    eye2.showturtle()
    tongue.clear()
    tongue.pendown()
    tongue.forward(10)
    tongue.penup()

def play_sound(sound):
    try:
        winsound.PlaySound(sound, winsound.SND_ASYNC)
    except:
        pass

def add_segment():
    color_index = len(segments) % len(segment_colors)
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("circle")  # Rounded segment
    new_segment.color(segment_colors[color_index])
    new_segment.penup()
    segments.append(new_segment)

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")
wn.onkeypress(pause_game, "p")

# Main game loop
while True:
    wn.update()
    if paused:
        time.sleep(0.1)
        continue

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        play_sound("SystemHand")
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()

        # Reset the score
        score = 0
        delay = 0.1

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "bold"))
        game_over.clear()
        game_over.write("Game Over!", align="center", font=("Courier", 36, "bold"))
        time.sleep(1)
        game_over.clear()

    # Check for a collision with the food
    if head.distance(food) < 20:
        play_sound("SystemAsterisk")
        # Move the food to a random spot
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x,y)
        food.color(random.choice(food_colors))

        # Add a segment with gradient color
        add_segment()

        # Shorten the delay
        delay = max(0.05, delay - 0.001)

        # Increase the score
        score += 10
        if score > high_score:
            high_score = score

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "bold"))

    move()

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            play_sound("SystemHand")
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            # Reset the score
            score = 0
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "bold"))
            game_over.clear()
            game_over.write("Game Over!", align="center", font=("Courier", 36, "bold"))
            time.sleep(1)
            game_over.clear()

    time.sleep(delay)

wn.mainloop()