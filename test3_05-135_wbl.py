import datetime
import json
import os.path
import time
import re
import telebot
import requests
from fake_useragent import UserAgent
import pandas as pd

TOKEN = ""
bot = telebot.TeleBot(TOKEN)
chat_id = ''

url = 'https://1xstavka.ru/live/football/'
url2 = 'https://1xstavka.ru/LiveFeed/Get1x2_VZip?count=100&mode=4&top=true&partner=51'

def db_test():
    default_dir_db = 'db'
    #sheet_name1 = datetime.datetime.now()
    #sheet_name1 = sheet_name1.strftime("%Y-%m-%d")
    sheet_name1='db05135'
    os.makedirs(f'{default_dir_db}/', exist_ok=True)
    #db_default = 'db05135.xlsx'
    # Создаем пустой датафрейм за текущую дату если отсутствует
    check_file = os.path.exists(f'{default_dir_db}/db05135.xlsx')
    if (check_file == False):
        db_1 = pd.DataFrame(columns=['m_id', 'id_liga', 'liga', 'home', 'away', 'tb05time', 'taim', 'score', 'tb05', 'status', 'sts', 'ct'])
        db_1.to_excel(f'{default_dir_db}/db05135.xlsx', sheet_name=sheet_name1, index=False)
    else:
        db_1 = pd.read_excel(f'{default_dir_db}/db05135.xlsx', sheet_name=sheet_name1)
        #print(db_1)
    return default_dir_db, sheet_name1, db_1


def db_apply(temp_db, sts):
    default_dir_db = db_test()[0]
    sheet_name1 = db_test()[1]
    #print(temp_db)
    if (sts == 1):
        ifsh = "overlay"
    else:
        ifsh = "replace"
    with pd.ExcelWriter(f'{default_dir_db}/db05135.xlsx',engine="openpyxl", mode='a', if_sheet_exists=ifsh) as writer:
        temp_db.to_excel(writer, sheet_name=sheet_name1,index=False)



def check_id(m_id):
    default_dir_db = db_test()[0]
    sheet_name1 = db_test()[1]
    check_file = os.path.exists(f'{default_dir_db}/db05135.xlsx')
    status = False
    if (check_file == False):
        status = False
        #print(status)
    else:
        db_1 = pd.read_excel(f'{default_dir_db}/db05135.xlsx', sheet_name=sheet_name1)
        if (len(db_1) > 0):
            mel_count = (db_1['m_id'] == m_id).sum()
            #print(mel_count)
            if mel_count>0:
                status = True
                #print(status)
    return status


def parsing_football():

    agent = UserAgent()
    headers = {
        'Accept': 'application/json, text/plain, */*',

        'User-Agent': agent.random
    }

    params = {
        'sports': '1',
        'count': '50',
        'antisports': '188',
        'mode': '4',
        'country': '1',
        'partner': '51',
        'getEmpty': 'true',
        'noFilterBlockEvent': 'true',
    }
    response_ = ''

    game_id_all = []
    while response_ == '':
        try:
            response_ = requests.get('https://1xstavka.ru/LiveFeed/Get1x2_VZip', params=params, headers=headers, timeout=3)
            #response_ = requests.get('https://melbet.ru/LiveFeed/Get1x2_VZip', params=params, headers=headers, timeout=3)
            result_all = response_.json()
            with open('result_football_live_new.json', 'w', encoding='utf-8') as file:
                json.dump(result_all, file, sort_keys=True, ensure_ascii=False, indent=4)
        except:
            time.sleep(50)
            print('Не получилось подключиться')
            continue
    with open('result_football_live_new.json', 'r',
              encoding='utf-8') as file_read:
        result_all = json.load(file_read)
    data_list = []

    #Начальные параметры читаем с экселя
    black_list = {2056113,
                  2071516,
                  2165493,
                  2055972,
                  2055959,
                  2103135,
                  1222861,
                  2120110,
                  2055846,
                  2170155,
                  2130174,
                  2101142,
                  2316222,
                  2172323,
                  2055906,
                  2055922,
                  2162429,
                  2183824,
                  2229769,
                  2226159,
                  2492942,
                  2481138,
                  150505,
                  2059891,
                  2165493,
                  2492384,
                  2057156
                  }

    for all_football in result_all['Value']:
        game_id_d = []
        if all_football['SC'].get('TS', 0) < 6000:
            id_liga = all_football.get('LI', '-')

            if int(id_liga) not in black_list:
                game_id_d.append(all_football["L"])
                m_id = all_football['I']
                game_id_all.append(id)
                liga = all_football.get('L', '-')
                #print(liga)
                ligaE = all_football.get('LE', '-')
                com1E = all_football['O1E']
                # print(comand1)
                com2E = all_football['O2E']
                #print(m_id)
                ligaE = re.sub('[^A-Za-z0-9]+', '', ligaE)
                com1E = re.sub('[^A-Za-z0-9]+', '', com1E)
                com2E = re.sub('[^A-Za-z0-9]+', '', com2E)
                url_bet=(url+str(id_liga)+'-'+ligaE+'/'+str(m_id)+'-'+com1E+'-'+com2E).replace(" ", "-")
                game_id = all_football.get('I')
                #print(url_bet)
                comand1 = all_football['O1']
                #print(comand1)
                comand2 = all_football['O2']
                #print(comand2)
                curtime = all_football['SC'].get('TS', 0)
                curtime = (curtime / 60).__format__('2.0f')
                #print(curtime)
                taim = all_football['SC'].get('CPS', '-')
                #print(taim)
                score = [all_football['SC']['FS'].get('S1', 0), all_football['SC']['FS'].get('S2', 0)]
                #print(url_bet)
                tb05='-'
                for tots in all_football['AE']:
                    for tot in tots['ME']:
                        if (tot['G'] == 17 and tot['T']==9):
                            if (tot['P']==0.5):
                                tb05=str(tot['C'])
                Status = 'В ожидании'
                sts = 0
                temp_db = db_test()[2]
                ct = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data = {
                    'm_id': m_id,
                    'id_liga': id_liga,
                    'liga': liga,
                    'home': comand1,
                    'away': comand2,
                    'tb05time': curtime,
                    'taim': taim,
                    'score': f'{score[0]}:{score[1]}',
                    'tb05': tb05,
                    'status': Status,
                    'sts': sts,
                    'ct': ct
                    }
                #стратегия 1
                if (check_id(m_id) == False):
                    if (score[0]+score[1]<1):
                        if (int(curtime)>1):
                            if (tb05!='-'):
                                if ((float(tb05)>1.35) and (float(tb05)<3)):
                                    Status = 'Матч подходит, ставка сделана'
                                    data['sts'] = 1
                                    data['status'] = 'Ставка не зашла'
                                    data['tb05time'] = curtime
                                    data_list.append(data)
                                    temp_db.loc[len(temp_db.index)] = data
                                    #print(temp_db)
                                    db_apply(temp_db, data['sts'])
                                    #сделали ставку, матч на мониторинге по ид
                                    send_text('Match ID_05(1.35):['+url_bet+ ']\n' + Status + '  '+ liga + '.\n' + comand1+ ' : ' + comand2 +'\n( ' + str(score[0])+' : '+str(score[1]) + ', '+taim+' '+str(curtime)+' минута)    \nТБ0.5: ' + tb05 + '\n' + 'Время ставки: ' + ct)
                                    print(Status + '  ' + liga + '. \n' + comand1 + ' : ' + comand2 + '\n( ' + str(
                                        score[0]) + ' : ' + str(score[1]) + ', ' + taim + ' ' + str(
                                        curtime) + ' минута)    \nТБ0.5: ' + tb05)
                                    time.sleep(2)
                else:
                    Status = 'Ставка не зашла'
                    temp_db = db_test()[2]
                    data['score']=f'{score[0]}:{score[1]}'
                    data['tb05time'] = curtime
                    data['taim'] = "Игра завершена"
                    if (len(temp_db) > 0):
                        filter = temp_db['m_id'] == m_id
                        temp_db2 = temp_db.loc[filter].copy()
                        sts = temp_db2['sts'].where(temp_db2['m_id'] == temp_db2['m_id'].max()).dropna().values[0]
                    if sts == 1:
                        #print(sts)
                        if (score[0]+score[1]>0):
                            Status = "Ставка зашла"
                            sts = 2
                            temp_db.loc[(temp_db['m_id'] == m_id), 'tb05time'] = data['tb05time']
                            temp_db.loc[(temp_db['m_id'] == m_id), 'taim'] = taim
                            temp_db.loc[(temp_db['m_id'] == m_id), 'score'] = data['score']
                            temp_db.loc[(temp_db['m_id'] == m_id), 'status'] = Status
                            temp_db.loc[(temp_db['m_id'] == m_id), 'sts'] = sts
                            db_apply(temp_db, sts)
                            sts_sum = temp_db[temp_db['sts'] == 2]['sts'].count()
                            tb_sum = temp_db[temp_db['sts'] == 2]['tb05'].sum()
                            sts_all = len(temp_db)
                            send_text('Match ID_05:[' + str(
                                m_id) + ']\n' + Status + '  \n' + liga + '.\n' + comand1 + ' : ' + comand2 + '\n(' + str(
                                score[0]) + ' : ' + str(score[1]) + ')')
                            send_xls()
                            time.sleep(2)
                            stata = (1000 + (tb_sum-sts_all)*20).__format__('2.0f')
                            send_text(str(sts_sum) + ' / ' + str(sts_all) + ', проходимость (0.5Б): ' +  (100*sts_sum / sts_all).__format__('2.0f') + '%, норма 75% \n' + 'Текущий баланс при ставке 20р, начальный баланс 1000р: ' + stata)
    #temp_db = db_test()[2]
    return data_list


def send_text(text):
    try:
        bot.send_message(chat_id, text)
    except:
        print("Не удалось отправить")
        time.sleep(10)


def send_xls():
    time.sleep(2)
    try:
        default_dir_db = db_test()[0]
        sheet_name1 = db_test()[1]
        bot.send_document(chat_id=chat_id, document=open(f'{default_dir_db}/db05135.xlsx', 'rb'))
    except:
        print("Не удалось доставить xls")
        time.sleep(10)

i=0
while i<1000:
    parsing_football()
    time.sleep(50)
    print(i)
    i=i+1

#parsing_football()

