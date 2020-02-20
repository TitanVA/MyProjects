import requests
import time

running = True

URL1 = 'https://html.mineto.site/index.php?page=api&action=getuserstatus&api_key'
URL2 = ''
URL = URL1 + URL2
min_hashrate = 7000000.00


class Mining:
    def __init__(self, url, min_hash):
        self.url = url
        self.min_hash = min_hash

    def get_hashrate(self):
        r = requests.get(self.url)
        r = r.json()
        return r['getuserstatus']['data']['hashrate']

    def send_alert(self):
        pass


html = Mining(URL, min_hashrate)
while True:
    hash = html.get_hashrate()
    print(hash)
    if hash < min_hashrate:
        html.send_alert()
        print('Alert')
    time.sleep(10)