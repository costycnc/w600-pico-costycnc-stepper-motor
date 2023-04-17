from machine import Pin
from machine import Timer

led = Pin(Pin.PA_00, Pin.OUT, Pin.PULL_FLOATING)

timer3 = Timer(3)
timer3.init(period=1000, mode=Timer.PERIODIC, callback=lambda t:prt())

def prt():
    led.value(not led.value())
