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
absolute=1
kx=0
ky=0
dx=0
dy=0
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
    global targhetx,currentx,targhety,currenty,directionx,directiony,absolute,k,mx,my,tmpx,tmpy,dx,dy
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
        my=targhety-currenty          
        if targhety>currenty:
            directiony=1
        else:
            directiony=-1
    #print("---------------------------------------------------")        
    #print("prima currentx=",currentx," currenty=",currenty) 
    #print(strg)    
    #print(" prima mx=",mx," my=",my," dirx=",directionx," diry=",directiony)            
    if (mx and my):
        dx=directionx
        dy=directiony
        if abs(mx)>abs(my):                      
            directionx=dx*int(mx/my) 
            targhetx=currentx+(abs(my)*directionx)
        if abs(my)>abs(mx):                      
            directiony=dy*int(my/mx) 
            targhety=currenty+(abs(mx)*directiony)      
    #print("dupa tx=",targhetx,"ty=",targhety,"dix=",directionx," diy=",directiony)        
    
def do_step():
    global currentx,directionx,currenty,directiony,targhetx,targhety


    if mx:
        currentx +=directionx

    if my:        
        currenty +=directiony
  
    #print("dirx=",directionx," diry=",directiony)
    #print("x=",currentx," to ",targhetx," y=",currenty," to ",targhety)  
    time.sleep(.001)

while True:
    if (currentx==targhetx) and (currenty==targhety): # arrivatto in punto di destinazione
        if len(buffer)>0: # daca buffer e gol atunci sare peste asta
            #print(len(buffer)," buffer prima=",buffer)
            gcode_exec(buffer.pop(0)) 
            #print(len(buffer)," buffer dopo=",buffer)
            conn.send("ok\n")   
    else:
            do_step() # executa pana ajunge la destinazione
    try:       
        request = conn.recv(200).decode()         
        if "?" in request:   
            conn.send("<Idle|MPos:"+str(currentx)+","+str(currenty)+",0.000|FS:0,0>\r")
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
