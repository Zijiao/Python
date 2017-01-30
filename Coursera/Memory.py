# implementation of card game - Memory

import simplegui
import random

# helper function to initialize globals
def new_game():
    global deck,exposed
    deck=range(0,8)+range(0,8) 
    random.shuffle(deck)
    

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    pass
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(0,16):
        canvas.draw_text(str(deck[i]),[50*i+10,65],50,'White')


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()