import logging
import datetime
import os.path

log_directory = "logs"
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Handler pre zapis do suboru
file_handler = logging.FileHandler(
    log_directory + '/' + datetime.datetime.now().strftime('%Y-%m-%d (%H_%M_%S)') + '.log',
    mode='w',
    encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Handler pre vystup na konzolu
console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)  # nastavenie je v my_keyboard.py

# Formatovanie sprav
formatter = logging.Formatter(
    '%(asctime)s,%(msecs)03d  [%(filename)s(%(lineno)06d)]\n\t[%(levelname).3s]  %(message)s',
    datefmt='%Y-%m-%d_%H:%M:%S')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Pridanie handlerov k loggerovi
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info('🤖 | ahoj, som (b)Logger a fungujem')  # ℹ️
