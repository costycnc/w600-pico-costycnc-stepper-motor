from machine import Pin, PWM

#pwm1 = PWM(Pin(Pin.PB_18), channel=2, freq=1000, duty=150)
pwm2 = PWM(Pin(Pin.PB_18))
pwm2.freq()
pwm2.freq(1000)
pwm2.duty()
pwm2.duty(250)