
from time import sleep
import requests

# main_url = "http://127.0.0.1:6666"
main_url = "http://192.168.124.9:6666"
# main_url = "http://192.168.1.103:6666"
sub_url0 = main_url + "/emeter/0"
sub_url1 = main_url + "/emeter/1"
sub_url2 = main_url + "/emeter/2"

reset_url0 = sub_url0+"/reset_totals"
reset_url1 = sub_url1+"/reset_totals"
reset_url2 = sub_url2+"/reset_totals"
reset_url = main_url+"/reset_totals"


def req():
    response_0: requests.Response = requests.get(sub_url0, timeout=2)
    response_0.raise_for_status()
    data_0: dict = response_0.json()
    print(data_0)

    response_1: requests.Response = requests.get(sub_url1, timeout=2)
    response_1.raise_for_status()
    data_1: dict = response_1.json()
    print(data_1)

    response_2: requests.Response = requests.get(sub_url2, timeout=2)
    response_2.raise_for_status()
    data_2: dict = response_2.json()
    print(data_2)
    print('---------------------------------------------------------------------')


def cls():
    print('清零')
    response_0: requests.Response = requests.get(reset_url0, timeout=2)
    response_0.raise_for_status()
    response_1: requests.Response = requests.get(reset_url1, timeout=2)
    response_1.raise_for_status()
    response_2: requests.Response = requests.get(reset_url2, timeout=2)
    response_2.raise_for_status()
    # response: requests.Response = requests.get(reset_url, timeout=2)
    # response.raise_for_status()


while True:
    req()
    sleep(2)
    req()
    sleep(2)
    req()
    sleep(2)
    cls()
    sleep(2)
