import sys
import json
import requests

# server酱开关，填off不开启(默认)，填on同时开启cookie失效通知和签到成功通知
sever = 'on'



def start(sckey,cookie):
    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    # checkin = requests.post(url,headers={'cookie': cookie ,'referer': referer })
    # state =  requests.get(url2,headers={'cookie': cookie ,'referer': referer})
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 " \
                "Safari/537.36 "
    payload = {
        # 'token': 'glados_network'
        'token': 'glados.network'
    }
    checkin = requests.post(url,
                            headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent,
                                     'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
    state = requests.get(url2,
                         headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})
    print(checkin.text)
    print(state.text)


    if 'message' in checkin.text:
        mess = checkin.json()['message']
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        print(mess)
        print(time)
        if sever == 'on':
            requests.get('https://sctapi.ftqq.com/' + sckey + '.send?title='+mess+'，you have '+time+' days left')

    else:
        requests.get('https://sctapi.ftqq.com/' + sckey + '.send?title=error')
        print("error")

    checkin.close()
    state.close()

def main_handler(event, context):
    start()


if __name__ == "__main__":
    sckey = sys.argv[1]
    cookie = sys.argv[2]
    print(sys.argv[1:])
    try:
        start(sckey, cookie)
    except Exception:
        exit(1)
