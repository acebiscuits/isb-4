import hashlib
import argparse
import json
import multiprocessing as mp
from random import randint
from useful_funcs import checking_hash, luhn
from functools import partial
import logging
from tqdm import tqdm

cores = mp.cpu_count()

#initial = {"hash": "0b08d71bd3e26721ff32542069442d82811bff4a1e61134dfeedc14848cd0e39",    
#"first_digits":["480086","480087","487415","487416","487417","489354","424917","427326","430643","424976"],
#"last_digits":"0956"}
initial = {"hash": "f56ab81d14e7c55304dff878c3f61f2d96c8ef1f56aff163320e67df",    
"first_digits":["477932","477932","431417","458450","475791","477714","477964","479087","419540","426101","428905","428906","458411","458443","415482"],
"last_digits":"7819"}
def search(initial: dict)->None:
    flag = 0
    with mp.Pool(processes=cores) as p:
        for b in initial["first_digits"]:
            for result in p.map(partial(checking_hash, int(b)), range(100000, 1000000)):
                if result:
                    print(f'we have found {result} and have terminated pool')
                    p.terminate()
                    flag = 1
                    break
            if flag == 1:
                break

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--settings_path',default='settings.json',help='Путь к json файлу с данными, default = files\\settings.json', action='store')
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-sch','--search',help='Поиск подходящих номеров', action="store_true")
    group.add_argument('-ch','--check',help='Проверка на реальную карту', action="store_true")
    group.add_argument('-stat','--statistic',help='Замер времени в зависимости от числа потоков', action="store_true")
    args = parser.parse_args()
    logging.info(args)
    settings_path = args.settings_path

    #try:
        #with open(settings_path) as jf:
          #  initial = json.load(jf)
    #except FileNotFoundError:
   #     logging.error(f"{settings_path} not found")

    mode = (args.search, args.check, args.statistic)
    logging.info(mode)

    match mode:
        case (True, False, False):
            #with tqdm(total=4) as pbar:
            logging.info('Generation keys\n')
            search(initial)#, pbar)
        case (False, True, False):
            with tqdm(total=2) as pbar:
                logging.info('Encryption the file\n')
                #encrypting(settings, pbar)
        case (False, False, True):
            with tqdm(total=2) as pbar:
                logging.info('Decryption the file\n')
                #decrypting(settings, pbar)
        case _:
            logging.error("wrong mode")