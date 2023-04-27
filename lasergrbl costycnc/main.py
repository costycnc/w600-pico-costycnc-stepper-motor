# costycnc gcode interpreter 1.0
import usocket as socket
import time

s = socket.socket()
s.bind(('', 23))
s.listen(5)
conn, addr = s.accept()
conn.setblocking(False)

targhetx=0
currentx=0
directionx=0
targhety=0
currenty=0
directiony=0
buffer=[]
absolute=0
ax=""
b=[]

def extract(a4):
    vrt=""
    for a5 in a4:    
        if  a5 in('.','0','1','2','3','4','5','6','7','8','9',"-"):
            vrt +=a5
        else:
            break
    return vrt    

def gcode_exec(strg):
    global targhetx,currentx,targhety,currenty,directionx,directiony,absolute

    if "G90" in strg:
        print("absolute")
        absolute=0
        
    if "G91" in strg:
        print("incremental")
        absolute=1       

    if ("X") in strg:
        nn=strg.split("X")
        k=int(float(extract(nn[1]))) 
        print("arivatto=",k)
        if absolute:                 # incremental
            targhetx=currentx+k
            print("targhet incr=",targhet)
            if targhetx>currentx:
                directionx=1
            else:
                directionx=0                           
        else :                        #absolute
            targhet=k
            print("targhet abs=",targhet)
            if targhetx>currentx:
                directionx=1
            else:
                directionx=0          

    if ("Y") in strg:
        nn=strg.split("Y")
        k=int(float(extract(nn[1]))) 
        print("arivatto=",k)
        if absolute:                 # incremental
            targhet=current+k
            print("targhet incr=",targhet)
            if targhet>current:
                direction=1
            else:
                direction=0                           
        else :                        #absolute
            targhet=k
            print("targhet abs=",targhet)
            if targhet>current:
                direction=1
            else:
                direction=0                         

def do_step():
    global currentx,directionx,currenty,directiony
    if directionx:
        currentx +=1
    else:
        currentx -=1
    print("do_step-current",current)
    time.sleep(.1)

while True:
    if current==targhet: # arrivatto in punto di destinazione
        if len(buffer)>0: # daca buffer e gol atunci sare peste asta
            gcode_exec(buffer.pop(0)) 
            conn.send("ok\n")   
    else:
            do_step() # executa pana ajunge la destinazione
    try:       
        request = conn.recv(200).decode()         
        if "?" in request:   
            conn.send("<Idle|MPos:0.000,0.000,0.000|FS:0,0>\r")
        elif "$$" in request:
            conn.send("ok\n")
        else: 
            b=request.split("\n")
            for a in b:            
                buffer.append(a)

                
    except OSError as e:
        pass                 
      
# Clean up the connection.
conn.close()
print("closed. ") 