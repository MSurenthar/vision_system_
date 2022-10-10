import RPi.GPIO as pin
import time
pin.setmode(pin.BCM)
pin.setup(21,pin.OUT)
pin.setup(20,pin.IN,pull_up_down=pin.PUD_DOWN)
#pin.setup(38,pin.pu)
c=0
while c<20000:
    if pin.input(20):
        print("PIN40 on",c)
        pin.output(21,pin.HIGH)
    # print(f" High .... {c}")
    # time.sleep(5)
    # print(f" Low .... {c}")
    else:
        print("PIN40 off",c)
        pin.output(21,pin.LOW)

    time.sleep(.01)
    c=c+1