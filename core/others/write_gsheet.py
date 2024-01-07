import gspread
import json
import os
from dotenv import load_dotenv


load_dotenv()

WORKBOOK = os.getenv('WORKBOOK')
SHEET_NAMES = json.loads(os.environ['USERS_GS'])


async def write_new_op(data: dict) -> bool:
    gc = gspread.service_account()
    sh = gc.open(WORKBOOK)
    sheet = [value for key, value in SHEET_NAMES.items() if int(key) == data['user']] # проверяем юзера на принадлежность
    main_sheet = sh.worksheet(sheet[0])

    if data['type'] == 'Приход':
        prep_data = [[data['date'], float(data['amount']), '', data['comment'], '', data['warehouse']]]
        main_sheet.append_rows(prep_data, table_range='B4:G4', )
        return True

    elif data['type'] == 'Расход':
        prep_data = [[data['date'], '', float(data['amount']), data['comment'], '', data['warehouse']]]
        main_sheet.append_rows(prep_data, table_range='B4:G4', )
        return True

    return False


"""data = [['26.12.2023', '100000', '', 'Python test row append', '', '(3) Текин (копия)'],]
main_sheet.append_rows(data, table_range='B4:G4', )"""

"""test_data = {'user': 306152412, 'type': 'Приход', 'date': '04.01.2024', 'amount': '5000', 'comment': 'Ролл', 'warehouse': '(3) Текин (копия)'}
write_new_op(test_data)"""
