import hashlib
import logging
import json
from matplotlib import pyplot as plt
import multiprocessing as mp
from functools import partial
from time import time

cores = mp.cpu_count()

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

def luhn(init: dict)->bool:
    """
    Проверяет номер на корректность алгоритмом Луна
    args:
        init(dict): входные данные
    return:
        (bool): True, если все сошлось, иначе - False
    """
    res = 0
    try:
        with open(init["found_card"]) as f:
            data = json.load(f)
    except FileNotFoundError:
          logging.error(f"{init['found_card']} not found")
    logging.info(data)
    number = str(data["card_number"])
    number = list(map(int, number))
    if len(number) != 16:
         logging.info("Номер не корректен")
         data["luhn_check"] = "no result"
    else:
        last = number[15]
        number.pop()
        for n in number:
            i = n * 2
            if i > 9:
                res += i % 10 + i // 10
            else:
                res += i

        res = 10 - res % 10
        logging.info(res)
        if res == last:
            logging.info("Карточка корректна")
            data["luhn_check"] = "true"
        else:
            logging.info("Карточка не корректна")
            data["luhn_check"] = "false"
    logging.info(f"Результат сохранен по пути {init['found_card']}")
    try:
        with open(init["found_card"], 'w') as f:
            json.dump(data, f)
    except FileNotFoundError:
          logging.error(f"{init['found_card']} not found")

def search(initial: dict, processes: int)->None:
    flag = 0
    with mp.Pool(processes) as p:
        for b in initial["first_digits"]:
            logging.info(b)

            for result in p.map(partial(checking_hash, int(b), initial), range(1000000)):
                if result:
                    logging.info('we have found ' + result + ' and have terminated pool')
                    p.terminate()
                    flag = 1
                    logging.info('Найденная карта лежит по пути ' + initial["found_card"])
                    data = {}
                    data["card_number"] = f"{result}"
                    data["luhn_check"] = "no result"
                    try:
                        with open(initial["found_card"], 'w') as f:
                                json.dump(data, f)
                    except FileNotFoundError:
                        logging.error(f"{initial['found_card']} not found")
                    break
            if flag == 1:
                break
    if flag == 0:
        logging.info('Карта не найдена')    

def checking_hash(bin: int, initial:dict, number: int)->int:
    """
    Сравнивает хэш полученной карты с уже существующим

    args:
    number(int): сгенерированные цифры карты
    return:
    (int): номер, если хэш совпал, иначе False
    """
    if hashlib.sha3_224(f'{bin}{number:06d}{initial["last_digits"]}'.encode()).hexdigest() == initial["hash"]:
        return f'{bin}{number:06d}{initial["last_digits"]}'
    
def save_stat(initial: dict):
    """
    Сохраняет зависимость времени поиска коллизии хэша от кол-ва процессов
    args:
        init(dict): входные данные
    """
    time_ = []
    for i in range(int(initial["processes_amount"])):
            start = time()
            logging.info(f'количество процессов: {i+1}\n')
            search(initial, i+1)
            time_.append(time()-start)
    fig=plt.figure(figsize=(30, 17))
    plt.ylabel('Время')
    plt.xlabel('процессы')
    plt.title('зависимость времени от кол-ва процессов')
    plt.plot(list(x+1 for x in range(int(initial["processes_amount"]))),time_) 
    plt.savefig(f'{initial["stat_path"]}')
    logging.info(f'Зависимость времени от процессов сохранена по пути {initial["stat_path"]}\n')