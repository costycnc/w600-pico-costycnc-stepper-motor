import easyw600
easyw600.createap(ssid="w600")
import w600
w600.run_ftpserver(port=21,username="user",password="user")
print("w600 ")

'''
from time import sleep 
import network
wlan = network.WLAN(network.STA_IF)    
wlan.active(True)                      
wlan.connect("name", "psw")#insert name and password of your router
for i in range(16):
	if wlan.isconnected():
		break
	else:
		sleep(.5)
if wlan.isconnected():
	print('Connected to', "TIM-32883215")
	import w600
	w600.run_ftpserver(port=21,username="user",password="12345678")
	sleep(1)
	print('URL:', wlan.ifconfig()[0]+':21', 'username: "user", password:"user"')
	print(wlan.ifconfig()[0])
import gc
gc.collect()
gc.mem_free()
'''
