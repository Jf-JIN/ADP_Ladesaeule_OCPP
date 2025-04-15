

from gpiozero import LED


a = LED(25)
a.blink()
print("Button pressed")
