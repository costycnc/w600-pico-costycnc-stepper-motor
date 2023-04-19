from machine import Pin
from machine import Timer

step = Pin(Pin.PB_18, Pin.OUT, Pin.PULL_FLOATING)
direction = Pin(Pin.PA_00, Pin.OUT, Pin.PULL_FLOATING)

timer3 = Timer(3)
timer3.init(period=1, mode=Timer.PERIODIC, callback=lambda t:prt())
a=0

def prt():
    global a
    a+=1
    step.value(not step.value())
    if a>2000:
        direction.value(0)
        if a>4000:
            direction.value(1)
            a=0
        