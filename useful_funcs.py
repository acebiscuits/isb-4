import hashlib
import logging
import json

settings = {"hash": "f56ab81d14e7c55304dff878c3f61f2d96c8ef1f56aff163320e67df",
"first_digits": ["477932", "427714", "431417", "458450", "475791", "477714", "477964", "479087", "419540", "426101", "428905", "428906", "458411", "458443", "415482"],
"last_digits": "7819"
}

def serialisation_to_json(filename: str, key: bytes)->None:
    '''
    str сериализуется в json файл

    Args:
        filename (str): имя файла в который сериализуется str
        key (bytes): объект, который сериализуется в json
    '''
    try:
        with open(filename, "w") as f:
            json.dump(list(key), f)
    except FileNotFoundError:
        logging.error(f"{filename} not found")



initial = {"hash": "f56ab81d14e7c55304dff878c3f61f2d96c8ef1f56aff163320e67df",    
"first_digits":["477932","477932","431417","458450","475791","477714","477964","479087","419540","426101","428905","428906","458411","458443","415482"],
"last_digits":"7819"}

#initial = {"hash": "0b08d71bd3e26721ff32542069442d82811bff4a1e61134dfeedc14848cd0e39",    
#"first_digits":["480086","480087","487415","487416","487417","489354","424917","427326","430643","424976"],
#"last_digits":"0956"}
def luhn(number: int)->bool:
    """
    Проверяет номер на корректность алгоритмом Луна

    args:
    number(int): сгенерированные цифры карты
    return:
    (bool): True, если все сошлось, иначе - False
    """
    number = str(f'{initial["first_digits"]}{number}{initial["last_digits"]}')
    res = 0
    for i, n in enumerate(number):
        if i % 2 == 0 and i < 15:
            res += n if n < 10 else str(n)[0] + str(n)[1]
        else:
            res += n
    res = 0 if res % 10 == 0 else 10 - res % 10
    return int(res) == int((initial["last_digits"])[-1])


def checking_hash(bin: int, number: int)->int:
    """
    Сравнивает хэш полученной карты с уже существующим

    args:
    number(int): сгенерированные цифры карты
    return:
    (int): номер, если хэш совпал, иначе False
    """
    if hashlib.sha3_224(f'{bin}{number}{initial["last_digits"]}'.encode()).hexdigest() == f'{initial["hash"]}':
        return number
    return number if hashlib.sha3_224(f'{bin}{number}{initial["last_digits"]}'.encode()).hexdigest() == f'{initial["hash"]}' else False