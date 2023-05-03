# main.py -- put your code here!
# costycnc gcode interpreter 1.0
from machine import Pin
import socket
import time

led = Pin(Pin.PB_14, Pin.OUT, Pin.PULL_FLOATING)
led1 = Pin(Pin.PB_15, Pin.OUT, Pin.PULL_FLOATING)
led2 = Pin(Pin.PB_16, Pin.OUT, Pin.PULL_FLOATING)
led3 = Pin(Pin.PB_17, Pin.OUT, Pin.PULL_FLOATING)
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
x=[1,3,2,6,4,12,8,9]
dorme=1


def movey(pasy):
    global x
    #print((x[a] >> 0) & 1,(x[a] >> 1) & 1,(x[a] >> 2) & 1,(x[a] >> 3) & 1)
    led4.value((x[pasy] >> 0) & 1)
    led5.value((x[pasy] >> 1) & 1)
    led6.value((x[pasy] >> 2) & 1)
    led7.value((x[pasy] >> 3) & 1)

def movex(pasx):
    led.value((x[pasx] >> 0) & 1)
    led1.value((x[pasx] >> 1) & 1)
    led2.value((x[pasx] >> 2) & 1)
    led3.value((x[pasx] >> 3) & 1)


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
        #print("sx=",sx)
        movex(x0&7)
    if e2 <= dx:
        error = error + dx
        y0 = y0 + sy
        #print("sy=",sy)
        movey(y0&7)        
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
            if(x0==0)and(y0==0): #se cursore e arivatto in 0,0 e buffer ancora ha data
                if len(buffer)>0: # significa che qualche ok e scapato o almeno non mi spiego 
                    conn.send("ok\n") #perche 3-4 istruzioni a fine risulta non lette
                    
                 
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


