ADDRESS_PATTERNS = {
    'ERC20': r'^(0x)[0-9A-Fa-f]{40}$',
    'BEP20': r'^(0x)[0-9A-Fa-f]{40}$', 
    'AVAX': r'^(X-avax)[0-9A-Za-z]{39}$',
    'XMR': r'^[48][a-zA-Zd]{94}([a-zA-Zd]{11})?$',
    'ARBITRUM': r'^(0x)[0-9A-Fa-f]{40}$',
    'MATIC': r'^(0x)[0-9A-Fa-f]{40}$',
    'POLYGON': r'^(0x)[0-9A-Fa-f]{40}$',
    'TON': r'^[UE][Qf][0-9a-zA-Z-_]{46}$',
    'SOL': r'^[1-9A-HJ-NP-Za-km-z]{32,44}$',
    'DOGE': r'^(D|A|9)[a-km-zA-HJ-NP-Z1-9]{33,34}$',
    'BTC': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[(bc1q)|(bc1p)][0-9A-Za-z]{37,62}$',
    'TRC20': r'^T[1-9A-HJ-NP-Za-km-z]{33}$',
    'LTC': r'^(L|M)[A-Za-z0-9]{33}$|^(ltc1)[0-9A-Za-z]{39}$',
    'BCH': r'^[1][a-km-zA-HJ-NP-Z1-9]{25,34}$|^[0-9a-z]{42,42}$',
    'DASH': r'^[X|7][0-9A-Za-z]{33}$'
}


STATUS_WITHDRAW = {
    "1": "pending payment",
    "2": "awaiting network confirmation",
    "3": "successful exchange",
    "4": "canceled",
    "5": "AML block",
    "6": "requisites need to be changed (if the specified aml is large or the wrong bank is selected for SBP transfer)",
    "7": "bank processing (only when payment is made to Sberbank or SBP)"
}


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
