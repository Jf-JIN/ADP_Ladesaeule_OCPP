
from gpiozero import LED
# from _test_Module import *
from GPIO_Parameter import *
import traceback

obj_dict = {

}
while 1:
    num: str = input("\nEnter a number: ")
    if num in ['q', 'Q']:
        break
    try:
        num = int(num)
    except ValueError:
        print("Invalid input. Try again.")
        continue
    if not 0 <= abs(num) <= 27:
        print("Number out of range. Try again.")
        continue
    print("You entered:", num)
    abs_num = abs(num)
    if abs_num not in obj_dict:
        obj_dict[abs_num] = LED(abs_num)
    a: LED = obj_dict[abs_num]
    print(a, type(a))
    try:
        if num < 0:
            a.off()
        else:
            a.on()
    except:
        print(traceback.format_exc())
