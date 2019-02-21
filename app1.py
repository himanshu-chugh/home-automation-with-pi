from flask import Flask,render_template,request
from time import sleep 
import threading
app = Flask(__name__)
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

no_of_switches=4   #MENTION ACCORDING TO NEED

switches=[]

for i in range(no_of_switches):
    print('setuping switch ',i+1,'haveing index ',i)
    GPIO.setup(i+1, GPIO.OUT)
    GPIO.setup(27-i, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
    GPIO.output(i+1, GPIO.LOW)
    switches.append(
        {
        'pin_no_output':i+1,   #pin related to output signal of this switch (to relay)
        'pin_no_input':27 - i,  #pin related to input signal of this switch (from physical switch)
        'state':'off',  #pin state = 0
        'other_state':'on'  #pin state compliment = 1
        }   
        )


#function for state change of switches
def turn(switch_index,signal):
    if(signal=='on'):
        switches[switch_index]['state']='on'
        switches[switch_index]['other_state']='off'
        print('''
                    turning on bc 
                    
                        ''')
        GPIO.output(switches[switch_index]['pin_no_output'], 1)
    else:
        switches[switch_index]['state']='off'
        switches[switch_index]['other_state']='on'
        GPIO.output(switches[switch_index]['pin_no_output'], 0)


######    functionality for physical input  ###########

#def my_callback(sw_no):
#            print('''
#                hit happened
#                
#                ''')
#            if(switches[sw_no-1]['state']=='on'):
#                turn(sw_no-1,'off')
#                
#            else:
#                turn(sw_no-1,'on')


#def physical_responce_of_switch(sw_no):
#    def my_callback():
#            print('''
#                hit happened
#                
#                ''')
#            if(switches[sw_no-1]['state']=='on'):
#                turn(sw_no-1,'off')
#                
#            else:
#                turn(sw_no-1,'on')
#
#    try:
#        GPIO.add_event_detect(28-sw_no,callback=my_callback, GPIO.RISING,bouncetime=200)
#        print('himanshu-------------------------')
#        # refer to this link https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
#        
#
#    except Exception as e:
#        print("problem in switch-",sw_no)

def physical_responce_of_switch(sw_index):
#    try:  
#        while True:            # this will carry on until you hit CTRL+C  
#            if GPIO.input(28-sw_no): # if port 25 == 1  
#                print "Port 27 is 1/HIGH/True - LED ON"  
#                GPIO.output(sw_no, 1)         # set port/pin value to 1/HIGH/True  
#            else:  
#                print "Port 27 is 0/LOW/False - LED OFF"  
#                GPIO.output(sw_no, 0)         # set port/pin value to 0/LOW/False  
#        sleep(3)         # wait 0.1 seconds  
#  
#    finally:                   # this block will run no matter how the try block exits  
#        GPIO.cleanup()         # clean up after yourself  


    def my_callback(sw_index): 
        
        if switches[27-sw_index]['state']=='on' :
            turn(27-sw_index,'off')
        else:
            turn(27-sw_index,'on')
    
    
    GPIO.add_event_detect(27-sw_index, GPIO.RISING, callback=my_callback, bouncetime=200)
        
    
    
    
total_thread=[]


def physical_responce_of_all_switch(no_of_switches):
    for i in range(no_of_switches):
        
        total_thread.append(threading.Thread(target=physical_responce_of_switch, args=(i,)))
        total_thread[i].start()

@app.route("/")
def hello():
    return render_template('home.html',switches=switches)


@app.route("/<switch_no>/<action>")
def act(switch_no,action):
    action = str(action)
    switch_index=int(switch_no)-1 #for matching 1st switch to zero index
    turn(switch_index,action)
    return render_template('home.html',switches=switches)


if __name__ == "__main__":
    physical_responce_of_all_switch(no_of_switches)
    app.run( debug=True)
