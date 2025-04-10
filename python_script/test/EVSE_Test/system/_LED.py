from const.Const_Parameter import *
import json
import os


class LED:
    def __init__(self, arg):
        if arg == 23:
            self.__key = 'latch_lock_pin'
        elif arg == 24:
            self.__key = 'latch_unlock_pin'
        self.__fp = os.path.join(os.getcwd(), 'test', 'Motor.json')

    def on(self):
        with open(self.__fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[self.__key] = 1
        with open(self.__fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def off(self):
        with open(self.__fp, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data[self.__key] = 0
        with open(self.__fp, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
