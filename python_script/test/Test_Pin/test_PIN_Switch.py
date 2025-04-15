

from gpiozero import Button


a = Button(21)
a.wait_for_press()
print("Button pressed")
