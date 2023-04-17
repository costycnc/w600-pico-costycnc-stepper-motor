# main.py -- put your code here!
from machine import Pin
from time import sleep
import usocket as socket
import uselect as select

led = Pin(Pin.PB_12, Pin.OUT, Pin.PULL_FLOATING)
led1 = Pin(Pin.PB_11, Pin.OUT, Pin.PULL_FLOATING)
led2 = Pin(Pin.PB_10, Pin.OUT, Pin.PULL_FLOATING)
led3 = Pin(Pin.PB_09, Pin.OUT, Pin.PULL_FLOATING)

a=0

# setup the webserver
b=2
c=0

def Client_handler(client_obj):
    global b
    #Do this when there's a socket connection 
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
    print(response)    
    conn.sendall('<html><head><meta name="viewport" content="width=device-width, initial-scale=1"></head><body><a href="192.168.43.1/b=0"><button>left</button></a><a href="192.168.43.1/b=1"><button>right</button></a><a href="192.168.43.1/b=2"><button>stop</button></a></body></html>')	
    conn.close()    

    
    

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create new socket, address family type = AF_INET, socket type = SOCK_STREAM
s.bind(('', 80))
s.listen(5) # accept connections. backlog = 5 = max. number of unaccepted connections before refusing new connections



while True:
    r, w, err = select.select((s,), (), (), .001)
    if r:
        for readable in r:
            conn, addr = s.accept()
        try:
            Client_handler(conn)
        except OSError as e:
            pass
            
    if b==1: 
        c +=1
        if c==32000:
            b=2
            c=0            
        a +=1
        if a>8:
            a=1
        if a==1:
            led.value(1) 
            led1.value(0) 
            led2.value(0) 
            led3.value(0) 
        if a==2:
            led.value(1) 
            led1.value(1) 
            led2.value(0) 
            led3.value(0) 
        if a==3:
            led.value(0) 
            led1.value(1) 
            led2.value(0) 
            led3.value(0) 
        if a==4:
            led.value(0) 
            led1.value(1) 
            led2.value(1) 
            led3.value(0)        
        if a==5:
            led.value(0) 
            led1.value(0) 
            led2.value(1) 
            led3.value(0)  
        if a==6:
            led.value(0) 
            led1.value(0) 
            led2.value(1) 
            led3.value(1)  
        if a==7:
            led.value(0) 
            led1.value(0) 
            led2.value(0) 
            led3.value(1)  
        if a==8:
            led.value(1) 
            led1.value(0) 
            led2.value(0) 
            led3.value(1)        
    elif b==0:        
        a -=1
        if a<1:
            a=8
        if a==1:
            led.value(1) 
            led1.value(0) 
            led2.value(0) 
            led3.value(0)            
        if a==2:
            led.value(1) 
            led1.value(1) 
            led2.value(0) 
            led3.value(0) 
        if a==3:
            led.value(0) 
            led1.value(1) 
            led2.value(0) 
            led3.value(0) 
        if a==4:
            led.value(0) 
            led1.value(1) 
            led2.value(1) 
            led3.value(0)        
        if a==5:
            led.value(0) 
            led1.value(0) 
            led2.value(1) 
            led3.value(0)  
        if a==6:
            led.value(0) 
            led1.value(0) 
            led2.value(1) 
            led3.value(1)  
        if a==7:
            led.value(0) 
            led1.value(0) 
            led2.value(0) 
            led3.value(1)  
        if a==8:
            led.value(1) 
            led1.value(0) 
            led2.value(0) 
            led3.value(1)  
    else:
        led.value(0) 
        led1.value(0) 
        led2.value(0) 
        led3.value(0)    

    
