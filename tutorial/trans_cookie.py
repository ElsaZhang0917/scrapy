# -*- coding: utf-8 -*-
class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict


if __name__ == "__main__":
    cookie = "navCtgScroll=0; showNav=#nav-tab|0|1; showNav=javascript:; navCtgScroll=0; _lxsdk_cuid=16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8; _lxsdk=16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8; _hc.v=bdf9071a-fad7-2616-2606-4e67d0f1ea2b.1576389784; cy=7; cye=shenzhen; s_ViewType=10; fspop=test; _lx_utm=utm_source%3Dgoogle%26utm_medium%3Dorganic; t_lxid=1719ac52a93c8-0e251eba695ead-396e7507-1aeaa0-1719ac52a93c8-tid; dplet=d58d7496f5860c83fe2e3e9c64fedb01; dper=26f7be90c8fd77a6e45b004e14cfe17bd878d973eb7569110c41ea156c18620d06cdcaf800b0343a3a1f08b941d5065200fcd73d3969b38882e1d43916ea7a33ef90d76ec04847c1897a8abf1a9eeeb6e6b8b6dc847ef2aee2f2573754c3226d; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_6884594313; ctu=81abb58f8dc816d0ae8bf04402d12ff04e0f440b174c52c74484a97684f9bf50"
    trans = transCookie(cookie)
    print(trans.stringToDict())

{'navCtgScroll': '0', 'showNav': 'javascript:', '_lxsdk_cuid': '16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8', '_lxsdk': '16f08272e5dc8-0a7fa797654a26-1c3f6a5a-1aeaa0-16f08272e5dc8', '_hc.v': 'bdf9071a-fad7-2616-2606-4e67d0f1ea2b.1576389784', 'cy': '7', 'cye': 'shenzhen', 's_ViewType': '10', 'fspop': 'test', '_lx_utm': 'utm_source%3Dgoogle%26utm_medium%3Dorganic', 't_lxid': '1719ac52a93c8-0e251eba695ead-396e7507-1aeaa0-1719ac52a93c8-tid', 'dplet': 'd58d7496f5860c83fe2e3e9c64fedb01', 'dper': '26f7be90c8fd77a6e45b004e14cfe17bd878d973eb7569110c41ea156c18620d06cdcaf800b0343a3a1f08b941d5065200fcd73d3969b38882e1d43916ea7a33ef90d76ec04847c1897a8abf1a9eeeb6e6b8b6dc847ef2aee2f2573754c3226d', 'll': '7fd06e815b796be3df069dec7836c3df', 'ua': 'dpuser_6884594313', 'ctu': '81abb58f8dc816d0ae8bf04402d12ff04e0f440b174c52c74484a97684f9bf50'}


