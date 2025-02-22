import json
from datetime import datetime

from apps.checks.misc.sheet import GoogleSheet

date_format = '%Y-%m-%d %H:%M'


class Check:

    @staticmethod
    def find_id(id_: str):
        sheet = GoogleSheet.open_file('Checks')
        cells = sheet.findall(str(id_))
        if cells:
            return True

    @staticmethod
    def write_to_sheet(data: list):
        sheet = GoogleSheet.open_file('Checks')
        for item in data:
            sheet.append_row(item)

    @staticmethod
    def parse_json(file):
        result = []
        data = json.loads(file)
        ticket = data[0].get("ticket", {}).get("document", {}).get("receipt", {})
        items = ticket.get("items", [])
        id_ = data[0].get("_id")
        place = ticket.get("retailPlace", '')
        place_adress = ticket.get("retailPlaceAddress", '')
        iso_string = ticket.get("dateTime", '')
        date = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S").strftime(date_format)
        for item in items:
            name = item.get("name", "Неизвестно")
            price = item.get("price", 0) / 100  # Цена в копейках
            quantity = item.get("quantity", 0)
            total = item.get("sum", 0) / 100  # Итоговая сумма в копейках
            result.append([date, name, quantity, price, total, place, place_adress, id_])
        return result, id_
