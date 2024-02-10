import datetime
import sqlite3
import json
import os.path
import time
import re
from datetime import timedelta
import telebot
import requests
from fake_useragent import UserAgent
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import configparser
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


connected = False
ser = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--disable-notifications')
options.add_argument('--no-sandbox')
options.add_argument('--disable-extentions')
browser = webdriver.Chrome(service=ser, options=options)



def read_config():
    check_config = os.path.exists('config-exp.ini')
    config = configparser.ConfigParser()
    login = passwd = token = chat_id = betting = martingale = workcal = blacklist = main_url = live_url = test = bet_list = norma= 0
    if (check_config == False):
        config.add_section("Account Settings")
        config.set("Account Settings", "login", "1111")
        config.set("Account Settings", "passwd", "1111")
        config.add_section("Server connect")
        config.set("Server connect", "main_string", "https://www.fon.bet/live/football/")
        config.set("Server connect", "live_string",
                   "https://line04w.bk6bba-resources.com/events/list?lang=ru&version=11539200979&scopeMarket=1600")
        config.add_section("Bot Settings")
        config.set("Bot Settings", "token", "1111")
        config.set("Bot Settings", "chat_id", "-100")
        config.add_section("Game Settings")
        config.set("Game Settings", "bet", "30, 60, 180, 540, 1620")
        config.add_section("Nobet")
        config.set("Nobet", "State", "0")
        config.add_section("Martingale")
        config.set("Martingale", "use", "1")
        config.set("Martingale", "norma", "100")
        config.add_section("Working time")
        config.set("Working time", "ПН", "00-00:23-59")
        config.set("Working time", "ВТ", "00-00:23-59")
        config.set("Working time", "СР", "00-00:23-59")
        config.set("Working time", "ЧТ", "00-00:23-59")
        config.set("Working time", "ПТ", "00-00:23-59")
        config.set("Working time", "СБ", "00-00:23-59")
        config.set("Working time", "ВС", "00-00:23-59")
        config.add_section("Black listed leagues")
        config.set("Black listed leagues", "list",
                   "83511, 93573, 83501, 87133, 79724, 66651, 71736, 83505, 83506, 84089, 84090, 85571, 89004, 73904, 89446, 83497, 80255, 92621, 89004, 73905, 85571,  76146, 76159, 85572, 85570, 76159, 87269, 91069, 83500, 72521, 83494, 83496, 70166, 84083, 83510, 30148, 44249, 88373, 87939, 83502, 85490, 28082, 86238,84086, 84087, 20006, 47450, 78907, 83491, 83492, 83493, 83495, 83498, 83503, 83507, 83508, 83509, 83652, 83653, 83654, 83907, 83908, 83909, 83910, 84158, 84159, 84232, 84238, 84239, 84242, 84248, 84251, 84328, 84972, 83499, 85110, 86416, 86415, 84081, 85490, 86238, 84084, 84091, 84082, 85490, 84087, 85490, 84087, 86238, 87280, 87269, 85489, 84081, 84088, 87940")

        with open('config-exp.ini', "w") as config_file:
            config.write(config_file)
    else:
        config.read('config-exp.ini')
        login = config.get('Account Settings', 'login')
        passwd = config.get('Account Settings', 'passwd')
        token = config.get('Bot Settings', 'token')
        chat_id = config.get('Bot Settings', 'chat_id')
        betting = dict(config.items('Game Settings'))
        martingale = config.get('Martingale', 'use')
        workcal = dict(config.items('Working time'))
        blacklist = dict(config.items('Black listed leagues'))
        main_url = config.get('Server connect', 'main_string')
        live_url = config.get('Server connect', 'live_string')
        test = config.get('Nobet', 'State')
        bet_list = dict(config.items('Game Settings'))
        norma = config.get('Martingale', 'norma')
    return login, passwd, token, chat_id, betting, martingale, workcal, blacklist, main_url, live_url, test, bet_list, norma


def connect_to_chrome():

    loginin = False
    
    login = f'{read_config()[0]}'
    password = f'{read_config()[1]}'
    try:
        browser.get('https://www.fon.bet/live/')
        browser.maximize_window()
        time.sleep(20)
        browser.implicitly_wait(20)
    except:
        print('как то хрень')
        flag = False
    try:
        # butbet = WebDriverWait(browser, 20).until(lambda x: x.find_element(By.CLASS_NAME, "_login-btn")).click()
        butbet = WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "_login-btn"))
        ).click()
        browser.implicitly_wait(3)
        email = browser.find_element(By.XPATH,
                                     "//*[@id='auth_form']/div/div/div/div/div/div/form/div[2]/div/div/input")
        email.send_keys(login)
        browser.implicitly_wait(1)
        passwd = browser.find_element(By.XPATH,
                                      "//*[@id='auth_form']/div/div/div/div/div/div/form/div[3]/div[1]/div[2]/input")
        passwd.send_keys(password)
        time.sleep(1)
        browser.implicitly_wait(1)
        # //*[@id="auth_form"]/div/div/div[2]/form/div[3]/div[2]/div/button/div
        # //*[@id="auth_form"]/div/div/div/div/div/div/form/div[5]/button
        browser.find_element(By.XPATH,
                             "//*[@id='auth_form']/div/div/div/div/div/div/form/div[5]/button").click()
        time.sleep(10)
        browser.implicitly_wait(10)
        state = 1

        loginin = True

    except:
        state = 0
        loginin = False
        browser.quit()
        flag = False
    return loginin


# def bettexp(urlslist, sum_bet, minkfall, connected):
#     return "Коннект"


def bettexp(urlslist, sum_bet, minkfall):
    state = True
    bal1 = 900
    bal2 = 1000
    #print('1')
    return state, bal1, bal2

def bettexp2(urlslist, sum_bet, minkfall):
    # print(urlslist)
    maxkf = 4
    urlx = ''
    state = False
    print('зашел в деп')
    cancel = "//div[contains(@class, 'stakes-head')]//div"
    tb05str = "//div[contains(text(), 'Тотал')]//following::div[contains(text(), '0.5')]//following::div"  # +
    tb15str = "//div[contains(text(), 'Тотал')]//following::div[contains(text(), '1.5')]//following::div"  # +
    tbxtype = "//div[contains(text(), 'Тотал голов')]//following::div[contains(text(), 'Тотал')]//following::div[4]"  # тотал любой от 45 минут (13) подумаю
    tbxstr = "//div[contains(text(), 'Тотал голов')]//following::div[contains(text(), 'Тотал')]//following::div"
    x1xstr = "//div[contains(text(), 'Исход матча')]//following::div[contains(text(), 'или')]//following::div"  # +
    x2xstr = "//div[contains(text(), 'Исход матча')]//following::div[contains(text(), 'или')]//following::div[7]"  # +
    p1tenstr = "//div[contains(text(), 'Победа в')]//following::div[5]"  # +
    p2tenstr = "//div[contains(text(), 'Победа в')]//following::div[10]"  # +
    fora15str = "//div[contains(text(), 'Фора (+1.5)')]//following::div"  # +
    tm05str = "//div[contains(text(), 'Тотал')]//following::div[contains(text(), '0.5')]//following::div//following::div[2]"  # +
    p175str = "//div[contains(text(), 'Исход матча')]//following::div[5]"  # + 9
    tm0575str = "//div[contains(text(), 'Исход матча')]//following::div[10]"  # + 10
    # p275str = "//div[contains(@class, 'market-group-box')]//div[contains(text(), 'Исход матча (основное время)')]//following::div[1]//following::div//following::div//following::div//following::div[5]"
    # tm0575str = "//div[contains(@class, 'market-group-box')]//div[contains(text(), 'Исход матча (основное время)')]/following::div[1]//following::div[1]//following::div[1]"
    # p1hockey = "//div[contains(@class, 'event-view-tables-wrap')]//div[contains(text(), ' или')]"
    # p2hockey = "//div[contains(@class, 'event-view-tables-wrap')]//div[contains(text(), ' или')]//following::div[7]"
    p1hockey = "//div[contains(text(), 'Исход матча')]//following::div[contains(text(), 'или')]//following::div"  # + 5
    tbemptynetter = "//div[contains(text(), 'Тотал голов')]//following::div[contains(text(), 'Тотал')]//following::div[4]"  # + 12
    ozystr="//div[contains(text(), 'Обе забьют')]//following::div[2]"
    oznstr = "//div[contains(text(), 'Обе забьют')]//following::div[2]//following::div[2]"
    i = 0
    while i < len(urlslist):
        urlbet = str(urlslist.loc[i, 'urls'])
        urlx = urlx + urlbet + ',\n'
        i = i + 1

    # print(urlx)
    # send_text(urlx)
    test = read_config()[10]
    balans = 20
    # ser = Service('chromedriver.exe')
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--disable-notifications')
    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-extentions')

    if int(test) == 0:
        # рабочий режим
        balansaf = 0
        balans = 0
        possible = 0
        i = 0

        # browser = webdriver.Chrome(service=ser, options=options)
        print('Количество мачтей в депе: ' + str(len(urlslist)))
        while i < len(urlslist):

            flag = True
            urlbet = urlslist.loc[i, 'urls']
            # urlx = urlx + urlbet + ',\n'
            bettype = urlslist.loc[i, 'type']
            element = i + 1
            # browser.refresh()
            try:
                browser.get(urlbet)
                browser.maximize_window()
                time.sleep(20)
                browser.implicitly_wait(20)
            except:
                print('как то хрень')
                flag = False

            if flag:
                fortext = ''

                try:
                    if bettype == 0:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, tb05str))).click()
                        fortext = "ТБ0.5"
                    if bettype == 13 or bettype == 14 or bettype == 15:
                        butt15kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, tbxstr))).click()
                        fortext = "ТБ1.5"
                    if bettype == 1:
                        butt05kf = browser.find_element(By.XPATH, x1xstr).click()
                        fortext = "1x"
                    if bettype == 2:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, p1tenstr))).click()
                        fortext = "Теннис П1"
                    if bettype == 3:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, p2tenstr))).click()
                        fortext = "Теннис П2"
                    if bettype == 4:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, x2xstr))).click()
                        fortext = "x2"
                    if bettype == 5:
                        butt05kf = browser.find_element(By.XPATH, p1hockey).click()
                        fortext = "Хоккей П1"
                    if bettype == 6:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, p2hockey))).click()
                        fortext = "Хоккей П2"
                    if bettype == 7:
                        butt05kf = browser.find_element(By.XPATH, fora15str).click()
                        fortext = "Фора (+1.5)"
                    if bettype == 8:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, tm05str))).click()
                        fortext = "ТМ05"
                    if bettype == 9:
                        butt05kf = browser.find_element(By.XPATH, p175str).click()
                        fortext = "П1 Футбол +75 минута"
                    if bettype == 10:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, tm0575str))).click()
                        fortext = "Пx Футбол +75 минута"
                    if bettype == 11:
                        butt05kf = WebDriverWait(browser, 5).until(
                            EC.element_to_be_clickable((By.XPATH, p275str))).click()
                        fortext = "П2 Футбол +75 минута"
                    if bettype == 12:
                        butt05kf = browser.find_element(By.XPATH, tbemptynetter).click()
                        fortext = "Хоккей тотал Больше Х"
                    if bettype == 4241:
                        butt05kf = browser.find_element(By.XPATH, ozystr).click()
                        fortext = "Обе забьют: да"
                    if bettype == 4242:
                        butt05kf = browser.find_element(By.XPATH, oznstr).click()
                        fortext = "Обе забьют: нет"
                    # if bettype == 13:
                    #     butt05kf = browser.find_element(By.XPATH, tbxstr).click()
                    #     fortext = "Футбол тотал Больше Х"

                    time.sleep(5)
                    state = True
                    # urlslist.loc[i, 'state'] = state
                    print('Элемент ' + str(element) + ' : ' + str(fortext) + ' выбран')
                    flag = True
                except:
                    print('Элемент ' + str(element) + ' не найден для клика ' + str(fortext))
                    state = False
                    # urlslist.loc[i, 'state'] = state

                    flag = False

            if flag == False:
                break
            # else:
            #     print('Завершен цикл доавления матчей в список депа')
            #     flag = 1
            #     state = 1

            i = i + 1

        # countall = len(urlslist)
        # stateall = urlslist['state'].sum()
        # print(str(countall) + ' : ' + str(stateall) + ' : ' + str(flag))
        try:
            balans = browser.find_element(By.XPATH,
                                          "//*[@id='headerContainer']/div[2]/header/div[2]/div/div[6]/div/a/span[2]/span/span[1]").text
            balans = float(balans.replace(' ', ''))
            state = True
        except:
            balans = 0
            state = False

        if state:
            # if int(stateall) == int(countall):
            try:

                browser.find_element(By.XPATH,
                                     "//input[contains(@class, 'sum-panel__input')]").send_keys(sum_bet)
                time.sleep(5)
                browser.implicitly_wait(5)

                # possible = browser.find_element(By.XPATH,
                #                                 "//span[contains(text(), 'Коэф')]//following::span").text
                # //input[contains(@class, 'sum-panel__input')]//following::div[2]//span[2]
                possible = browser.find_element(By.XPATH,
                                                "//input[contains(@class, 'sum-panel__input')]//following::div[2]//span[2]").text
                possible = float(possible.replace(' ', ''))
                print('Возможный выигрыш: ' + str(possible) + ', minkfall: ' + str(minkfall))

                if float(minkfall) <= float(possible) / float(sum_bet) <= float(maxkf):
                    print('Общий кеф: ' + str(float(possible) / float(sum_bet)) + ' соответствует, заключаем пари')
                    #
                    # place-button__inner
                    try:
                        balans = browser.find_element(By.XPATH,
                                                      "//*[@id='headerContainer']/div[2]/header/div[2]/div/div[6]/div/a/span[2]/span/span[1]").text
                        balans = float(balans.replace(' ', ''))
                        print('проверка баланса непосредственно перед заключением сделки.. ' + str(balans))
                    except:
                        balans = 0

                    butbet = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Заключить пари')]"))
                    ).click()
                    time.sleep(10)
                    # except:
                    #     print('почему то не нажал')

                    state = True
                    print('проверяем баланс...')
                else:
                    print('Общий кеф: ' + str(
                        float(possible) / float(
                            sum_bet)) + ' меньше минимального или ставка изменилась и стала больше ' + str(
                        maxkf) + ', НЕ заключаем пари')
                    state = False
            except:
                state = False
                balansaf = 0
                print('Не удалось заключить пари, ждем следующий цикл')

            if state:

                try:
                    browser.implicitly_wait(10)
                    balansaf = browser.find_element(By.XPATH,
                                                    "//*[@id='headerContainer']/div[2]/header/div[2]/div/div[6]/div/a/span[2]/span/span[1]").text
                    balansaf = float(balansaf.replace(' ', ''))
                    time.sleep(5)
                    browser.implicitly_wait(5)
                    state = True


                except:
                    state = False
                    balansaf = 0
                    print('Не удалось считать баланс после заключения пари')
            else:
                print('Не проходит сделка')
                state = False
                balansaf = 0
        else:
            print('статус не 1')
            state = False
            balansaf = 0

        if float(balans) <= float(balansaf) or float(balansaf) == 0:
            print('Сделка не заключена, ждем новый цикл, баланс не изменился, начальный баланс: ' + str(
                balans) + ', конечный баланс: ' + str(balansaf))
            state = False
            try:
                cancelspisok = WebDriverWait(browser, 5).until(
                    EC.element_to_be_clickable((By.XPATH, cancel))).click()
                time.sleep(5)
            except:
                print('Не удалось очистить список, в любом случае пари не заключено')
        else:
            print('Сделка заключена, баланс изменился, начальный баланс: ' + str(
                balans) + ', конечный баланс: ' + str(balansaf))
            state = True
        print('betting ' + str(state))

    else:
        # print(test + ': тестовый режим')
        state = True
        balansaf = 0
        print(sum_bet)

    return state, balansaf, balans


def db_test():
    default_dir_db = 'db'
    sheet_name1 = 'db'
    sheet_name_trend = 'trend'
    os.makedirs(f'{default_dir_db}/', exist_ok=True)
    #print('2')
    # Создаем пустой датафрейм за текущую дату если отсутствует
    check_file = os.path.exists(f'{default_dir_db}/db29.xlsx')
    check_trend_file = os.path.exists(f'{default_dir_db}/db1x-fonbet-trend.xlsx')
    if (check_file == False):
        db_1 = pd.DataFrame(
            columns=['m_id', 'id_liga', 'home', 'away', 'startkf', 'lastkf', 'kfall', 'sh', 'sa', 'step', 'sts',
                     'ct',
                     'balans', 'sumbet', 'type', 'strategy', 'id_repl'])
        db_1.to_excel(f'{default_dir_db}/db29.xlsx', sheet_name=sheet_name1, index=False)
    else:
        db_1 = pd.read_excel(f'{default_dir_db}/db29.xlsx', sheet_name=sheet_name1)

    if (check_trend_file == False):
        trend = pd.DataFrame(columns=['m_id', 'p1', 'p2', 'curtime', 'updown'])
        trend.to_excel(f'{default_dir_db}/db1x-fonbet-trend.xlsx', sheet_name=sheet_name_trend, index=False)
    else:
        trend = pd.read_excel(f'{default_dir_db}/db1x-fonbet-trend.xlsx', sheet_name=sheet_name_trend)
    return default_dir_db, sheet_name1, db_1, trend


def db_apply(temp_db, sts):
    default_dir_db = db_test()[0]
    sheet_name1 = db_test()[1]
    #print('3')
    # print(temp_db)
    if (sts == 1):
        ifsh = "overlay"
    else:
        ifsh = "replace"
    with pd.ExcelWriter(f'{default_dir_db}/db29.xlsx', engine="openpyxl", mode='a',
                        if_sheet_exists=ifsh) as writer:
        temp_db.to_excel(writer, sheet_name=sheet_name1, index=False)



def check_id(m_id, sh, sa, p1, p2, ct):
    idx = idy = 0
    default_dir_db = db_test()[0]
    sheet_name1 = db_test()[1]
    # trend_db = db_details_read(0)
    trend_db = db_test()[3]
    check_file = os.path.exists(f'{default_dir_db}/db29.xlsx')
    check_trend_file = os.path.exists(f'{default_dir_db}/db1x-fonbet-trend.xlsx')
    #print('5')
    status = False
    if not check_file:
        status = False
        # print(status)
    else:

        db_1 = pd.read_excel(f'{default_dir_db}/db29.xlsx', sheet_name=sheet_name1)

        if len(db_1) > 0:
            #print(db_1['m_id'].to_list())
            i = 0
            flag = False
            while i < len(db_1):
                m_idn =[]
                m_idn.append(db_1.loc[i,'m_id'])
                #print(len(m_idn))
                # if str(m_id) in m_idn:
                #     print(str(m_id) + ' : ' + str(m_idn[0]))
                #     status = True
                #     break
                # i += 1
                j = 0
                while j < len(m_idn):
                    #print(m_idn[idy])
                    if str(m_id) == str(m_idn[j]):
                        idy = j
                        idx = i
                        #print('found id in row: ' + str(idx) + ', column: ' + str(idy))
                        status = True
                        shtemp = []
                        satemp = []
                        ststemp = []
                        typetemp = []
                        shtemp.append(db_1.loc[idx, 'sh'])
                        satemp.append(db_1.loc[idx, 'sa'])
                        ststemp.append(db_1.loc[idx, 'sts'])
                        typetemp.append(db_1.loc[idx, 'type'])
                        #print(str(shtemp) + ' : ' + str(satemp) + ' : ' + str(ststemp) + ' : ' + str(typetemp))
                        shtemp[idy] = sh
                        satemp[idy] = sa

                        success_list = [0, 2, 6, 10, 14, 18, 22, 26]
                        unsuccess_list = [0, 1, 5, 9, 13, 17, 21, 25]

                        if int(typetemp[idy]) == 9:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) > int(sa):
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17
                        if int(typetemp[idy]) == 10:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) == int(sa):
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17
                        if typetemp[idy] == 0:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) + int(sa) > 0:
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17
                        if typetemp[idy] == 4241:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) > 0 and int(sa) > 0:
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17
                        if typetemp[idy] == 4242:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) == 0 or int(sa) == 0:
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17

                        if typetemp[idy] == 1:
                            #print(str(sh) + ':' + str(sa))
                            if int(sh) >= int(sa):
                                if ststemp[idy] not in success_list:
                                    ststemp[idy] = ststemp[idy] + 1  # 1->2, 5->6, 9->10, 13->14, 17->18
                            else:
                                # print(str(sh) + ':' + str(sa))
                                if int(ststemp[idy]) not in unsuccess_list:
                                    ststemp[idy] = ststemp[idy] - 1  # 2->1, 6->5, 10->9, 14->13, 18->17

                        #print(str(shtemp) + ' : ' + str(satemp) + ' : ' + str(ststemp) + ' : ' + str(typetemp))
                        sts_total = 0
                        #del ststemp[-1]
                        # for element in ststemp:
                        #     sts_total += int(element)

                        db_1.loc[idx, 'sh'] = shtemp
                        db_1.loc[idx, 'sa'] = satemp
                        #db_1.loc[idx, 'lastkf'] = ",".join(tempscore)

                        db_1.loc[idx, 'sts'] = ststemp
                        #db_1.loc[idx, 'sts_start'] = ststemp

                        db_apply(db_1, 2)
                        flag = True
                        break

                    j += 1
                if flag:
                    break

                i += 1

    return status




def server_fonbet_connect():
    url = 'https://line04w.bk6bba-resources.com/events/list?lang=ru&version=11539200979&scopeMarket=1600'
    agent = UserAgent()
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': agent.random
    }
    params = {
        'partner': '51',
        'getEmpty': 'true',
        'noFilterBlockEvent': 'true',
    }
    response_ = ''
    while response_ == '':
        try:
            response_ = requests.get(url)
            result_all = response_.json()
            with open('result_football_live_fonbet-real.json', 'w', encoding='utf-8') as file:
                json.dump(result_all, file, sort_keys=True, ensure_ascii=False, indent=4)
        except:
            print('Не получилось подключиться')
            continue
    with open('result_football_live_fonbet-real.json', 'r', encoding='utf-8') as file_read:
        result_all = json.load(file_read)
    return result_all


def stepbet(sumbet):
    bet_list = read_config()[11]
    step = 0
     #print('6')
    if sumbet == bet_list['bet0']:
        step = 0
    if sumbet == bet_list['bet1']:
        step = 1
    if sumbet == bet_list['bet2']:
        step = 2
    if sumbet == bet_list['bet3']:
        step = 3
    if sumbet == bet_list['bet4']:
        step = 4
    if sumbet == bet_list['bet5']:
        step = 5
    if sumbet == bet_list['bet6']:
        step = 6
    if sumbet == bet_list['bet7']:
        step = 7
    return step


def sts_count_list(stslist):
    betseq = []
    betreb = []
    #print('7')
    betseq.append('1' * stslist)
    betseq[0] = betseq[0]
    betseq.append('3' * stslist)
    betseq[1] = betseq[1]
    betseq.append('7' * stslist)
    betseq[2] = betseq[2]
    betseq.append('11' * stslist)
    betseq[3] = betseq[3]
    betseq.append('15' * stslist)
    betseq[4] = betseq[4]
    betseq.append('19' * stslist)
    betseq[5] = betseq[5]
    betseq.append('23' * stslist)
    betseq[6] = betseq[6]
    betseq.append('27' * stslist)
    betseq[7] = betseq[7]

    betreb.append('1' * stslist)
    betreb[0] = betreb[0]
    betreb.append('5' * stslist)
    betreb[1] = betreb[1]
    betreb.append('9' * stslist)
    betreb[2] = betreb[2]
    betreb.append('13' * stslist)
    betreb[3] = betreb[3]
    betreb.append('17' * stslist)
    betreb[4] = betreb[4]
    betreb.append('21' * stslist)
    betreb[5] = betreb[5]
    betreb.append('25' * stslist)
    betreb[6] = betreb[6]
    betreb.append('29' * stslist)
    betreb[7]= betreb[7]
    rubmin = stslist + 1

    return betseq, betreb, rubmin


def checkFutureSumbet(temp_db):
    # к примеру {1 ст - 30, bkf 3, mm 5}, {2, 35, 2.7, 4}, {3, 60, 2.5, 4}, {4, 65, 2.2 , 3}, {5, 120, 2, 2}, {6, 125, 1.7, 2}

    bet_list = read_config()[11]
    base_koeff = bet_list['kf0']
    max_matches_round = bet_list['mm0']
    betfuture = bet_list['bet0']
    bettype = bet_list['bt0']
    minkf = bet_list['minkf0']
    delta = bet_list['delta0']
    stop = 0
    sts_index = 0
    if len(temp_db) > 0:
        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][1]]['sts'].count()
            i += 1
        if sts_count > 0:
            base_koeff = bet_list['kf1']
            max_matches_round = bet_list['mm1']
            betfuture = bet_list['bet1']
            bettype = bet_list['bt1']
            minkf = bet_list['minkf1']
            delta = bet_list['delta1']

            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][2]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf2']
            max_matches_round = bet_list['mm2']
            betfuture = bet_list['bet2']
            bettype = bet_list['bt2']
            minkf = bet_list['minkf2']
            delta = bet_list['delta2']
            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][3]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf3']
            max_matches_round = bet_list['mm3']
            betfuture = bet_list['bet3']
            bettype = bet_list['bt3']
            minkf = bet_list['minkf3']
            delta = bet_list['delta3']
            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][4]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf4']
            max_matches_round = bet_list['mm4']
            betfuture = bet_list['bet4']
            bettype = bet_list['bt4']
            minkf = bet_list['minkf4']
            delta = bet_list['delta4']
            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][5]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf5']
            max_matches_round = bet_list['mm5']
            betfuture = bet_list['bet5']
            bettype = bet_list['bt5']
            minkf = bet_list['minkf5']
            delta = bet_list['delta5']
            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][6]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf6']
            max_matches_round = bet_list['mm6']
            betfuture = bet_list['bet6']
            bettype = bet_list['bt6']
            minkf = bet_list['minkf6']
            delta = bet_list['delta6']
            stop = 1

        sts_count = 0
        i = 1
        while i < 6:
            sts_count = sts_count + temp_db[temp_db['sts'] == sts_count_list(i)[0][7]]['sts'].count()
            i += 1
        if sts_count > 0 and stop == 0:
            base_koeff = bet_list['kf7']
            max_matches_round = bet_list['mm7']
            betfuture = bet_list['bet7']
            bettype = bet_list['bt7']
            minkf = bet_list['minkf7']
            delta = bet_list['delta7']
            stop = 1

        # lastmatch = checklastdatematch(temp_db)
        # if stop == 0:
        #     if lastmatch < 7000:
        #         print('Не закончена цепочка, есть матчи на удвоение')
        #     else:
        #         print('Цепочка закрыта, начинаем новую, начальный (future) деп: ' + str(betfuture))

    return base_koeff, max_matches_round, betfuture, bettype, float(minkf), float(delta)


def check_sts_insert(temp_db, urlslist):
    print('проверка инсерта')
    bet_list = read_config()[11]
    stslist = len(urlslist)
    #print(stslist)
    live_time_rebate = 7200
    betseq, betreb, rb = sts_count_list(stslist)
    type_newdep = urlslist['type']
    m_id_newdep = urlslist['m_id']
    #print(str(type_newdep) + ' : ' + str(m_id_newdep))
    stop = 0
    sumbet = bet_list['bet0']
    sts = betseq[0]
    minkfall = bet_list['kf0']
    # print(str(sts))
    idrepl = 0
    state = True
    balans = 0
    bal2 = 0
    success_list = [0, 2, 6, 10, 14, 18, 22, 26]
    unsuccess_list = [0, 1, 5, 9, 13, 17, 21, 25]
    curtime = datetime.datetime.now()
    match_live = 0
    if len(temp_db) > 0:
        i = 0
        while i < len(temp_db):
            ct = datetime.datetime.strptime(temp_db.loc[i, 'ct'], "%Y-%m-%d %H:%M:%S")
            live_time = curtime.timestamp() - ct.timestamp()
            if live_time < live_time_rebate:
                match_live += 1
            i += 1
        print('Одиночек в игре: ' + str(match_live))
        i = 0
        while i < len(temp_db):

            ct = datetime.datetime.strptime(temp_db.loc[i, 'ct'], "%Y-%m-%d %H:%M:%S")
            live_time = curtime.timestamp() - ct.timestamp()
            print('выбор ставки')
            if live_time > live_time_rebate:
                print('есть матчи на замену')
                if match_live <= 10:
                    #print(temp_db.loc[i, 'sts'])
                    if temp_db.loc[i, 'sts'] == 1:
                        sumbet = bet_list['bet1']
                        minkfall = bet_list['kf1']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet1): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[1]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 5:
                        sumbet = bet_list['bet2']
                        minkfall = bet_list['kf2']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet2): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[2]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 9:
                        sumbet = bet_list['bet3']
                        minkfall = bet_list['kf3']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet3): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[3]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 13:
                        sumbet = bet_list['bet4']
                        minkfall = bet_list['kf4']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet4): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[4]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 17:
                        sumbet = bet_list['bet5']
                        minkfall = bet_list['kf5']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet5): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[5]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 21:
                        sumbet = bet_list['bet6']
                        minkfall = bet_list['kf6']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet6): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[6]
                            state = True
                            break
                    if temp_db.loc[i, 'sts'] == 25:
                        sumbet = bet_list['bet7']
                        minkfall = bet_list['kf7']
                        sts_index = i
                        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                        if state:
                            print('state(bet7): ' + str(state) + ' bal: ' + str(balans) + ' idx: ' + str(
                                i))
                            temp_db.loc[sts_index, 'sts'] = 0
                            idrepl = temp_db.loc[sts_index, 'm_id']
                            stop = 1
                            sts = betreb[7]
                            state = True
                            break
                else:
                    print('Не депаем, Количество мачтей больше: ' + str(match_live))
            else:
                #print('Нет матчей на замену')
                sumbet = bet_list['bet0']
                minkfall = bet_list['kf0']
                state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
                if state:
                    print('state(bet0 - нет матчей на замену): ' + str(state) + ' bal: ' + str(balans))
                    sts = betreb[0]
                    state = True
                    break
            i += 1
        db_apply(temp_db, 2)
    else:

        sumbet = bet_list['bet0']
        minkfall = bet_list['kf0']

        state, balans, bal2 = bettexp(urlslist, sumbet, minkfall)
        if state:
            print('state(bet0 - начальный bet): ' + str(state) + ' bal: ' + str(balans))
            sts = betreb[0]
            state = True


    return state, balans, bal2, sts, sumbet, idrepl



def db_normalize(db_name, norma):

    #print('10')
    sheet_name1 = 'db'
    default_dir_db = 'db'
    test = read_config()[10]
    matches_live = 0
    db_trend = 'db1x-fonbet-trend.xlsx'
    db_1 = pd.read_excel(f'{default_dir_db}/{db_name}', sheet_name=sheet_name1)

    if len(db_1) > 0:
        endbalans = db_1['balans'][-1:].values[0]
        if int(test) == 0:
            try:
                balans = browser.find_element(By.XPATH,
                                              "//*[@id='headerContainer']/div[2]/header/div[2]/div/div[6]/div/a/span[2]/span/span[1]").text
                endbalans = float(balans.replace(' ', ''))
                state = 1
            except:
                #endbalans = db_1['balans'][-1:].values[0]
                endbalans = -1
                state = 0
        print("Начальный баланс: " + str(db_1.iloc[0]['balans']) + " - Конечный баланс: " + str(endbalans))
        # send_text("Начальный баланс: " + str(db_1.iloc[0]['balans']) + " - \nКонечный баланс: " + str(endbalans))
        print('База нормализована')
        j = 0
        if int(test) == 0:
            if len(db_1) > 0:
                if (float(endbalans) - float(norma) > float(db_1.iloc[0]['balans'])):
                    print('Текущий баланс больше нормы: ' + str(norma) + " , обнуляем счетчики удвоения")
                    while j < len(db_1):
                        db_1.loc[j, 'sts'] = 0

                        j += 1
                    db_1.loc[0, 'balans'] = endbalans
                else:
                    print(
                        'Баланс не достиг нужного значения, схема удвоений по умолчанию...' + "Начальный баланс: " + str(
                            db_1.iloc[0]['balans']) + " - Конечный баланс: " + str(endbalans))


    db_apply(db_1, 2)


def filterligues(comand1, liganame, id_liga):
    status = False
    if liganame.find("Футзал") == -1:
        if liganame.find("(Жен)") == -1:
            if comand1.find("(ж)") == -1:
                if comand1.find("(р)") == -1:
                    if comand1.find("мол") == -1:
                        if comand1.find("U19") == -1:
                            if comand1.find("U20") == -1:
                                if comand1.find("U21") == -1:
                                    if comand1.find("U23") == -1:
                                        if 11000 <= int(id_liga) <= 20001:
                                            status = True
    return status

# def printstat(strtype, foot, p1, p2, px, tb05, tm05, x1x, x2x, f15, priority, liganame, id_liga, comand1, comand2,


def printstat(strtype, foot, id_liga, comand1, comand2, comand1id, comand2id, curtime, sh, sa, m_id, ozy, ozn, x1x):
    # print(foot + ' ' + strtype + ' - ' + str(id_liga) + ' :(' + str(m_id) + ') ' + comand1 + '(' + str(
    #     comand1id) + ') - ' +
    #       comand2 + '(' + str(comand2id) + ') : (' + str(curtime) + ' мин ) ' + str(sh) + ' : ' + str(
    #     sa) + ' 1x: ' + str(x1x) +
    #       ' 2x: ' + str(x2x) + ' ТБ05: ' + str(tb05) + ' ТМ05: ' + str(tm05) + str(sa) + ', П1: ' + str(
    #     p1) + ' X: '+ str(px) + ' П2: ' + str(p2) + ', Ф1(+1.5) ' + str(f15))
    # print(foot + ' ' + strtype + ' - ' + str(id_liga) + ' :(' + str(m_id) + ') ' + comand1 + '(' + str(
    #     comand1id) + ') - ' +
    #       comand2 + '(' + str(comand2id) + ') : (' + str(curtime) + ' мин ) ' + str(sh) + ' : ' + str(
    #     sa) + ', ОЗ:да ' + str(ozy) + ', ОЗ:нет ' + str(ozn))
    print(foot + ' ' + strtype + ' - ' + str(id_liga) + ' :(' + str(m_id) + ') ' + comand1 + '(' + str(
        comand1id) + ') - ' +
          comand2 + '(' + str(comand2id) + ') : (' + str(curtime) + ' мин ) ' + str(sh) + ' : ' + str(
        sa) + ', 1х ' + str(x1x))



def parsing_football_fonbet():
    matches_live = 0
    drop_db = pd.DataFrame(
        columns=['m_id', 'id_liga', 'home', 'away', 'startkf', 'lastkf', 'kfall', 'sh', 'sa', 'step', 'sts',
                 'ct',
                 'balans', 'sumbet', 'type', 'strategy', 'id_repl'])
    # trend_db = db_details_read(0)
    trend_db = db_test()[3]
    urlslist = pd.DataFrame(columns=['urls', 'type', 'state', 'm_id'])
    urlstemp = pd.DataFrame(columns=['urls', 'type', 'state', 'm_id'])

    # if len(urlslist) > 0:
    #     urlslist.drop()
    result_all = server_fonbet_connect()
    url2 = 'https://www.fon.bet/live/'

    # dopfilter = ['ATP', 'WTA']
    bettype = -1
    check_koeff = 0
    #tmp_id = ''
    tmp_sh = ''
    tmp_sa = ''
    tmp_bettype = ''
    tmp_id = tmp_comand1 = tmp_comand2 = tempscore = tmp_liga = ''

    tmp_all = 1
    max_matches = 0

    exit = False
    temp_db = db_test()[2]
    statistic, autodata = state_type()
    base_koeff, max_matches_round, sumbetfuture, bettypes, minkf, delta = checkFutureSumbet(
        temp_db)
    autobot = False
    bet_list = read_config()[11]
    bettypes = list(map(int, bettypes.split(',')))

    # if autobot:
    #     if statistic:
    #         matches_stats = autodata['matches'].sum()
    #         if float(matches_stats) < 50:
    #             bettypes = autodata['types'].to_list()
    #         else:
    #             if (sumbetfuture == bet_list['bet0']):
    #                 bettypes = autodata['types'].astype(float).to_list()
    #             else:
    #                 bettypes = autodata['types'][:5].astype(float).to_list()
    #
    #             print('режим автоопределения типов ставок включен: ' + str(bettypes) + ', матчей в статистике: ' + str(matches_stats))
    #     else:
    #         bettypes = list(map(int, bettypes.split(',')))
    #         print('Статистики недостаточно. обычный режим')
    # else:
    #     bettypes = list(map(int, bettypes.split(',')))
    #     print('Статистика отсутстует. обычный режим')
    #print(bettypes)
    strategy = 'kf_all: ' + str(base_koeff) + ', kf_min_per_match: ' + str(
        minkf) + ', Max_Matches: ' + str(
        max_matches_round) + ', bet: ' + str(
        sumbetfuture) + ', Types: ' + str(bettypes) + ' ; delta: ' + str(delta)
    print(strategy)
    for all_sports in result_all['events']:

        if all_sports['place'] == 'live':

            # if all_sports['level'] == 2:
            #     if all_sports['name'] == 'жёлтые карты':
            #         print(str(all_sports['team1Id']) +' : ' + str(all_sports['team2Id']))

            if all_sports['level'] == 1:
                for scores in result_all['liveEventInfos']:
                    foot = scores.get('scoreFunction', '-')
                    events_list = ['Football', 'Hockey']
                    if foot in events_list:
                        subscores = scores.get('subscores', '-')
                        print(subscores)
                        event = foot
                        # print(event)
                        if scores['eventId'] == all_sports['id']:

                            m_id = all_sports['id']
                            # max_matches = 0
                            id_liga = all_sports['sportId']
                            for name_sports in result_all['sports']:
                                if name_sports['id'] == id_liga:
                                    liganame = name_sports['name']
                                    break

                                    # if (liganame.find("Англия") > 0):
                                    #    print(liganame)
                                    #    break
                            blacklist = read_config()[7]
                            black_list = blacklist['list']
                            #blacklist = list(map(int, blacklist['list']))
                            #print(black_list)
                            # working_time = read_config()[6]result = list(map(int, a))
                            #

                            taim = (scores.get('timerSeconds', 0) / 60).__format__('2.0f')


                            comand1 = str(all_sports['team1'])
                            comand2 = str(all_sports.get('team2', '-'))
                            comand1id = int(all_sports['team1Id'])
                            comand2id = int(all_sports['team2Id'])
                            curtime = (scores.get('timerSeconds', 0) / 60).__format__('2.0f')



                            # taim = 'Игра подходит'
                            score = list(scores.get('scores'))
                            # subscores = scores.get('subscores')
                            # print(subscores['Score.YellowCards'])
                            sh = int(score[0][0]['c1'])
                            sa = int(score[0][0]['c2'])




                            ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            p1 = p2 = px = x1x = x2x = ozy = ozn = tb05 = f15 = tm05 = f15t = esn = 0.0
                            strtype = ''
                            for ee in result_all['customFactors']:
                                bettype = -1
                                # max_matches = 0
                                if ee['e'] == int(all_sports['id']):
                                    servak = 0.05

                                    for tots in ee['factors']:
                                        if (tots['f'] == 921):  # п1 теннис п2 921 , football, hockey
                                            p1 = tots['v'] - servak
                                        if (tots['f'] == 922):  # x football, hockey
                                            px = tots['v'] - servak
                                        if foot == 'Hockey':
                                            if (tots['f'] == 924):  # hock p1
                                                p1 = tots['v'] - servak
                                                #print(p1)
                                        if foot == 'Hockey':
                                            if (tots['f'] == 925):  # hock p2
                                                p2 = tots['v'] - servak
                                                #print(p2)
                                        if (tots['f'] == 922):  # x football, hockey
                                            px = tots['v'] - servak - 0.1
                                        if (tots['f'] == 923):  # п2 теннис п2 923 , football, hockey
                                            p2 = tots['v'] - servak

                                        if (tots['f'] == 924):  # 1x футбол и хоккей
                                            x1x = tots['v'] - servak


                                        if (tots['f'] == 925):  # 2x футбол и хоккей
                                            x2x = tots['v'] - servak


                                        if tots['f'] == 1696 or tots['f'] == 930:  # 05
                                            if (tots['p'] == 50) and (tots['pt'] == '0.5'):
                                                tb05 = tots['v'] - servak
                                        if tots['f'] == 1697 or tots['f'] == 931:  # 05<
                                            if (tots['p'] == 50) and (tots['pt'] == '0.5'):
                                                tm05 = tots['v'] - servak
                                        if (tots['f'] == 927):  # Ф(+1.5) футбол
                                            if (tots['p'] == 150):
                                                f15 = tots['v']

                                        if (tots['f'] == 1845):  # Ф(+1.5) теннис
                                            if (tots['p'] == 150):
                                                f15t = tots['v'] - servak
                                        if (tots['f'] == 4241):  # #обе забьют да
                                           ozy = tots['v'] - servak
                                        if (tots['f'] == 4242):  # #обе забьют нет
                                           ozn = tots['v'] - servak

                            if str(id_liga) not in black_list:
                                if not check_id(m_id, sh, sa, p1, p2, ct):

                                    noblet = 0
                                    #1X
                                    if x1x != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if 1 < int(curtime) <= 80:
                                                        if sh + 1 >= sa:
                                                            if minkf <= float(x1x) <= minkf + delta:
                                                                strtype = '1Х кф 2+-'
                                                                bettype = 1
                                                                if float(bettype) in bettypes:
                                                                    noblet = 1
                                                                    max_matches += 1
                                                                    print('добавил 1Х: ' + str(
                                                                        max_matches))
                                                                    printstat(strtype, foot, id_liga, comand1, comand2,
                                                                              comand1id, comand2id, curtime, sh, sa,
                                                                              m_id, ozy, ozn, x1x)
                                                                else:
                                                                    bettype = -1
                                    #gzy, gzn
                                    if ozy != '-' and ozn != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if 1 < int(curtime) <= 45:
                                                        if minkf <= float(ozy) <= minkf + delta:
                                                            if int(sh) + int(sa) == 0:
                                                                strtype = 'ОЗ:да (футбол)'
                                                                bettype = 4241
                                                                if float(bettype) in bettypes:
                                                                    noblet = 1
                                                                    max_matches += 1
                                                                    print('добавил ОЗ: да: ' + str(
                                                                        max_matches))
                                                                    printstat(strtype, foot, id_liga, comand1, comand2,
                                                                              comand1id, comand2id, curtime, sh, sa,
                                                                              m_id, ozy, ozn,x1x)
                                                                else:
                                                                    bettype = -1
                                    #!не оз:да
                                    if ozy != '-' and ozn != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if 1 < int(curtime) <= 45:
                                                        if minkf <= float(ozy) <= minkf + delta:
                                                            if int(sh) + int(sa) == 0:
                                                                strtype = 'ОЗ:нет (футбол)'
                                                                bettype = 4242
                                                                if float(bettype) in bettypes:
                                                                    noblet = 1
                                                                    max_matches += 1
                                                                    print('добавил ОЗ: нет: ' + str(
                                                                        max_matches))
                                                                    printstat(strtype, foot, id_liga, comand1, comand2,
                                                                              comand1id, comand2id, curtime, sh, sa,
                                                                              m_id, ozy, ozn,x1x)
                                                                else:
                                                                    bettype = -1

                                    #PX
                                    if p1 != '-' and p2 != '-' and px != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if 45 < int(curtime) <= 75:
                                                        if minkf <= float(px) <= minkf + delta:
                                                            if int(sh) == int(sa):
                                                                strtype = 'PX (футбол)'
                                                                bettype = 10
                                                                if float(bettype) in bettypes:
                                                                    noblet = 1
                                                                    max_matches += 1
                                                                    print('добавил PX: ' + str(
                                                                        max_matches))
                                                                else:
                                                                    bettype = -1
                                    #p1
                                    if p1 != '-' and p2 != '-' and px != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if float(p1) < float(p2):
                                                        if 5 <= int(curtime) <= 55:
                                                            if minkf <= float(p1) <= minkf + delta:
                                                                if int(sh) >= int(sa):
                                                                    strtype = 'П1 (футбол)'
                                                                    bettype = 9
                                                                    if float(bettype) in bettypes:
                                                                        noblet = 1
                                                                        max_matches += 1
                                                                        print('добавил П1: ' + str(
                                                                            max_matches))
                                                                    else:
                                                                        bettype = -1
                                    # тб0.5
                                    if p1 != '-' and p2 != '-' and px != '-':
                                        if foot == 'Football':
                                            if noblet == 0:
                                                if filterligues(comand1, liganame, id_liga):
                                                    if 75 < int(curtime) <= 90:
                                                        if minkf <= float(tb05) <= minkf + delta:
                                                            if int(sh) + int(sa) == 0:
                                                                strtype = 'ТБ05 (футбол)'
                                                                bettype = 0
                                                                if float(bettype) in bettypes:
                                                                    noblet = 1
                                                                    max_matches += 1
                                                                    print('добавил ТБ05: ' + str(
                                                                        max_matches))
                                                                else:
                                                                    bettype = -1

                                    if bettype != -1:
                                        # printstat(strtype, foot, p1,p2, px, tb05, tm05, x1x, x2x, f15,
                                        #     priority, liganame, id_liga, comand1, comand2, comand1id, comand2id,
                                        #     curtime, sh, sa, m_id)
                                        tmp_id = tmp_id + str(m_id) + ','
                                        tmp_liga = tmp_liga + str(id_liga) + ','
                                        tmp_comand1 = tmp_comand1 + comand1 + ','  # 2
                                        tmp_comand2 = tmp_comand2 + comand2 + ','  # 3
                                        curtime = str(curtime)
                                        # tempscore = tempscore + str(p1) + ':' + str(p2) + ','
                                        tmp_sh = tmp_sh + str(sh) + ','  # 6
                                        tmp_sa = tmp_sa + str(sa) + ','  # 7
                                        url_bet = url2 + str(foot) + '/' + str(all_sports['sportId']) + '/' + str(
                                            all_sports['id'])
                                        temp = 'not'


                                        if bettype == 0:
                                            tmp_all = float(tmp_all) * float(tb05)  # 8
                                            tempscore = tempscore + str(tb05) + ','
                                        if bettype == 4241:
                                            tmp_all = float(tmp_all) * float(ozy)  # 8
                                            tempscore = tempscore + str(ozy) + ','
                                        if bettype == 4242:
                                            tmp_all = float(tmp_all) * float(ozn)  # 8
                                            tempscore = tempscore + str(ozn) + ','
                                        if bettype == 8:
                                            tmp_all = float(tmp_all) * float(tm05)  # 8
                                            tempscore = tempscore + str(tm05) + ','
                                        if bettype == 1:
                                            tmp_all = float(tmp_all) * float(x1x)  # 8
                                            tempscore = tempscore + str(x1x) + ','
                                        if bettype == 4:
                                            tmp_all = float(tmp_all) * float(x2x)  # 8
                                            tempscore = tempscore + str(x2x) + ','

                                        if bettype == 9:
                                            tmp_all = float(tmp_all) * float(p1)  # 8
                                            tempscore = tempscore + str(p1) + ':' + str(p2) + ','
                                            temp = comand1
                                        if bettype == 3 or bettype == 11:
                                            tmp_all = float(tmp_all) * float(p2)  # 8
                                            tempscore = tempscore + str(p1) + ':' + str(p2) + ','
                                            temp = comand2
                                        if bettype == 5:
                                            tmp_all = float(tmp_all) * float(x1x)  # 8
                                            tempscore = tempscore + str(x1x) + ':' + str(x2x) + ','
                                        if bettype == 6:
                                            tmp_all = float(tmp_all) * float(x2x)  # 8
                                            tempscore = tempscore + str(x1x) + ':' + str(x2x) + ','
                                        if bettype == 7:
                                            tmp_all = float(tmp_all) * float(f15)  # 8
                                            tempscore = tempscore + str(f15) + ','
                                        if bettype == 10:
                                            tmp_all = float(tmp_all) * float(px)  # 8
                                            tempscore = tempscore + str(px) + ','

                                        # tmp_all = f"{float(tmp_all):10.2f}"
                                        print('Общий кеф: ' + str(tmp_all) + ' Количество матчей: ' + str(max_matches) + ', тип: ' + str(bettype))
                                        urlslist.loc[len(urlslist.index)] = [url_bet, bettype, 0, temp]

                                        check_koeff = float(base_koeff) / float(tmp_all)
                                        # для m_id ставка есть
                                        tmp_bettype = tmp_bettype + str(bettype) + ','  # 14
                                        if float(check_koeff) < 1:
                                            print('кеф соответствует: ' + str(tmp_all))
                                            if int(max_matches) <= int(max_matches_round):

                                                print('max матчей соответствует: ')
                                                print(
                                                    'Собрано: ' + str(max_matches) + ' MAX: ' + str(max_matches_round))
                                                # send_text(
                                                #     'express на ' + str(
                                                #         urlslist.count()[0]) + ' матчей (счет) для депа')
                                                # print(urlslist['urls'])
                                                state, balansaf, balnach, sts, sumbet, idrepl = check_sts_insert(
                                                    temp_db, urlslist)
                                                print('Результаты после депа: состояние: ' + str(state) + ', баланс ДО: ' + str(balnach) + ', баланс ПОСЛЕ: ' + str(balansaf))
                                                sts_start = sts

                                                steptype = stepbet(sumbet)
                                                temp_db.loc[len(temp_db.index)] = [tmp_id[:-1], tmp_liga[:-1],
                                                                                   tmp_comand1[:-1], tmp_comand2[:-1],
                                                                                   tempscore[:-1], tempscore[:-1],
                                                                                   tmp_all, tmp_sh[:-1], tmp_sa[:-1],
                                                                                   steptype, sts, ct,
                                                                                   balansaf, sumbet, tmp_bettype[:-1],
                                                                                   strategy, idrepl]
                                                # print(exp_id)
                                                time.sleep(1)
                                                print(str(balansaf) + ' :+!+ ' + str(balnach))
                                                test = read_config()[10]


                                                if int(test) == 0:


                                                    if state:
                                                        print('bal' + str(balansaf))
                                                        # balansaf_new = checkbal()
                                                        # if float(balnach) <= float(balansaf) or float(balansaf) == 0:
                                                        print('контрольная проверка: ' + str(
                                                            state) + ', баланс до ставки: ' + str(
                                                            balnach) + ', баланс после ставки: ' + str(balansaf))
                                                        #     print('Нет депа')
                                                        #     break

                                                        db_apply(temp_db, 1)
                                                        send_text('Ставка на express ' + str(
                                                            len(urlslist)) + '(матчей) fonbet (счет) сделана, \n' + 'Сумма ставки: ' + sumbet + 'руб.\n' + str(
                                                            strategy) + ', типы ставок: ' + str(
                                                            urlslist['type'].tolist()))
                                                        time.sleep(1)
                                                        send_text('Текущий баланс (счет): ' + str(
                                                            float(balansaf.__format__('2.0f'))) + ' руб.')
                                                        check_koeff = 0
                                                        tmp_liga = tmp_comand1 = tmp_comand2 = tempscore = ''
                                                        #tmp_id = tmp_sh = tmp_sa = tmp_bettype = []
                                                        tmp_all = 1
                                                        urlslist = urlstemp.copy()
                                                        # temp_db = drop_db.copy()
                                                        # send_text(urlslist['urls'])
                                                        send_xls()
                                                        max_matches = 0
                                                        exit = True
                                                        break


                                                    else:
                                                        print(str(balansaf) + ' :-- ' + str(balnach))
                                                        send_text(
                                                            'Статус не 1, какая то ошибка')
                                                        time.sleep(10)
                                                        send_text('Текущий баланс (счет): ' + str(balansaf) + ' руб.')

                                                        check_koeff = 0
                                                        max_matches = 0
                                                        tmp_liga = tmp_comand1 = tmp_comand2 = tempscore = ''
                                                        tmp_id = tmp_sh = tmp_sa = tmp_bettype = []
                                                        tmp_all = 1
                                                        state = 0
                                                        urlslist = urlstemp.copy()
                                                        # temp_db = drop_db.copy()
                                                        # if balansaf < 20:
                                                        #     send_text('Пополните баланс')
                                                        #     # time.sleep(300)
                                                        exit = True
                                                        break
                                            else:
                                                print('количество матчей не соответствует: ' + str(
                                                    max_matches) + ': сброс')
                                                max_matches = 0
                                                check_koeff = 0
                                                tmp_liga = tmp_comand1 = tmp_comand2 = tempscore = ''
                                                tmp_id = tmp_sh = tmp_sa = tmp_bettype = []
                                                urlslist = urlstemp.copy()
                                                # temp_db = drop_db.copy()
                                                tmp_all = 1
                                                state = 0
                                                time.sleep(10)
                                                exit = True
                                                break

        if exit == True:
            print('выход из основного цикла')

            break
    else:
        print('Цикл завершен без break')




def send_text(text):
    TOKEN = read_config()[2]
    bot = telebot.TeleBot(TOKEN)
    chat_id = read_config()[3]
    try:
        bot.send_message(chat_id, text)
    except:
        print("Не удалось отправить")
        time.sleep(10)


def send_xls():
    TOKEN = read_config()[2]
    bot = telebot.TeleBot(TOKEN)
    chat_id = read_config()[3]
    time.sleep(2)
    try:
        default_dir_db = db_test()[0]
        # sheet_name1 = db_test()[1]
        bot.send_document(chat_id=chat_id, document=open(f'{default_dir_db}/db29.xlsx', 'rb'))
    except:
        print("Не удалось доставить xls")
        time.sleep(10)


def main():

    global connected, browser
    i = 0
    norma = read_config()[12]

    while i < 14000:
        if (connected == True):
            print('Хром активен...' + str(connected))

            if browser.title:
                print('Браузер открыт ' + str(browser.title))
                parsing_football_fonbet()
                time.sleep(10)
                db_normalize('db29.xlsx', norma)  # норма прибыли для обнуления удвоения в руб

            # except:
            #     print('Браузер не активен')
            #     connected = False

        else:
            connected = connect_to_chrome()
            print('Хром подкючен..' + str(connected))


        if i % 10 == 0:
            test = read_config()[10]
            if int(test) == 0:
                st = 'Рабочий режим'
            else:
                st = 'Тестовый режим'
            bet = read_config()[11]
            #statistic, wish_list = state_type()

            #stata = 'Статистика отсутствует'
            # if statistic:
            #     stata = 'Типы ставок: ' + str(wish_list['types'].to_list()) + ' : ' + '\n' \
            #             + 'Процент (проходимость): ' + str(wish_list['procent'].to_list()) + ' : ' + '\n' \
            #             + 'Кол-во матчей' + str(wish_list['matches'].to_list())
            # bets = bet['bet0'] + ' , ' + bet['bet1'] + ' , ' + bet['bet2'] + ' , ' + bet['bet3'] + ' , ' + bet[
            #     'bet4'] + ' , ' + bet['bet5'] + ' , ' + bet['bet6'] + ' , ' + bet['bet7']
            # send_text('Активен multi express: ' + str(datetime.datetime.now().strftime(
            #     "%Y-%m-%d %H:%M:%S")) + ' \n' + st + '\n' + 'Цепочка ступеней: ' + bets + ', норма прибыли: ' + str(norma) + ' руб.\n')
            # send_text(stata)
        print(str(i) +' ( ' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' )')
        i = i + 1


def state_type():
    temp_db = db_test()[2]
    listtypes = pd.DataFrame()
    state = False
    if (len(temp_db) > 0) and state:

        temp_db[['sh0', 'sh1', 'sh2']] = temp_db['sh'].str.split(',', expand=True).astype(float)
        temp_db[['sa0', 'sa1', 'sa2']] = temp_db['sa'].str.split(',', expand=True).astype(float)
        temp_db[['type0', 'type1', 'type2']] = temp_db['type'].str.split(',', expand=True).astype(float)
        temp_db[['step0', 'step1', 'step2']] = temp_db['step'].str.split(',', expand=True)

        temp_db = temp_db[['sh0', 'sh1', 'sh2', 'sa0', 'sa1', 'sa2', 'type0', 'type1', 'type2','step0','step1','step2']]
        #print(temp_db)
        state = True
        #
        #
        # state = False
        i = 0
        #   0           8           7       1           4           2               3             9             11       10         13      12
        counttb05 = counttm05 = countf15 = count1x = countx2 = countp1h = countp2h = countp175 = countp275 = countpx75 = counthock58 = counttbhockey = 0
        counttb05q = counttm05q = countf15q = count1xq = countx2q = countp1hq = countp2hq = countp175q = countp275q = countpx75q = counthock58q = counttbhockeyq = 0
        #resulttb05 = resulttm05 = resultf15 = result1x = resultx2 = resultp1h = resultp2h = resultp175 = resultp275 = resultpx75 = resulth58 = 0

        while i < len(temp_db):
            temptype0 = temp_db.loc[i, 'type0']
            temptype1 = temp_db.loc[i, 'type1']
            temptype2 = temp_db.loc[i, 'type2']
            sh0 = temp_db.loc[i, 'sh0']
            sa0 = temp_db.loc[i, 'sa0']
            sh1 = temp_db.loc[i, 'sh1']
            sa1 = temp_db.loc[i, 'sa1']
            sh2 = temp_db.loc[i, 'sh2']
            sa2 = temp_db.loc[i, 'sa2']
            try:
                if temptype0 == 12:
                    sk0 = temp_db.loc[i, 'step0']
                    #print(sk0)
            except:
                sk0 = 0
            try:
                if temptype1 == 12:
                    sk1 = temp_db.loc[i, 'step1']
                    #print(sk1)
            except:
                sk1 = 0
            try:
                if temptype2 == 12:
                    sk2 = temp_db.loc[i, 'step2']
                    #print(sk2)
            except:
                sk2 = 0


            # if temptype0 == 13:
            #     counthock58 += 1
            #     if float(sh0)+float(sa0) > float(sk0):
            #         counthock58q += 1
            # if temptype1 == 13:
            #     counthock58 += 1
            #     if float(sh1+sa1)  > float(sk1):
            #         counthock58q += 1
            # if temptype2 == 13:
            #     counthock58 += 1
            #     if float(sh2+sa2)  > float(sk2):
            #         counthock58q += 1


            if temptype0 == 12:
                counttbhockey += 1
                if sh0+sa0 + 1 > float(sk0):
                    #print(sk0)
                    counttbhockeyq += 1
            if temptype1 == 12:
                counttbhockey += 1
                print(sk1)
                if sh1+sa1 + 1> float(sk1):
                    #print(sk1)
                    counttbhockeyq += 1
            if temptype2 == 12:
                counttbhockey += 1
                #print(sk2)
                if sh2+sa2 + 1> float(sk2):
                    counttbhockeyq += 1


            #0.5
            if temptype0 == 0:
                counttb05 += 1
                if sh0+sa0 > 0:
                    counttb05q += 1
            if temptype1 == 0:
                counttb05 += 1
                if sh1 + sa1 > 0:
                    counttb05q += 1
            if temptype2 == 0:
                counttb05 += 1
                if sh2 + sa2 > 0:
                    counttb05q += 1
            #1X
            if temptype0 == 1:
                count1x += 1
                if sh0 >= sa0:
                    count1xq += 1
            if temptype1 == 1:
                count1x += 1
                if sh1 >= sa1:
                    count1xq += 1
            if temptype2 == 1:
                count1x += 1
                if sh2 >= sa2:
                    count1xq += 1

            # x2
            if temptype0 == 4:
                countx2 += 1
                if sh0 <= sa0:
                    countx2q += 1
            if temptype1 == 4:
                countx2 += 1
                if sh1 <= sa1:
                    countx2q += 1
            if temptype2 == 4:
                countx2 += 1
                if sh2 <= sa2:
                    countx2q += 1

            #f15
            if temptype0 == 7:
                countf15 += 1
                if sh0 + 1 >= sa0:
                    countf15q += 1
            if temptype1 == 7:
                countf15 += 1
                if sh1 + 1 >= sa1:
                    countf15q += 1
            if temptype2 == 7:
                countf15 += 1
                if sh2 + 1 >= sa2:
                    countf15q += 1

            #тм05
            if temptype0 == 8:
                counttm05 += 1
                if sh0 + sa0 == 0:
                    counttm05q += 1
            if temptype1 == 8:
                counttm05 += 1
                if sh1 + sa1 == 0:
                    counttm05q += 1
            if temptype2 == 8:
                counttm05 += 1
                if sh2 + sa2 == 0:
                    counttm05q += 1

            #P175
            if temptype0 == 9:
                countp175 += 1
                if sh0 > sa0:
                    countp175q += 1
            if temptype1 == 9:
                countp175 += 1
                if sh1 > sa1:
                    countp175q += 1
            if temptype2 == 9:
                countp175 += 1
                if sh2 > sa2:
                    countp175q += 1

            # PX
            if temptype0 == 10:
                countpx75 += 1
                if sh0 == sa0:
                    countpx75q += 1
            if temptype1 == 10:
                countpx75 += 1
                if sh1 == sa1:
                    countpx75q += 1
            if temptype2 == 10:
                countpx75 += 1
                if sh2 == sa2:
                    countpx75q += 1

            # P275
            if temptype0 == 11:
                countp275 += 1
                if sh0 < sa0:
                    countp275 += 1
            if temptype1 == 11:
                countp275 += 1
                if sh1 < sa1:
                    countp275q += 1
            if temptype2 == 11:
                countp275 += 1
                if sh2 < sa2:
                    countp275q += 1



            # 1X hockey
            if temptype0 == 5:
                countp1h += 1
                if sh0 >= sa0:
                    countp1hq += 1
            if temptype1 == 5:
                countp1h += 1
                if sh1 >= sa1:
                    countp1hq += 1
            if temptype2 == 5:
                countp1h += 1
                if sh2 >= sa2:
                    countp1hq += 1

            # x2 hockey
            if temptype0 == 6:
                countp2h += 1
                if sh0 <= sa0:
                    countp2hq += 1
            if temptype1 == 6:
                countp2h += 1
                if sh1 <= sa1:
                    countp2hq += 1
            if temptype2 == 6:
                countp2h += 1
                if sh2 <= sa2:
                    countp2hq += 1
            i += 1

        try:
            resulttb05 = float((counttb05q / counttb05).__format__('2.2f'))
        except:
            resulttb05 = 1
        try:
            result1x =  float((count1xq / count1x).__format__('2.2f'))
        except:
            result1x = 1
        try:
            resultx2 =  float((countx2q / countx2).__format__('2.2f'))
        except:
            resultx2 = 1
        try:
            resultf15 =  float((countf15q / countf15).__format__('2.2f'))
        except:
            resultf15 = 1
        try:
            resulttm05 = float((counttm05q / counttm05).__format__('2.2f'))
        except:
            resulttm05 = 1
        try:
            resultp175 = float((countp175q / countp175).__format__('2.2f'))
        except:
            resultp175 = 1
        try:
            resultp275 = float((countp275q / countp275).__format__('2.2f'))
        except:
            resultp275 = 1
        try:
            resultpx75 = float((countpx75q / countpx75).__format__('2.2f'))
        except:
            resultpx75 = 1
        # print('П2 +75: ' + str(countp275) + ' : ' + str(countp275q) + ' : ' + str(resultp2))
        try:
            resulth58 = float((counthock58q / counthock58).__format__('2.2f'))
        except:
            resulth58 = 0
        try:
            resulthtb = float((counttbhockeyq / counttbhockey).__format__('2.2f'))
        except:
            resulthtb = 1

        try:
            resultp1h = float((countp1hq / countp1h).__format__('2.2f'))
        except:
            resultp1h = 1
        try:
            resultp2h = float((countp2hq / countp2h).__format__('2.2f'))
        except:
            resultp2h = 1

        # print('TB05: '+str(counttb05) + ' : ' + str(counttb05q) + ' : ' + str(resulttb05))
        # print('1X: ' + str(count1x) + ' : ' + str(count1xq) + ' : ' + str(count1xq / count1x))
        # print('X2: ' + str(countx2) + ' : ' + str(countx2q) + ' : ' + str(countx2q / countx2))
        # print('F15: ' + str(countf15) + ' : ' + str(countf15q) + ' : ' + str(countf15q / countf15))
        # print('TМ05: ' + str(counttm05) + ' : ' + str(counttm05q) + ' : ' + str(counttm05q / counttm05))
        # print('П1 +75: ' + str(countp175) + ' : ' + str(countp175q) + ' : ' + str(countp175q / countp175))
        # print('ПX +75: ' + str(countpx75) + ' : ' + str(countpx75q) + ' : ' + str(countpx75q / countpx75))
        print('hock: ' + str(counttbhockeyq) + ' : ' + str(counttbhockey) + ' : ' + str(resulthtb))
        print('hock: ' + str(counthock58q) + ' : ' + str(counthock58) + ' : ' + str(resulth58))

        listtypes['types'] = [0,1,4,8,9,10,11,13,5,6,12]
        listtypes['matches'] = [counttb05, count1x, countx2, counttm05, countp175, countpx75, countp275, counthock58, countp1h, countp2h, counttbhockey]
        listtypes['procent'] = [resulttb05, result1x , resultx2, resulttm05, resultp175, resultpx75, resultp275, resulth58, resultp1h, resultp2h, resulthtb]

        # print(listtypes.sort_values('procent', ascending=False))
        listtypes = listtypes.sort_values('procent', ascending=False)
        #print(listtypes['types'][:5].to_list())
        # wish_list = listtypes['types'].to_list()
        # print(wish_list[:5])
        state = True
    return state, listtypes


# print(wish_list['types'][:5].to_list())

main()
#check_id(44190192,2,1,1.2,1.2, 1)
#state, wish = state_type()
#print(wish)


def stata_ozdanet():
    temp_db = pd.DataFrame()
    db_1 = pd.read_excel('db/db29.xlsx', sheet_name='db')

    #temp_db = db_1.groupby('id_liga').count()
    temp_db = db_1.groupby('id_liga').sum('sh' + 'sa')
    temp_db['sall'] = temp_db['sh'] + temp_db['sa']


    #temp_db = temp_db['sall']
    print(temp_db['sall'])

    temp_db.to_excel('temp-ozdanet.xlsx')






#stata_ozdanet()