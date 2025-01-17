import threading

charging_plan = {
    'evseId': 1,
    'chargingProfile': {
        'id': 1,
        'stackLevel': 1,
        'chargingProfilePurpose': 'TxProfile',
        'chargingProfileKind': 'Absolute',
        'chargingSchedule':
            [
                {'id': 1,
                 'chargingRateUnit': 'A',
                 'chargingSchedulePeriod': [
                     {'startPeriod': 0, 'limit': 8.9},
                     {'startPeriod': 2, 'limit': 8.9},
                     {'startPeriod': 4, 'limit': 8.9},
                     {'startPeriod': 6, 'limit': 8.9},
                     {'startPeriod': 8, 'limit': 8.9},
                     {'startPeriod': 10, 'limit': 8.9},
                     {'startPeriod': 12, 'limit': 8.9},
                     {'startPeriod': 14, 'limit': 8.9},
                     {'startPeriod': 16, 'limit': 8.9}
                 ],
                 'startSchedule': '2025-01-15T15:12:20Z'}
            ]
    },
    'customData': None}
voltage_max = 220
unit = charging_plan['chargingProfile']['chargingSchedule'][0]['chargingRateUnit']
current_periode = [0, 0]
request_periode = 4

def set_current(value):
    print(value)


def get_limit_value(item: dict):
    if unit == 'W':
        return item['limit'] / voltage_max
    else:
        return item['limit']


def periodic_timer(current_periode:list):
    if len(charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod']) <= 0:
        return
    current_plan = charging_plan['chargingProfile']['chargingSchedule'][0]['chargingSchedulePeriod'].pop(0)
    # print(current_plan)
    interval = current_plan['startPeriod'] - current_periode[0]
    limit = get_limit_value(current_plan)
    set_current(limit)
    current_periode[0] = current_plan['startPeriod'] # current_periode += interval
    if current_periode[0] // request_periode >= current_periode[1]:
        if current_periode[1] != 0:
            print('再次请求')
        current_periode[1] = current_periode[0] // request_periode
    threading.Timer(interval, periodic_timer,[current_periode]).start()



# 每3秒触发一次


# periodic_timer(current_periode)
# print([num for num in range(1,248)])


class EVSE(object):
    def __init__(self,id):
        self.__id = id
        self.count = 1
        print(f'实例{self.__id}的计数{self.count}')
        self.count += 1

    def conn(self, m):
        print('连接', self.__id)
        m()
        ...

class Manager(object):
    def __init__(self):
        self.obj_dict ={}
        self.num_list = [n for n in range(1,248)]
        self.data_dict = {}

    def find_EVSE(self):
        id_num = self.num_list.pop(0)
        return id_num

    def set_EVSE(self, id):
        item = EVSE(str(id))
        self.obj_dict[str(id)] = item
        item.conn(lambda message='EVSE_Message': self.handle(message, id))
        print(self.obj_dict)

    def handle(self,message, id):
        print(f'这个是信号{message}处理{id}')
        self.data_dict[id] = message
        print(self.data_dict)

def test():
    print('test')
a= Manager()
# print(a.obj_dict['1'])
#a.obj_dict['1'].conn(test)
a.set_EVSE(1)
a.set_EVSE(2)
a.set_EVSE(1)