# main.py -- put your code here!
# costycnc gcode interpreter 1.0
import socket
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
kx=0
ky=0
ax=""
b=[]
este=0
movementx=0
movementy=0
tmpx=0
tmpy=0

def extract(a4):
    vrt=""
    for a5 in a4:    
        if  a5 in('.','0','1','2','3','4','5','6','7','8','9',"-"):
            vrt +=a5
        else:
            break
    return vrt    

def gcode_exec(strg):
    global targhetx,currentx,targhety,currenty,directionx,directiony,absolute,k,mx,my,tmpx,tmpy
    print(strg)
    este=0
    if "G90" in strg:
        absolute=1
        
    if "G91" in strg:
        absolute=0       
    mx=0
    my=0
    tmpx=0
    tmpy=0
    if ("X") in strg:
        targhetx=0
        nn=strg.split("X")
        k=int(float(extract(nn[1])))
        if absolute:
            targhetx=k             
        else:
            targhetx=currentx+k
        tmpx=1
        mx=targhetx-currentx
        if targhetx>currentx:
            directionx=1
        else:
            directionx=-1 
  
    if ("Y") in strg:
        targhety=0
        nn=strg.split("Y")
        k=int(float(extract(nn[1])))
        if absolute:
            targhety=k
        else:
            targhety=currenty+k 
        tmpy=1
        my=targhety-currenty    
        if targhety>currenty:
            directiony=1
        else:
            directiony=-1 
    print("prima targhetx=",targhetx)
    print("prima targhety=",targhety)    
    if (mx and my):
        if mx>my:            # ex: first X=0 Y=0  -> dopo X=10 Y=3
            tmpx=int(mx/my)  # 10/3=3.3 -> int(3.3)=3 -> tmpx=3
            targhetx=tmpx*my # tmpx=3 my=3 -> 3*3=9 -> targhetx=9
            #directionx is 1 or -1
            directiony=directiony*tmpx # directiony=1 tmpx=3 -> 1*3=3 -> directiony=3
            #so ... at 3 step x will make one step y
        if my>mx: 
            tmpy=int(my/mx)
            targhety=tmpy*mx
            directionx=directionx*tmpy            
    print("dopo targhetx=",targhetx)
    print("dopo targhety=",targhety)      
                      

def do_step():
    global currentx,directionx,currenty,directiony,targhetx,targhety


    if mx:
        currentx +=directionx

    if my:        
        currenty +=directiony
  
    print("currentx=",currentx," targhetx=",targhetx)
    print("currenty=",currenty," targhety=",targhety)

    
    time.sleep(.1)

while True:
    if (currentx==targhetx) and (currenty==targhety): # arrivatto in punto di destinazione
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
