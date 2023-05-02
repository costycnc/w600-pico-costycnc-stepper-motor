# main.py -- put your code here!
# costycnc gcode interpreter 1.0
from machine import Pin
import socket
import time

led = Pin(Pin.PB_09, Pin.OUT, Pin.PULL_FLOATING)
led1 = Pin(Pin.PB_10, Pin.OUT, Pin.PULL_FLOATING)
led2 = Pin(Pin.PB_11, Pin.OUT, Pin.PULL_FLOATING)
led3 = Pin(Pin.PB_12, Pin.OUT, Pin.PULL_FLOATING)
led4 = Pin(Pin.PB_18, Pin.OUT, Pin.PULL_FLOATING)
led5 = Pin(Pin.PB_06, Pin.OUT, Pin.PULL_FLOATING)
led6 = Pin(Pin.PB_07, Pin.OUT, Pin.PULL_FLOATING)
led7 = Pin(Pin.PB_08, Pin.OUT, Pin.PULL_FLOATING)

s = socket.socket()
s.bind(('', 23))
s.listen(5)
conn, addr = s.accept()
conn.setblocking(False)
x0=0
y0=0
x1=0
y1=0
dx=0
dy=0
sx=0
sy=0
error=0
buffer=[]
currentx=0
absolute=0
k=0
nn=[]
este=0


def movey(pasy):
    if pasy==0:
        led4.value(1)
        led5.value(0)
        led6.value(0)
        led7.value(1)
    if pasy==1:
        led4.value(1)
        led5.value(0)
        led6.value(0)
        led7.value(0)
    if pasy==2:
        led4.value(1)
        led5.value(1)
        led6.value(0)
        led7.value(0)
    if pasy==3:
        led4.value(0)
        led5.value(1)
        led6.value(0)
        led7.value(0)
    if pasy==4:
        led4.value(0)
        led5.value(1)
        led6.value(1)
        led7.value(0)
    if pasy==5:
        led4.value(0)
        led5.value(0)
        led6.value(1)
        led7.value(0)
    if pasy==6:
        led4.value(0)
        led5.value(0)
        led6.value(1)
        led7.value(1)
    if pasy==7:
        led4.value(0)
        led5.value(0)
        led6.value(0)
        led7.value(1)


def movex(pasx):
    print(pasx)
    if pasx==0:
        led.value(1)
        led1.value(0)
        led2.value(0)
        led3.value(1)
    if pasx==1:
        led.value(1)
        led1.value(0)
        led2.value(0)
        led3.value(0)
    if pasx==2:
        led.value(1)
        led1.value(1)
        led2.value(0)
        led3.value(0)
    if pasx==3:
        led.value(0)
        led1.value(1)
        led2.value(0)
        led3.value(0)
    if pasx==4:
        led.value(0)
        led1.value(1)
        led2.value(1)
        led3.value(0)
    if pasx==5:
        led.value(0)
        led1.value(0)
        led2.value(1)
        led3.value(0)
    if pasx==6:
        led.value(0)
        led1.value(0)
        led2.value(1)
        led3.value(1)
    if pasx==7:
        led.value(0)
        led1.value(0)
        led2.value(0)
        led3.value(1)

       


def extract(a4):
    vrt=""
    for a5 in a4:    
        if  a5 in('.','0','1','2','3','4','5','6','7','8','9',"-"):
            vrt +=a5
        else:
            break
    return vrt    

def gcode_exec(strg):
    global x0,y0,x1,y1,dx,dy,sx,sy,error,absolute,este
    if "G90" in strg:
        absolute=1
        
    if "G91" in strg:
        absolute=0       
    
      
    if ("X") in strg:
        nn=strg.split("X")
        k=int(float(extract(nn[1]))*100)
        if absolute:
            x1=k             
        else:
            x1=x0+k
   
  
    if ("Y") in strg:
        targhety=0
        nn=strg.split("Y")
        k=int(float(extract(nn[1]))*100)
        if absolute:
            y1=k
        else:
            y1=y0+k 
    #print(x0," ",y0," ",x1," ",y1)
    dx = abs(x1 - x0)
    if x0<x1:
        sx=1
    else:
        sx=-1
    dy = -abs(y1 - y0)
    if y0<y1:
        sy=1
    else:
        sy=-1
    error = dx + dy           
        
       
           
    
def do_step(): 
    global currentx,x0,y0,x1,y1,sx,sy,dx,dy,error
    #print("x0=",x0," x1=",x1," y0=",y0," y1=",y1)
    e2 = 2 * error
    if e2 >= dy:
        error = error + dy
        x0 = x0 + sx
        movex((x0&4)+(x0&2)+(x0&1))
    if e2 <= dx:
        error = error + dx
        y0 = y0 + sy
        movey((y0&4)+(y0&2)+(y0&1))        
    time.sleep(.001)
    
    

while True:

    if x0 == x1 and y0 == y1: # arrivatto in punto di destinazione
        if len(buffer)>0: # daca buffer e gol atunci sare peste asta
            #print(len(buffer)," buffer prima=",buffer)
            gcode_exec(buffer.pop(0)) 
            #print(len(buffer)," buffer dopo=",buffer)
            conn.send("ok\n")
            currentx=0            
    else:
            do_step() # executa pana ajunge la destinazione

    try:       
        request = conn.recv(200).decode()         
        if "?" in request:   
            conn.send("<Idle|MPos:"+str(x0/100)+","+str(y0/100)+",0.000|FS:0,0>\r")
        elif "$$" in request:
            conn.send("ok\n")
        else: 
            if len(buffer)<10:
                b=request.split("\n")
                for a in b: 
                    if a=="": 
                        pass
                    else:                        
                        buffer.append(a)

                
    except OSError as e:
        pass                 
      
# Clean up the connection.
conn.close()
print("closed. ") 

'''
def plotLine(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    if x0<x1:
        sx=1
    else:
        sx=-1
    dy = -abs(y1 - y0)
    if y0<y1:
        sy=1
    else:
        sy=-1
    error = dx + dy
    
    while True:
        print(x0," ", y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * error
        if e2 >= dy:
            if x0 == x1:
                break
            error = error + dy
            x0 = x0 + sx
        if e2 <= dx:
            if y0 == y1:
                break
            error = error + dx
            y0 = y0 + sy
plotLine(0,-10,6,4)

'''