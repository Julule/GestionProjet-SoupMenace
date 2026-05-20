from random import randint
from pgzero.actor import Actor
import pgzrun

# ---------------- GAME SETTINGS ----------------

WIDTH = 800
HEIGHT = 600

GROUND = 464
GRAVITY = 200

NUMBER_OF_BACKGROUND = 2
GAME_SPEED = 100

JUMP_HEIGHT = 300

# Knife movement
KNIFE_UP_DOWN_SPEED = 120
KNIFE_MIN_HEIGHT = 20
KNIFE_MAX_HEIGHT = 300

KNIFE_APPARTION = (5, 9)
BOX_APPARTION = (2, 5)

next_knife_time = randint(KNIFE_APPARTION[0], KNIFE_APPARTION[1])
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

knifes = []
boxes = []

# ---------------- HERO ----------------

hero = Actor("leek1", anchor=("middle", "bottom"))
hero.pos = (64, GROUND)
hero_speed = 0

hero_images = ["leek1", "leek2", "leek3"]
hero_image_index = 0


def animate_hero():
    global hero_image_index

    hero_image_index += 1

    if hero_image_index >= len(hero_images):
        hero_image_index = 0

    hero.image = hero_images[hero_image_index]


clock.schedule_interval(animate_hero, 0.2)

# ---------------- CAT ----------------

cat = Actor("cat1", anchor=("middle", "bottom"))
cat.pos = (-200, 365)

cat_images = ["cat1", "cat2", "cat3", "cat4", "cat5"]
cat_image_index = 0


def animate_cat():
    global cat_image_index

    cat_image_index += 1

    if cat_image_index >= len(cat_images):
        cat_image_index = 0

    cat.image = cat_images[cat_image_index]


clock.schedule_interval(animate_cat, 0.5)

# ---------------- LIFE AND SCORE ----------------

heart = Actor("heart")

live = 3
score = 0
win_score = 10

game_over = False
game_win = False

# ---------------- BACKGROUND ----------------

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):
    bg_b = Actor("table", anchor=("left", "top"))
    bg_b.pos = (n * WIDTH, 0)
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("kitchen_background", anchor=("left", "top"))
    bg_t.pos = (n * WIDTH, 0)
    backgrounds_top.append(bg_t)


# ---------------- DRAW ----------------

def draw():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    cat.draw()

    for box in boxes:
        box.draw()

    for knife in knifes:
        knife.draw()

    hero.draw()

    # Draw lives
    for i in range(live):
        heart.pos = (WIDTH - 30 - i * 35, 30)
        heart.draw()

    # Draw score
    screen.draw.text(
        "Score: " + str(score),
        (10, 10),
        color="white",
        fontsize=30
    )

    if game_over:
        screen.draw.text(
            "GAME OVER",
            center=(WIDTH // 2, HEIGHT // 2),
            color="red",
            fontsize=70
        )

    if game_win:
        screen.draw.text(
            "YOU WIN!",
            center=(WIDTH // 2, HEIGHT // 2),
            color="yellow",
            fontsize=70
        )


# ---------------- UPDATE ----------------

def update(dt):
    global next_box_time
    global next_knife_time
    global hero_speed
    global live
    global score
    global game_over
    global game_win

    if game_over or game_win:
        return

    # ---------------- CAT MOVEMENT ----------------

    x, y = cat.pos
    x += GAME_SPEED / 8 * dt

    if x > WIDTH + 100:
        x = -200

    cat.pos = (x, y)

    # ---------------- SPAWN KNIFE ----------------

    next_knife_time -= dt

    if next_knife_time <= 0:
        knife = Actor("knife", anchor=("left", "bottom"))
        knife.pos = (WIDTH, GROUND)

        knife.direction = -1
        knife.jump_height = randint(KNIFE_MIN_HEIGHT, KNIFE_MAX_HEIGHT)

        knifes.append(knife)

        next_knife_time = randint(KNIFE_APPARTION[0], KNIFE_APPARTION[1])

    # ---------------- UPDATE KNIVES ----------------

    for knife in knifes[:]:
        x, y = knife.pos

        x -= GAME_SPEED * dt
        y += knife.direction * KNIFE_UP_DOWN_SPEED * dt

        if y <= GROUND - knife.jump_height:
            y = GROUND - knife.jump_height
            knife.direction = 1

        if y >= GROUND:
            y = GROUND
            knife.direction = -1

        knife.pos = (x, y)

        # Knife touches leek: life -1
        if knife.colliderect(hero):
            live -= 1
            knifes.remove(knife)

            if live <= 0:
                game_over = True
 
         # Knife passes leek / goes off screen: score +1
        elif knife.x <= -50:
            knifes.remove(knife)
            score += 1

    # ---------------- SPAWN BOX ----------------

    next_box_time -= dt

    if next_box_time <= 0:
        box = Actor("box", anchor=("left", "bottom"))
        box.pos = (WIDTH, GROUND)

        boxes.append(box)

        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

    # ---------------- UPDATE BOXES ----------------

    for box in boxes[:]:
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = (x, y)

        if box.colliderect(hero):
            score += 1
            boxes.remove(box)

        elif box.x <= -50:
            boxes.remove(box)
        

    # ---------------- WIN CHECK ----------------

    if score >= win_score:
        game_win = True

    # ---------------- HERO GRAVITY ----------------

    hero_speed -= GRAVITY * dt

    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0

    hero.pos = (x, y)

    # ---------------- BACKGROUND BOTTOM ----------------

    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= GAME_SPEED * dt
        bg.pos = (x, y)

    if backgrounds_bottom[0].x <= -WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = ((NUMBER_OF_BACKGROUND - 1) * WIDTH, 0)
        backgrounds_bottom.append(bg)

    # ---------------- BACKGROUND TOP ----------------

    for bg in backgrounds_top:
        x, y = bg.pos
        x -= GAME_SPEED / 3 * dt
        bg.pos = (x, y)

    if backgrounds_top[0].x <= -WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = ((NUMBER_OF_BACKGROUND - 1) * WIDTH, 0)
        backgrounds_top.append(bg)


# ---------------- KEYBOARD ----------------

def on_key_down(key):
    global hero_speed

    if key == keys.SPACE and hero.y >= GROUND:
        hero_speed = JUMP_HEIGHT


pgzrun.go()