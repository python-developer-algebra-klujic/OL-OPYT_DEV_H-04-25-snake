import customtkinter as ctk
import random

# ---------------------------
# POSTAVKE IGRE
# ---------------------------
GRID = 40          # 40x40 polja
CELL = 20          # veličina polja u pikselima
W = GRID * CELL
H = GRID * CELL

START_DELAY = 200  # ms
SPEED_EVERY = 3    # ubrzaj svakih N bodova
SPEED_STEP = 15    # ms manje
MIN_DELAY = 60     # minimalni delay

# ---------------------------
# GLOBALNE VARIJABLE (MODEL)
# ---------------------------
snake = [(10, 10), (9, 10), (8, 10)]  # grid koordinate (x, y)
direction = "Right"                   # "Up", "Down", "Left", "Right"
food = (5, 5)
score = 0
delay = START_DELAY
game_over = False

# UI global
root = None
canvas = None
score_label = None


# ---------------------------
# POMOĆNE FUNKCIJE (LOGIKA)
# ---------------------------
def spawn_food():
    """Postavi food na slučajnu poziciju koja nije na zmiji."""
    global food
    while True:
        pos = (random.randint(0, GRID - 1), random.randint(0, GRID - 1))
        if pos not in snake:
            food = pos
            return


def change_direction(new_dir):
    """Promijeni smjer, ali zabrani okret 180°."""
    global direction

    if new_dir == "Up" and direction != "Down":
        direction = "Up"
    elif new_dir == "Down" and direction != "Up":
        direction = "Down"
    elif new_dir == "Left" and direction != "Right":
        direction = "Left"
    elif new_dir == "Right" and direction != "Left":
        direction = "Right"


def move_snake():
    """
    Kretanje Snake-a:
    1) izračunaj novu glavu
    2) insert(0, new_head)
    3) ako je pojela food -> raste (ne pop)
       inače -> pop (makni rep)
    """
    global score, delay, game_over

    head_x, head_y = snake[0]

    if direction == "Up":
        new_head = (head_x, head_y - 1)
    elif direction == "Down":
        new_head = (head_x, head_y + 1)
    elif direction == "Left":
        new_head = (head_x - 1, head_y)
    else:  # Right
        new_head = (head_x + 1, head_y)

    # sudar sa zidom
    if new_head[0] < 0 or new_head[0] >= GRID or new_head[1] < 0 or new_head[1] >= GRID:
        game_over = True
        return

    # sudar sa sobom
    if new_head in snake:
        game_over = True
        return

    # dodaj glavu
    snake.insert(0, new_head)

    # hrana
    if new_head == food:
        score += 1
        spawn_food()

        # ubrzavanje svakih N bodova
        if score % SPEED_EVERY == 0:
            delay = max(MIN_DELAY, delay - SPEED_STEP)
    else:
        snake.pop()


def draw():
    """Nacrtaj sve na canvas (zmija + hrana + grid opcionalno)."""
    canvas.delete("all")

    # hrana (crvena)
    fx, fy = food
    canvas.create_oval(
        fx * CELL, fy * CELL,
        fx * CELL + CELL, fy * CELL + CELL,
        fill="red", outline=""
    )

    # zmija
    for i, (x, y) in enumerate(snake):
        color = "white" if i == 0 else "green"
        canvas.create_rectangle(
            x * CELL, y * CELL,
            x * CELL + CELL, y * CELL + CELL,
            fill=color, outline=""
        )

    # ako je game over, nacrtaj tekst preko
    if game_over:
        canvas.create_text(
            W // 2, H // 2,
            text="GAME OVER",
            fill="white",
            font=("Arial", 26, "bold")
        )
        canvas.create_text(
            W // 2, H // 2 + 30,
            text="Press R to restart",
            fill="white",
            font=("Arial", 14)
        )


def update_score_ui():
    """Osvježi score (i brzinu) desno u panelu."""
    score_label.configure(text=f"Score: {score}\nDelay: {delay} ms")


def restart_game():
    """Reset svih globalnih varijabli igre."""
    global snake, direction, score, delay, game_over
    snake = [(10, 10), (9, 10), (8, 10)]
    direction = "Right"
    score = 0
    delay = START_DELAY
    game_over = False
    spawn_food()
    update_score_ui()
    draw()


def loop():
    """Game loop preko after()."""
    if not game_over:
        move_snake()
        update_score_ui()
    draw()

    # nastavljamo tickati i kad je game_over (da se tekst vidi),
    # ali ne mičemo zmiju jer game_over blokira move_snake
    root.after(delay, loop)


# ---------------------------
# EVENTI TIPKOVNICE
# ---------------------------
def on_key(event):
    # event.keysym će biti: Up, Down, Left, Right, r, R...
    key = event.keysym

    if key == "Up":
        change_direction("Up")
    elif key == "Down":
        change_direction("Down")
    elif key == "Left":
        change_direction("Left")
    elif key == "Right":
        change_direction("Right")
    elif key in ("r", "R"):
        restart_game()


# ---------------------------
# UI (CustomTkinter)
# ---------------------------
def build_ui():
    global root, canvas, score_label

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Snake - CustomTkinter (bez klasa)")
    root.geometry("740x460")

    # GLAVNI LAYOUT: lijevo igra, desno panel
    main = ctk.CTkFrame(root)
    main.pack(fill="both", expand=True, padx=12, pady=12)

    main.grid_columnconfigure(0, weight=1)
    main.grid_columnconfigure(1, weight=0)
    main.grid_rowconfigure(0, weight=1)

    # LIJEVO: canvas (igra)
    left = ctk.CTkFrame(main)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

    canvas = ctk.CTkCanvas(left, width=W, height=H, bg="black", highlightthickness=0)
    canvas.pack(padx=12, pady=12)

    # DESNO: info + tipke
    right = ctk.CTkFrame(main, width=220)
    right.grid(row=0, column=1, sticky="ns")

    title = ctk.CTkLabel(right, text="SNAKE", font=("Arial", 26, "bold"))
    title.pack(pady=(18, 6))

    score_label = ctk.CTkLabel(right, text="Score: 0\nDelay: 200 ms", font=("Arial", 16))
    score_label.pack(pady=(0, 18))

    # Tipke kao "d-pad"
    pad = ctk.CTkFrame(right)
    pad.pack(pady=10)

    pad.grid_columnconfigure(0, weight=1)
    pad.grid_columnconfigure(1, weight=1)
    pad.grid_columnconfigure(2, weight=1)

    def btn(text, r, c, cmd):
        b = ctk.CTkButton(pad, text=text, width=60, height=44, command=cmd)
        b.grid(row=r, column=c, padx=6, pady=6)
        return b

    btn("↑", 0, 1, lambda: change_direction("Up"))
    btn("←", 1, 0, lambda: change_direction("Left"))
    btn("→", 1, 2, lambda: change_direction("Right"))
    btn("↓", 1, 1, lambda: change_direction("Down"))

    # dodatne kontrole
    ctk.CTkButton(right, text="Restart (R)", command=restart_game).pack(pady=(18, 6))
    ctk.CTkLabel(right, text="Tipkovnica: strelice\nRestart: R", font=("Arial", 12)).pack(pady=(6, 0))

    # Tipkovnica radi samo ako prozor ima fokus
    root.bind("<Key>", on_key)
    root.focus_set()


# ---------------------------
# START
# ---------------------------
build_ui()
spawn_food()
update_score_ui()
draw()
loop()
root.mainloop()
