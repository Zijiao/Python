
import simplegui

# define global variables
tenths_of_seconds=0
time_of_stops=0
correct_stops=0
stop_checker=True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = t/600
    A_remainder = t%600
    B = A_remainder/100
    B_remainder = A_remainder%100
    C = B_remainder/10
    C_remainder = B_remainder%10
    D = C_remainder
    return str(A)+':'+str(B)+str(C)+'.'+str(D)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button_handler():
    global stop_checker
    stop_checker=True
    timer.start()
    
def stop_button_handler():
    timer.stop()
    global time_of_stops, correct_stops,tenths_of_seconds,stop_checker        
    if stop_checker:
        t=tenths_of_seconds
        A = t/600
        A_remainder = t%600
        B = A_remainder/100
        B_remainder = A_remainder%100
        C = B_remainder/10
        C_remainder = B_remainder%10
        D = C_remainder
        time_of_stops=time_of_stops+1
        if D==0:
            correct_stops=correct_stops+1
        stop_checker=False
    
def reset_button_handler():
    timer.stop()
    global tenths_of_seconds,time_of_stops,correct_stops,stop_checker
    tenths_of_seconds=0
    time_of_stops=0
    correct_stops=0
    stop_checker=True


# define event handler for timer with 0.1 sec interval
def timer_handler():
    global tenths_of_seconds
    tenths_of_seconds=tenths_of_seconds+1
    print tenths_of_seconds

# define draw handler
def draw_handler(canvas):
    global tenths_of_seconds
    canvas.draw_text("Stopwatch game", (5, 20), 18, 'Gray')
    canvas.draw_text(format(tenths_of_seconds), (80, 100), 20, 'Red')
    canvas.draw_text(str(correct_stops)+'/'+str(time_of_stops), (170, 20), 16, 'Yellow')
    
# create frame
frame=simplegui.create_frame("Stopwatch",200,200)

# register event handlers
frame.set_draw_handler(draw_handler)
start_botton = frame.add_button('Start',start_button_handler,100)
stop_botton = frame.add_button('Stop',stop_button_handler,100)
reset_botton = frame.add_button('Reset',reset_button_handler,100)

timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()