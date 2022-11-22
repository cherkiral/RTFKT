import imaplib
import requests
from pprint import pprint
import re
import json
import random
import time
import cfscrape
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from making_driver import proxy_chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

path_to_mails = "D:\Прога\Работа\Python\RTFKT\mails.txt"
EXTENSION_PATH = "D:\Прога\Работа\Selenium extentions\metamask.crx"
PATH_TO_PROXIES = "D:\Прога\Работа\Webshare 500 proxies.txt"
path_to_seed = "D:\Прога\Работа\Python\RTFKT\seed.txt"

with open(path_to_seed) as f:
    seed_list = f.readlines()

def log_in_list(path):
    with open(path) as f:
        temp_log_in = f.readlines()
    return temp_log_in


def proxies_list(path):
    with open(path) as f:
        temp_proxies = f.readlines()
    return temp_proxies


def mail_list(path):
    with open(path) as f:
        temp_mails = f.readlines()
    return temp_mails


def get_mail(temp, number):
    mails = {}
    for i in range(len(temp)):
        mails[i] = {
            'email': temp[i].split(';')[0],
            'password': temp[i].split(';')[1].rstrip()
        }
    return mails[number]


def get_proxies(temp, number):
    proxies = {}
    for i in range(len(temp)):
        proxies[i] = {
            'http': temp[i].rstrip(),
            'https': temp[i].rstrip()
        }
    return proxies[number]


def connect_metamask(number, driver):
    driver.switch_to.window(driver.window_handles[1])

    driver.close()
    time.sleep(0.5)

    driver.switch_to.window(driver.window_handles[0])

    driver.get('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html')
    time.sleep(3)

    driver.find_element('xpath', '//*[@data-testid="first-time-flow__button"]').click()
    time.sleep(2)

    driver.find_element('xpath', '//*[@data-testid="page-container-footer-next"]').click()
    time.sleep(2)

    driver.find_element('xpath', '//*[@data-testid="import-wallet-button"]').click()
    time.sleep(2)

    try:
        driver.find_element('xpath', '//*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button').click()
        time.sleep(1)
    except Exception:
        pass

    for i in range(12):
        keys = seed_list[number].rstrip().split()[i]
        driver.find_element('xpath', f'//*[@id="import-srp__srp-word-{i}"]').send_keys(keys)

    driver.find_element('xpath', '//*[@id="password"]').send_keys('12345678')
    time.sleep(0.5)
    driver.find_element('xpath', '//*[@id="confirm-password"]').send_keys('12345678')
    time.sleep(0.5)
    driver.find_element('xpath', '//*[@id="create-new-vault__terms-checkbox"]').click()
    time.sleep(0.5)
    driver.find_element('xpath', '//*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button').click()

    driver.refresh()
    time.sleep(5)

    driver.find_element('xpath', '//*[@role="button"]').click()
    time.sleep(1)

    driver.find_element('xpath', '//*[@class="reveal-seed-phrase__reveal-button"]').click()
    time.sleep(1)

    driver.find_element('xpath', '//*[@role="button"][1]').click()
    time.sleep(1)

    # for i in range(12):
    #     keys = seed_list[number].rstrip().split()[i]
    #     driver.find_element('xpath', f'//*[text() = {keys}]').click()
    #     time.sleep(0.5)


def rtfkt(number, driver):
    temp_mail = get_mail(mail_list(path_to_mails), number)['email']
    temp_pass = get_mail(mail_list(path_to_mails), number)['password']
    driver.get('https://rtfkt.com/')
    time.sleep(1)

    driver.find_element('xpath', '//*[@id="app"]/nav/div[1]/div[3]/div[1]/rtfkt-button').click()
    time.sleep(1)

    shadow_host = driver.find_element(By.CSS_SELECTOR, 'rtfkt-input:first-of-type')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[placeholder="Username or email"]').send_keys(
        temp_mail.split('@')[0])

    shadow_host = driver.find_element(By.CSS_SELECTOR, 'rtfkt-input:nth-of-type(2)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[placeholder="Password"]').send_keys(
        temp_pass + ')' + '\n')
    time.sleep(3)

def get_driver(number):
    temp_proxy = get_proxies(proxies_list(PATH_TO_PROXIES), number)
    LOGIN = temp_proxy['http'].split('http://')[1].split('@')[0].split(':')[0]
    PASS = temp_proxy['http'].split('http://')[1].split('@')[0].split(':')[1]
    IP = temp_proxy['http'].split('http://')[1].split('@')[1].split(':')[0]
    PORT = temp_proxy['http'].split('http://')[1].split('@')[1].split(':')[1]

    opt = proxy_chrome(IP, int(PORT), LOGIN, PASS)

    opt.add_extension("D:\Прога\Работа\Selenium extentions\metamask.crx")
    opt.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 "
        "Safari/537.36")
    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)

path_to_log_in = "D:\Прога\Работа\Python\RTFKT\log_in_information.txt"
path_to_verif = "D:\Прога\Работа\Python\RTFKT\\verify_links.txt"
path_to_proxies = "D:\Прога\Работа\Webshare 500 proxies.txt"
path_to_names = "D:\Прога\Работа\Python\RTFKT\\names.txt"


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

    match = re.search('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', raw_email.decode('utf-8'))
    link_verif = (match.group(0)).split('?')[0]
    link_verif = link_verif + f'?email={username}'
    return link_verif

def connect_wallet(number, driver):
    driver.switch_to.window(driver.window_handles[0])

    driver.find_element('xpath', '//*[@id="app"]/nav/div[1]/div[3]/div[1]/rtfkt-button[3]').click()
    time.sleep(1)

    driver.find_element('xpath', '//*[@id="app"]/nav/div[3]/div[2]/div[2]/div[2]/div[1]/div/rtfkt-button').click()
    time.sleep(5)

    driver.find_element('xpath', '//*[@class="wallet-card"]').click()
    time.sleep(5)

    driver.switch_to.window(driver.window_handles[1])

    driver.find_element('xpath', '//*[@role="button"][2]').click()
    time.sleep(2)

    driver.find_element('xpath', '//*[@role="button"][2]').click()
    time.sleep(2)

    driver.find_element('xpath', '//*[@role="button"][2]').click()
    time.sleep(2)

    driver.switch_to.window(driver.window_handles[0])

def send_information(acc_number, timeout):
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
    pprint(scraper.post("https://api.rtfkt.com/auth/register", headers=headers, proxies=proxy, data=data, timeout=timeout).text)

    with open(path_to_log_in, 'a') as f:
        f.write(get_mail(mail_list(path_to_mails), acc_number)['email'].split('@')[0] + ':' + get_mail(mail_list(path_to_mails), acc_number)['password'] + ')' + '\n')

def send_information_selenium(number, driver):
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[0])

    with open(path_to_names) as f:
        names = f.readlines()
    rand_name = names[random.randint(0, 499)].rstrip()
    driver.get('https://rtfkt.com/')
    time.sleep(2)

    driver.find_element('xpath', '//*[@id="app"]/nav/div[1]/div[3]/div[1]/rtfkt-button').click()
    time.sleep(2)

    driver.find_element('xpath', '//*[@id="app"]/nav/div[2]/div[2]/div[3]/rtfkt-button').click()
    time.sleep(1)

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.register > div.split-layout.container-fluid.container-lg.px-4 > div > div.col-12.col-lg-6.false > div > div:nth-child(2) > rtfkt-input:nth-child(1)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(rand_name)

    shadow_host = driver.find_element(By.CSS_SELECTOR,'#app > main > div.register > div.split-layout.container-fluid.container-lg.px-4 > div > div.col-12.col-lg-6.false > div > div:nth-child(2) > rtfkt-input:nth-child(2)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(get_mail(mail_list(path_to_mails), number)['email'].split('@')[0])

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.register > div.split-layout.container-fluid.container-lg.px-4 > div > div.col-12.col-lg-6.false > div > div:nth-child(4) > rtfkt-input')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(get_mail(mail_list(path_to_mails), number)['email'])

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.register > div.split-layout.container-fluid.container-lg.px-4 > div > div.col-12.col-lg-6.false > div > div.d-flex.flex-column.gap-2.mb-4.shadow-input > rtfkt-input:nth-child(1)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(get_mail(mail_list(path_to_mails), number)['password'].rstrip() + ')')

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.register > div.split-layout.container-fluid.container-lg.px-4 > div > div.col-12.col-lg-6.false > div > div.d-flex.flex-column.gap-2.mb-4.shadow-input > rtfkt-input:nth-child(2)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(get_mail(mail_list(path_to_mails), number)['password'].rstrip() + ')')

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[2]/div/div[5]/label').click()
    time.sleep(1)

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[2]/div/div[6]/label').click()
    time.sleep(1)

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[2]/div/div[7]/label').click()
    time.sleep(2)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[2]/div/rtfkt-button').click()

    with open(path_to_log_in, 'a') as f:
        f.write(get_mail(mail_list(path_to_mails), number)['email'].split('@')[0] + ':' + get_mail(mail_list(path_to_mails), number)['password'] + ')' + '\n')

def enter_draw(driver):
    with open(path_to_names) as f:
        names = f.readlines()
    rand_name = names[random.randint(0, 499)].rstrip()

    driver.get('https://rtfkt.com/')
    time.sleep(2)
    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[3]/div/div[1]/div[1]/rtfkt-button[1]').click()
    time.sleep(3)

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[4]/div/div[3]/div/div/rtfkt-button').click()
    time.sleep(2)

    # WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > p.fs-6.fw-light.mb-6'))).click()
    time.sleep(25)

    driver.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/rtfkt-button').click()

    driver.find_element('xpath', '//*[@id="content"]/div[2]/div[2]/div/ul/li[2]').click()

    driver.find_element('xpath', '//*[@id="content"]/div[4]/rtfkt-button[5]').click()

    driver.find_element('xpath', '//*[@id="content"]/div[6]/rtfkt-button[5]').click()

    driver.find_element('xpath', '//*[@id="content"]/div[8]/rtfkt-button[2]').click()

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element('xpath', '//*[@id="content"]/rtfkt-button[1]').click()

    time.sleep(1)

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.settings.mb-lg-5 > div > div > div.col-12.col-lg-6.false > div > div > rtfkt-input:nth-child(2)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys('1')

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.settings.mb-lg-5 > div > div > div.col-12.col-lg-6.false > div > div > rtfkt-input:nth-child(3)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(rand_name)

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.settings.mb-lg-5 > div > div > div.col-12.col-lg-6.false > div > div > div.col-12.d-flex > rtfkt-input.mb-2.shadow-input.col-6.pe-2')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(random.randint(12345, 99999))

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.settings.mb-lg-5 > div > div > div.col-12.col-lg-6.false > div > div > div.col-12.d-flex > rtfkt-input:nth-child(2)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys('milan')

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#app > main > div.settings.mb-lg-5 > div > div > div.col-12.col-lg-6.false > div > div > rtfkt-input:nth-child(6)')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys('milan')

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div/div/div[2]/div/div/div[2]/div/rtfkt-button').click()

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div/div/div[2]/div/div/div[2]/div/ul/li[2]').click()

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div/div/div[2]/div/div/rtfkt-button[1]').click()

    time.sleep(25)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element('xpath', '//*[@id="content"]/div[12]/div[1]/div/rtfkt-button').click()

    driver.find_element('xpath', '//*[@id="content"]/div[12]/div[1]/div/ul/li[1]').click()

    driver.find_element('xpath', '//*[@id="content"]/div[12]/div[2]/div/div/rtfkt-button').click()

    driver.find_element('xpath', '//*[@id="content"]/div[12]/div[2]/div/div/ul/li[3]').click()

    shadow_host = driver.find_element(By.CSS_SELECTOR, '#content > div:nth-child(15) > div.col-12.mb-3.mb-lg-6 > rtfkt-input')
    shadow_root = shadow_host.shadow_root
    shadow_content = shadow_root.find_element(By.CSS_SELECTOR, '[id = htmlInput]').send_keys(random.randint(1234567890, 9999999999))

    driver.find_element('xpath', '//*[@id="content"]/rtfkt-button[2]').click()
    time.sleep(3)

    driver.get('https://rtfkt.com/')
    time.sleep(3)

    driver.find_element('xpath', '//*[@id="app"]/main/div[1]/div[1]/div/div[3]/div/div[1]/div[1]/rtfkt-button[1]').click()
    time.sleep(10)

for i in range(165, 500):

    try:
        driver = get_driver(i)
        driver.maximize_window()
        send_information_selenium(i, driver)
        connect_metamask(i, driver)
        time.sleep(3)
        rtfkt(i, driver)
        time.sleep(10)
        link = get_link(i)
        print(link)
        driver.get(link)
        time.sleep(3)
        rtfkt(i, driver)
        time.sleep(5)
        driver.get('https://rtfkt.com/')
        time.sleep(5)
        connect_wallet(i, driver)
        time.sleep(5)
        enter_draw(driver)
        driver.quit()
        print(i)
    except Exception:
        print(Exception.args)
        pass
