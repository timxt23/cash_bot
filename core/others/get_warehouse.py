import gspread
import os
from dotenv import load_dotenv


load_dotenv()

WORKBOOK = os.getenv('WORKBOOK')
SHEET_NAME = "Списки"


async def get_wh_names(search_symbols: str) -> list:
    gc = gspread.service_account()
    sh = gc.open(WORKBOOK)
    main_sheet = sh.worksheet(SHEET_NAME)
    values = main_sheet.get_values("A5:A")
    val_list = [cell[0] for cell in values]  # Убираем вложенные листы
    result = [value for value in val_list if search_symbols.lower().strip() in value.lower()]

    return result
