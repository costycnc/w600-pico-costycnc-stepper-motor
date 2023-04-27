# costycnc gcode interpreter 1.0
import usocket as socket
import time

s = socket.socket()
s.bind(('', 23))
s.listen(5)
conn, addr = s.accept()
conn.setblocking(False)

targhet=0
current=0
buffer=[]
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
    global targhet,current
    
    if ("X") in strg:
        nn=strg.split("X")
        k=int(float(extract(nn[1])))        
        targhet=k-current
        print(targhet)

def do_step():
    current =+1
    #print(current)
    time.sleep(.1)

while True:
    if current==targhet:
        if len(buffer)>0:
            gcode_exec(buffer.pop(0))    
    else:
        do_step()
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