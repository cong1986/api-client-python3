import base64, hashlib, hmac, time, json
from urllib.request import urlopen, Request

base_url = 'https://api.btcmarkets.net'

def request(action, key, signature, timestamp, path, data):
    header = {
        'Accept': 'application/json',
        'Accept-Charset': 'UTF-8',
        'Content-Type': 'application/json',
        'apikey': key,
        'timestamp': timestamp,
        'signature': signature,
    }

    http_request = Request(base_url + path, data, header)
    if action == 'post':
        response = urlopen(http_request, data)
    else:
        response = urlopen(http_request)
    return json.loads(response.read())

def get_request(key, secret, path):

    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = path + "\n" + nowInMilisecond + "\n"

    presignature = base64.b64encode(hmac.new(secret, stringToSign.encode('utf-8'), digestmod=hashlib.sha512).digest())
    signature = presignature.decode('utf8')


    return request('get', key, signature, nowInMilisecond, path, None)

def post_request(key, secret, path, postData):

    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = path + "\n" + nowInMilisecond + "\n" + postData

    signature = base64.b64encode(hmac.new(secret, stringToSign.encode('utf-8'), digestmod=hashlib.sha512).digest())

    return request('post', key, signature, nowInMilisecond, path, postData)

class BTCMarkets:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    def account_balance(self):

        return get_request(self.key, self.secret, '/account/balance')

api_key = 'your key'
private_key = 'your private key'

client = BTCMarkets (api_key, private_key)

print (client.account_balance())
