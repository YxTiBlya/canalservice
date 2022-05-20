from datetime import datetime
import os

import httplib2
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from .db import Database

DOLLAR_RUB = 'http://www.cbr.ru/currency_base/daily/' # страница курс валют ЦБ РФ
headers = {'User': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79'}

currdate = datetime.now().date() # текущая дата

# функция для ограничение знаков после запятой(по умолчанию 2)
def toFixed(numObj, digits=2):
    return f"{numObj:.{digits}f}"

# функция для проверки сроков поставки
def checkdate(d,m,y):
    if int(y) - currdate.year >= 0:
        if int(m) - currdate.month >= 0:
            if int(d) - currdate.day >=0:
                return True
            else:
                return False
        else:
            return False
    else:
        return False

# функция для получения и возращения данных из таблицы excel
def get_excel_table():
    creds_json = os.path.dirname(__file__) + "/canalservice-088a3f6e4843.json" # путь к ключу
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    service = build('sheets', 'v4', http = creds_service)
    sheet = service.spreadsheets()

    sheet_id = '1G29FYtOGMng4O713q8dAxi_aQj_4Gu7YNM9gF82PbcI' # id таблицы

    resp = sheet.values().get(spreadsheetId = sheet_id, range = "Лист1!A2:D51").execute() # выборка значений

    return resp['values']

# функция парсинга курсов валют со страницы ЦБ РФ http://www.cbr.ru/currency_base/daily/
def pars():
    full_page = requests.get(DOLLAR_RUB, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')

    trs = soup.find_all("tr")
    for tr in trs:
        tds = tr.find("td", string="USD")
        if tds is not None:
            tr_dollar = tr
    td_dollar = tr_dollar.find_all("td")
    doll_course = td_dollar[-1].getText()
    doll_course = doll_course.replace(',','.')

    return float(doll_course)

def db():
    db = Database()
    table = get_excel_table() # получения значений таблицы excel
    DforR = pars() # получение курса доллара 

    # удаление прошлых записей из бд если она не пуста
    if len(db.table_exists()) >= 1:
        db.table_clear()
    
    # заполнение бд значениями из таблицы
    for id, order, costDoll, date in table:
        db.table_insert(id, order, costDoll, toFixed(int(costDoll) * DforR), date)
        
        # проверка истечения срока поставки
        d,m,y = date.split('.')
        if checkdate(d,m,y) == False:
            if db.order_exists(int(order)) is None: # проверка нет ли уже в дб записи с этим номером заказа
                db.add_order(int(order)) # Добавляет номер заказа в дб

