from flask import Flask,render_template,request
import threading
app = Flask(__name__)
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)

no_of_switches=50   #MENTION ACCORDING TO NEED

switches=[]

for i in range(no_of_switches):
#    GPIO.setup(i+1, GPIO.OUT)
#    GPIO.setup(25-i, GPIO.IN)
#    GPIO.output(i+1, GPIO.LOW)
    switches.append(
        {
        'pin_no_output':i+1,   #pin related to output signal of this switch (to relay)
        'pin_no_input':26 - 1 - i,  #pin related to input signal of this switch (from physical switch)
        'state':'off',  #pin state = 0
        'other_state':'on'  #pin state compliment = 1
        }   
        )


#function for state change of switches
def turn(switch,signal):
    if(signal=='on'):
        switches[switch]['state']='on'
        switches[switch]['other_state']='off'
#        GPIO.output(switches[switch]['pin_no_output'], GPIO.HIGH)
    else:
        switches[switch]['state']='off'
        switches[switch]['other_state']='on'
#        GPIO.output(switches[switch]['pin_no_output'], GPIO.LOW)


######    functionality for physical input  ###########


def physical_responce_of_switch(sw_no):
    try:
#        GPIO.add_event_detect(26-1-sw_no, GPIO.RISING,bouncetime=200)
        # refer to this link https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
        def my_callback():
            if(switches[sw_no]['state']=='on'):
                turn(sw_no,'off')
            else:
                turn(sw_no,'on')

    except Exception as e:
        print("problem in switch-",sw_no)


total_thread=[]


def physical_responce_of_all_switch(no_of_switches):
    for i in range(no_of_switches):
        
        total_thread.append(threading.Thread(target=physical_responce_of_switch, args=(i+1,)))
        total_thread[i].start()

@app.route("/")
def hello():
    return render_template('home.html',switches=switches)


@app.route("/<sw>/<action>")
def act(sw,action):
    action = str(action)
    switch_no=int(sw)-1 #for matching 1st switch to zero index
    turn(switch_no,action)
    return render_template('home.html',switches=switches)


if __name__ == "__main__":
        physical_responce_of_all_switch(no_of_switches)
        app.run( debug=True)
