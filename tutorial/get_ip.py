# /usr/bin/python 3.7
# -*-coding:utf-8*-

"""
@author: Qiandan Zhang
"""

import requests


class Proxy:
    def get_ip(self):
        order_id = '958769506319977'
        url = 'http://dps.kdlapi.com/api/getdps?&orderid={}&num={}'.format(order_id, 10)
        proxy = requests.get(url).text
        proxy_list = proxy.split(',')
        with open('proxies.txt', mode='w') as f:
            for p in proxy_list:
                f.write(p)
        print('Successfully get proxy!')