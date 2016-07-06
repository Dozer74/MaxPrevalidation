import os

from jsonhelper import JsonParser
from maxhelper import MaxHelper
from limitsvalidator import LimitsValidator
from subprocess import Popen


dirpath = os.path.dirname(__file__)

data = JsonParser.parse(os.path.join(dirpath, 'data.json'))
currLimits = MaxHelper.getValue()
if currLimits is None:
    print("Can't get limits!")
else:
    res = LimitsValidator.validate(data.content, currLimits)
    JsonParser.write(os.path.join(dirpath, 'result.json'), res)  # результат сохранен, можно закрываться

killer_path = os.path.join(dirpath, 'maxkiller.py')
Popen([r'C:\Program Files\Autodesk\3ds Max 2015\python\python.exe', killer_path])  # на всякий случай, запускаем скрипт, который добьёт макс при необходимости
MaxHelper.close_max()  # просим макс закрыться по-хорошему

# только для теста:
# import time
# time.sleep(900)  # эмитируем зависание макса
