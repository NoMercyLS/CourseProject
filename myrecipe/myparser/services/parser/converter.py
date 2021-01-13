import unicodedata

quantity_library = ["по вкусу", "для обжарки", "на кончике ножа"]


def get_replaced_unit(unit):
    unit_case = {
        'fl oz': 'жидкая унция (США)/жидкая унция (британская)',
        'lb': 'фунт',
        'oz': 'унция',
        'pt': 'пинта (США)/пинта (британская)',
        'веточек': 'штук',
        'веточка': 'штук',
        'г': 'грамм',
        'головка': 'штук',
        'головки': 'штук',
        'д': 'десертная ложка',
        'десертная': 'десертная ложка',
        'десертной': 'десертная ложка',
        'десертных': 'десертная ложка',
        'дл': 'децилитр',
        'для': 'по вкусу',
        'зубчик': 'штук',
        'зубчика': 'штук',
        'зубчиков': 'штук',
        'кг': 'килограмм',
        'кружек': 'кружка',
        'куска': 'штук',
        'кусков': 'штук',
        'кусок': 'штук',
        'кусочек': 'штук',
        'л': 'литр',
        'мл': 'миллилитр',
        'на': 'по вкусу',
        'по': 'по вкусу',
        'ст.': 'столовая ложка',
        'стакан': 'стакан',
        'стакана': 'стакан',
        'стаканов': 'стакан',
        'стебелей': 'штук',
        'стебель': 'штук',
        'столовая': 'столовая ложка',
        'столовой': 'столовая ложка',
        'столовые': 'столовая ложка',
        'столовых': 'столовая ложка',
        'ч': 'чайная ложка',
        'ч.': 'чайная ложка',
        'чайная': 'чайная ложка',
        'чайной': 'чайная ложка',
        'чайные': 'чайная ложка',
        'чайных': 'чайная ложка',
        'шт.': 'штук',
        'штук': 'штук',
        'штука': 'штук',
        'штуки': 'штук',
        'щепоток': 'щепотка'
    }
    return unit_case[unit]


def get_calculated_quantity(quantity):
    if quantity is None:
        return None
    if quantity.find("-") != -1:
        quantity = quantity.split('-')
        quantity = quantity[1]
        return int(quantity)
    if quantity.find("/") != -1:
        quantity = quantity.split('/')
        quantity = int(quantity[0]) / int(quantity[1])
        return float(quantity)
    if quantity.find(',') != -1:
        quantity = quantity.split(',')
        quantity = int(quantity[0]) + int(quantity[1]) / int(10)
        return float(quantity)
    if quantity.isdigit():
        return quantity
    return float(unicodedata.numeric(quantity))


def convert_time(time):
    if len(time) > 2:
        result = int(time[0]) * 60 + int(time[2])
    else:
        if 'мин' in time[1]:
            result = int(time[0])
        else:
            result = int(time[0]) * 60
    return result
