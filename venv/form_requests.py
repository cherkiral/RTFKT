import requests
import random

PATH_TO_PROXIES = "D:\Прога\Работа\Webshare 500 proxies.txt"
PATH_TO_RAMBLER = "D:\Прога\Работа\\rambler.txt"
PATH_TO_WALLETS = "D:\Прога\Работа\Address.txt"

def proxies_list(path):
    with open(path) as f:
        temp_proxies = f.readlines()
    return temp_proxies

def mail_list(path):
    with open(path) as f:
        temp_mails = f.readlines()
    return temp_mails

def wallet_list(path):
    with open(path) as f:
        temp_wallet = f.readlines()
    return temp_wallet

def get_proxies(temp, number):
    proxies = {}
    for i in range(len(temp)):
        proxies[i] = {
            'http': temp[i].rstrip(),
            'https': temp[i].rstrip()
        }
    return proxies[number]


GoogleURL = 'https://docs.google.com/forms/d/e/1FAIpQLScKru-oiyk7uzSlKDLJqtPiS5rnEqvxqkPP4UTDHKp9OfrvAA'

urlResponse = GoogleURL+'/formResponse'
urlReferer = GoogleURL+'/viewform'


for i in range(0, 10000):
    mail = mail_list(PATH_TO_RAMBLER)[i].rstrip()
    wallet = wallet_list(PATH_TO_WALLETS)[i].rstrip()
    form_data = {
        'entry.565538350': mail,
        'entry.1527178928': wallet
    }

    user_agent = {'Referer':urlReferer,'User-Agent': "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.52 Safari/537.36"}
    while True:
        proxy = get_proxies(proxies_list(PATH_TO_PROXIES), random.randint(0, 499))
        try:
            r = requests.post(urlResponse, data=form_data, headers=user_agent, proxies=proxy, timeout=2)
            if r.status_code > 300:
                print(f'BAD with acc {i}')
                continue
            else:
                print(f'{i} {mail} is nice with wallet {wallet}')
                break
        except Exception:
            pass