from system.Socket_Core import *


a = SocketCore(host='127.0.0.1', isServer=True)
a.signal_recv_json.connect(lambda x: print(x))
a.connect()
while 1:
    a.send({'data': 'hello 呀 米娜桑'})
    time.sleep(0.5)
