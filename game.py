
#from argparse import Action
from random import randint
from pgzero.actor import Actor
import pgzrun


#game bases // physics & settings - Groung & Gravity
WIDTH = 800
HEIGHT = 600
GROUND = 464 # y-position hero stand here (height 600)
GRAVITY = 200 #Pulls the hero downward after jumping

NUMBER_OF_BACKGROUND = 2  #2 bg
GAME_SPEED = 100 # speed of game movement
JUMP_SPEED = 200 #upward speed when hero jump
JUMP_HEIGHT = 350 #height of the hero's jump

#1. Hero initialisation
hero = Actor("leek1", anchor=('middle', 'bottom')) # here leek1 is starting image
hero.pos = (64, GROUND) #place hero at x = 64, y = G
hero_speed = 0 #means hero can not move vertically
hero_image = ["leek1", "leek2", "leek3"]  #these 3 image stored for animation(gif)
image_index = 0 #use this variable for hero,This keeps track of which image is currently being shown.

def animate_hero():#Defines a function that changes the hero’s image
    global image_index #Without global, Python would think image_index is a new local variable inside the function.
    image_index += 1 #each time moves to nex image frame,0 -> 1-> 2->....
    if image_index >= len(hero_image): # hero img. 3 - it will valid until image_index reset back to 0
        image_index = 0
    hero.image = hero_image[image_index] #change the hero current image

clock.schedule_interval(animate_hero, 0.2) #each 0.2 secondplay the function hero 

#2. Knife init & movement up-down 
BOX_UP_DOWN_SPEED = 120 # speed of knife up-down movement
BOX_MIN_HEIGHT = 20 # minimum height knife can go up
BOX_MAX_HEIGHT = 200 # maximum height knife can go up
BOX_APPARTION = (2, 7) # enemy boxes appear every 2 to 5 second randomly
next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])  # Chooses random starting spawn time
boxes = []
#>>>>>>> c3afb712b77265f547fb09642c37bd8225fb9298 # what is this line ?

#3. Pots init
pot = Actor("pot", anchor=('left', 'bottom'))
pot.pos = (800, 465)
pots = []

#3. Cat init 
#------------------------------------------ CAT SPRITES ------------------------------------------------

cat = Actor("cat1", anchor=('middle', 'bottom')) 
cat.pos = (-200, 365) 

cat_sprite = ["cat1", "cat2", "cat3", "cat4", "cat5"]

def animate_cat():
    global image_index
    image_index += 1
    if image_index >= len(cat_sprite):
        image_index = 0
    cat.image = cat_sprite[image_index]

clock.schedule_interval(animate_cat, 0.5) 

#------------------------------------------------------------------------------------------------------

#4. Life count
heart = Actor("heart")
live = 3 #live score variable
score = 0 # create a sore variable

# 5. background inititalisation
backgrounds_bottom = []
backgrounds_top = []
for n in range(NUMBER_OF_BACKGROUND):#run twice becz. number of bg = 2 bg
    bg_b = Actor("table", anchor=('left', 'top')) #bottom bg
    bg_b.pos = n * WIDTH, 0
    backgrounds_bottom.append(bg_b)

    bg_t = Actor("kitchen_background", anchor=('left', 'top')) # bg top
    bg_t.pos = n * WIDTH, 0
    backgrounds_top.append(bg_t)




def draw():
    screen.clear()

    for bg in backgrounds_bottom:
        bg.draw()

    for bg in backgrounds_top:
        bg.draw()

    cat.draw()

    for knife in boxes:
        knife.draw()

    for pot in pots:
        pot.draw()

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

    # knife update
    global pot, next_box_time, hero_speed, live, score
    next_pot_time = randint(1, 2)
    next_box_time -= dt #enemies update

    for i in cat:
        x, y = cat.pos
        x -= GAME_SPEED/8 * -dt
        cat.pos = x, y

    # random timing for pots
    if next_pot_time == 2:
        # add one pot to pots list
        # pot.pos = WIDTH, GROUND
        pots.append(pot)
        for pot in pots:
            x, y = pot.pos
            x += GAME_SPEED/3 * -dt
            pot.pos = x, y


    if next_box_time <= 0:
        knife = Actor("knife", anchor=('left', 'bottom'))
        knife.pos = WIDTH, GROUND
        # Enemy OX RANDOM UP-DOWN MOVEMENT
        knife.direction = -1 # -1 means knife starts going up first
        knife.jump_height = randint(BOX_MIN_HEIGHT,BOX_MAX_HEIGHT) # each knife gets different height
        boxes.append(knife)
        next_box_time = randint(BOX_APPARTION[0], BOX_APPARTION[1])


    for knife in boxes[:]: #for each knife inside this loop, box1,box2..
        x, y = knife.pos
        x -= GAME_SPEED * dt

        #Box random up-down movement, knife goes-up
        y += knife.direction * BOX_UP_DOWN_SPEED * dt #Move knife up-down

         # If knife reaches its own random top height, then move down
        if y <= GROUND - knife.jump_height:
            y = GROUND - knife.jump_height
            knife.direction = 1
       
       # If knife reaches ground again, then move up
        if y >= GROUND:
            y = GROUND
            knife.direction = -1

        knife.pos = x, y


        if knife.colliderect(hero):
            live -= 1
            boxes.remove(knife)

            if live <= 0:
                exit()
        
        elif knife.pos[0] <= -32:
            boxes.remove(knife)
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


        #if hero_speed <= 0:
         #   hero_speed = JUMP_SPEED

        #if hero_speed <= 0:
        #if hero.y == GROUND: #the single jump
        if key == keys.SPACE and hero.y >= GROUND: # the single jump
            hero_speed = JUMP_HEIGHT


pgzrun.go()