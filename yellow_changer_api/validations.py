BANKS = {
    "sbpsber": "Сбер",
    "sbptinkoff": "Тинькофф",
    "sbpraif": "Райффайзен",
    "sbpalfa": "Альфабанк",
    "sbpotkritie": "Открытие",
    "sbpvtb": "ВТБ",
    "sbpsovkombank": "Совкомбанк",
    "sbpgazprom": "Газпром",
    "sbprosbank": "Росбанк",
    "sbppsb": "Промсвязьбанк (ПСБ)",
    "sbpakbars": "АкБарс",
    "sbprnkb": "РНКБ",
    "sbpotp": "ОТП",
    "sbpozon": "Озон",
    "sbpmtc": "МТС",
    "sbppochtabank": "Почта банк",
    "sbpumoney": "Yoomoney",
}


def format_number(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value
