# game data


#from argparse import Action
from random import randint
from pgzero.actor import Actor
import pgzrun


WIDTH = 800
HEIGHT = 600

#game phtsics & settings - Groung & Gravity
GROUND = 458 # y-position hero stand here
GRAVITY = 200 #Pulls the hero downward after jumping

NUMBER_OF_BACKGROUND = 2  #2 bg
GAME_SPEED = 100 # speed of game movement
JUMP_SPEED = 200 #upward speed when hero jump

# hero initialisation
hero = Actor("hero", anchor=('middle', 'bottom'))
hero.pos = (64, GROUND) #place hero at x = 64, y = G
hero_speed = 0 #means hero can not move vertically

#life count
heart = Actor("heart")
live = 3 #live score variable
score = 0 # create a sore variable

# enemies initialisations
BOX_APPARTION = (2, 5) # enemy boxes appear every 2 to 5 second rendomly
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])  #Chooses random starting spawn time
boxes = []

# background inititalisation

backgrounds_bottom = []
backgrounds_top = []

for n in range(NUMBER_OF_BACKGROUND):#run twice becz. number of bg = 2 bg
    bg_b = Actor("bg_1", anchor=('left', 'top')) #bottom bg
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("bg_2", anchor=('left', 'top')) # bg top
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)


def draw():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    for box in boxes:
        box.draw()

    hero.draw()

    #Life(heart)position 
    for i in range(live):
        heart.pos = (WIDTH - 30 - i*30,30)# last 30 is height consider top right (-30 is bottom right)
        heart.width = 25
        heart.height = 25
        heart.draw()
    
    ###draw score
    screen.draw.text("Score: " + str(score), (10, 10), color="white", fontsize=30)
   


def update(dt):

    # enemies update
    # box
    global next_box_time, hero_speed, live, score

    next_box_time -= dt #enemies update

    if next_box_time <= 0:
        box = Actor("box", anchor=('left', 'bottom'))
        box.pos = WIDTH, GROUND
        boxes.append(box)
        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])

    for box in boxes[:]: #for each box inside this loop, box1,box2..
        x, y = box.pos
        x -= GAME_SPEED * dt
        box.pos = x, y

        if box.colliderect(hero):
            live -= 1
            boxes.remove(box)

            if live <= 0:
                exit()
        
        elif box.pos[0] <= -32:
            boxes.remove(box)
            score += 1
  

    ### hero update
    #global hero_speed
    hero_speed -= GRAVITY * dt
    x, y = hero.pos
    y -= hero_speed * dt

    if y > GROUND:
        y = GROUND
        hero_speed = 0

    hero.pos = x, y

    # bg update
    for bg in backgrounds_bottom:
        x, y = bg.pos
        x -= GAME_SPEED * dt
        bg.pos = x, y

    if backgrounds_bottom[0].pos[0] <= - WIDTH:
        bg = backgrounds_bottom.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_bottom.append(bg)

    for bg in backgrounds_top:
        x, y = bg.pos
        x -= GAME_SPEED/3 * dt
        bg.pos = x, y

    if backgrounds_top[0].pos[0] <= - WIDTH:
        bg = backgrounds_top.pop(0)
        bg.pos = (NUMBER_OF_BACKGROUND - 1) * WIDTH, 0
        backgrounds_top.append(bg)


def on_key_down(key):
    global hero_speed

    # jump
    if key == keys.SPACE:

        if hero_speed <= 0:
            hero_speed = JUMP_SPEED

pgzrun.go()