# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

paddle_speed=8
ball_vel=[0,0]
paddle1_pos=[4,200]
paddle2_pos=[596,200]

paddle1_vel=0
paddle2_vel=0

score1=0
score2=0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos=[WIDTH/2,HEIGHT/2]
    ball_vel[1]=-random.randrange(60,180)/60
    if direction:
        ball_vel[0]=random.randrange(120,240)/60
    else:
        ball_vel[0]=-random.randrange(120,240)/60

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,score2,score1  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos=[4,200]
    paddle2_pos=[596,200]
    score2=0
    score1=0
    temp=random.randrange(0,2)
    spawn_ball(temp==0) # 


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,paddle1_vel,paddle2_vel
    # update ball positions
    ball_pos[0]+=ball_vel[0]
    ball_pos[1]+=ball_vel[1]
    
    # collide and reflect of verticle sides of canvas
    if ball_pos[1]<=BALL_RADIUS: # top
        ball_vel[1]=-ball_vel[1]
    elif ball_pos[1]>=HEIGHT-BALL_RADIUS-1: # bottom
        ball_vel[1]=-ball_vel[1]
        
    # collide and reflect with horizontal sides of gutters
    if ball_pos[0]<=BALL_RADIUS+PAD_WIDTH:# left
        if ball_pos[1]>=paddle1_pos[1]-HALF_PAD_HEIGHT-1 and ball_pos[1]<=paddle1_pos[1]+HALF_PAD_HEIGHT+1:
            ball_vel[0]= ball_vel[0]*1.1
            ball_vel[1]= ball_vel[1]*1.1
            ball_vel[0]=-ball_vel[0]
        else:
            score2+=1
            spawn_ball(RIGHT)
    elif ball_pos[0]>=WIDTH-BALL_RADIUS-PAD_WIDTH-1: # right
        if ball_pos[1]>=paddle2_pos[1]-HALF_PAD_HEIGHT-1 and ball_pos[1]<=paddle2_pos[1]+HALF_PAD_HEIGHT+1:
            ball_vel[0]= ball_vel[0]*1.1
            ball_vel[1]= ball_vel[1]*1.1
            ball_vel[0]=-ball_vel[0]
        else:
            score1+=1
            spawn_ball(LEFT)
            
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
            
    # draw ball
    canvas.draw_circle(ball_pos,BALL_RADIUS,2,"Red","White")
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1]>=HALF_PAD_HEIGHT and paddle1_pos[1]<=HEIGHT-HALF_PAD_HEIGHT: 
        paddle1_pos[1]+=paddle1_vel
    elif paddle1_pos[1]<HALF_PAD_HEIGHT:
        paddle1_pos[1]=HALF_PAD_HEIGHT
        paddle1_vel=0
    elif paddle1_pos[1]>HEIGHT-HALF_PAD_HEIGHT:
        paddle1_pos[1]=HEIGHT-HALF_PAD_HEIGHT
        paddle1_vel=0        
        
    if paddle2_pos[1]>=HALF_PAD_HEIGHT and paddle2_pos[1]<=HEIGHT-HALF_PAD_HEIGHT: 
        paddle2_pos[1]+=paddle2_vel
    elif paddle2_pos[1]<HALF_PAD_HEIGHT:
        paddle2_pos[1]=HALF_PAD_HEIGHT
        paddle2_vel=0
    elif paddle2_pos[1]>HEIGHT-HALF_PAD_HEIGHT:
        paddle2_pos[1]=HEIGHT-HALF_PAD_HEIGHT
        paddle2_vel=0  
    
    # draw paddles
    canvas.draw_polygon([[paddle1_pos[0], paddle1_pos[1]+HALF_PAD_HEIGHT ],[paddle1_pos[0], paddle1_pos[1]-HALF_PAD_HEIGHT ]], PAD_WIDTH, 'White')
    canvas.draw_polygon([[paddle2_pos[0], paddle2_pos[1]+HALF_PAD_HEIGHT ],[paddle2_pos[0], paddle2_pos[1]-HALF_PAD_HEIGHT ]], PAD_WIDTH, 'White')
    
    # draw scores
    canvas.draw_text(str(score1),[230,60],40,"White")
    canvas.draw_text(str(score2),[350,60],40,"White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel=-paddle_speed
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel=paddle_speed
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel=-paddle_speed
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel=paddle_speed   
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel=0
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel=0
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel=0
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel=0 
        
def button_handler():
    new_game()
        
# create frame
frame = simplegui.create_frame("Pong: The Most Stupid Game Ever", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart',button_handler,200)


# start frame
new_game()
frame.start()