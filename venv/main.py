import imaplib
import requests
from pprint import pprint
import re
import json
import random
import time
import cfscrape

path_to_mails = "D:\Прога\Работа\Python\RTFKT\mails.txt"
path_to_log_in = "D:\Прога\Работа\Python\RTFKT\log_in_information.txt"
path_to_verif = "D:\Прога\Работа\Python\RTFKT\\verify_links.txt"
path_to_proxies = "D:\Прога\Работа\Webshare 500 proxies.txt"
path_to_names = "D:\Прога\Работа\Python\RTFKT\\names.txt"

def mail_list(path):
    with open(path) as f:
        temp_mails = f.readlines()
    return temp_mails

def log_in_list(path):
    with open(path) as f:
        temp_log_in = f.readlines()
    return temp_log_in

def proxies_list(path):
    with open(path) as f:
        temp_proxies = f.readlines()
    return temp_proxies

def get_mail(temp, number):
    mails = {}
    for i in range(len(temp)):
        mails[i] = {
            'email' : temp[i].split(';')[0],
            'password': temp[i].split(';')[1].rstrip()
        }
    return mails[number]

def get_proxies(temp, number):
    proxies = {}
    for i in range(len(temp)):
        proxies[i] = {
            'http' : temp[i].rstrip(),
            'https': temp[i].rstrip()
        }
    return proxies[number]

def send_information(acc_number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36'
    }
    proxy = get_proxies(proxies_list(path_to_proxies), acc_number)

    with open(path_to_names) as f:
        names = f.readlines()

    rand_name = names[random.randint(0,499)].rstrip()

    data = {
        "fullName": rand_name,
        "email": get_mail(mail_list(path_to_mails), acc_number)['email'],
        "password": get_mail(mail_list(path_to_mails), acc_number)['password'].rstrip() + ')',
        "username": get_mail(mail_list(path_to_mails), acc_number)['email'].split('@')[0],
        "passwordConfirm": get_mail(mail_list(path_to_mails), acc_number)['password'].rstrip() + ')',
        "stayUpToDate": True,
        "agreedPrivacyPolicy": True,
        "agreedTermsAndConditions": True,
        "channel": "WEB"
    }

    scraper = cfscrape.create_scraper()
    pprint(scraper.post("https://api.rtfkt.com/auth/register", headers=headers, proxies=proxy, json=data).json())

    with open(path_to_log_in, 'a') as f:
        f.write(get_mail(mail_list(path_to_mails), acc_number)['email'].split('@')[0] + ':' + get_mail(mail_list(path_to_mails), acc_number)['password'] + ')' + '\n')

def get_link(acc_number):
    mail_pass = get_mail(mail_list(path_to_mails), acc_number)['password']
    username = get_mail(mail_list(path_to_mails), acc_number)['email']
    imap_server = "imap.rambler.ru"
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, mail_pass)
    mail.select("inbox")

    result, data1 = mail.search(None, "ALL")

    ids = data1[0]  # Получаем сроку номеров писем

    id_list = ids.split()  # Разделяем ID писем
    latest_email_id = id_list[-1]  # Берем последний ID

    result, data1 = mail.fetch(latest_email_id, "(RFC822)")  # Получаем тело письма (RFC822) для данного ID

    raw_email = data1[0][1]  # Тело письма в необработанном виде

    match = re.search(r'https://rtfkt.com/verify[\'"]?([^\'" >]+)', raw_email.decode('utf-8'))
    verify = (str(match).split('=\'')[1].split("'")[0].split('>')[0])

    return verify


for i in range(41, 499):
    send_information(i)
    time.sleep(20)
    get_link(i)