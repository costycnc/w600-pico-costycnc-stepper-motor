# main.py -- put your code here!
from machine import Pin,PWM
import usocket as socket

led = Pin(Pin.PB_12, Pin.OUT, Pin.PULL_FLOATING)#enable/disable 
#led1 = Pin(Pin.PB_11, Pin.OUT, Pin.PULL_FLOATING)
led2 = Pin(Pin.PB_10, Pin.OUT, Pin.PULL_FLOATING)#direction

pwm2 = PWM(Pin(Pin.PB_18))#pulse pin PB18
pwm2.freq()
pwm2.freq(4000)
pwm2.duty()
pwm2.duty(50)

a=0

# setup the webserver
b=2
c=0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create new socket, address family type = AF_INET, socket type = SOCK_STREAM
s.bind(('', 80))
s.listen(5) # accept connections. backlog = 5 = max. number of unaccepted connections before refusing new connections



while True: 
    conn, addr = s.accept()
    request = conn.recv(2500).decode()
    #print(request)
    response="hello3 world"
    if "/b=1" in request:
        b=1
        response="b=1"
    elif "/b=0" in request:
        b=0
        response="b=0"
    else:
        b=2
        response="stop"        
    conn.send("HTTP/1.1 200 ok\n")
    conn.send("Content-type: text /html\n")		
    conn.send("Connection: close\n\n")   
    conn.sendall('<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><a href="192.168.43.1/b=0"><button>left</button></a><a href="192.168.43.1/b=1"><button>right</button></a><a href="192.168.43.1/b=2"><button>stop</button></a></body></html>')	
    conn.close()
            
    if b==1: 
       led.value(0)#enable
       led2.value(0)#direction
    elif b==0:        
       led.value(0)#enable
       led2.value(1)#direction
    else:
       led.value(1)#disable
    
