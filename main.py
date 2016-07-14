import os

from jsonhelper import JsonParser
from maxhelper import MaxHelper
from limitsvalidator import LimitsValidator
from subprocess import Popen


dirpath = os.path.dirname(__file__)

param_info = JsonParser.parse(os.path.join(dirpath, 'data.json'))
currLimits = MaxHelper.getValue()
if currLimits is None:
    print("Can't get limits!")
else:
    res = LimitsValidator.validate(param_info.content, currLimits)
    JsonParser.write(os.path.join(dirpath, 'result.json'), res)  # результат сохранен, можно закрываться


python_path = r'C:\Program Files\Autodesk\3ds Max 2014\python\python.exe'
killer_path = os.path.join(dirpath, 'maxkiller.py')
pid = os.getpid() # получаем pid текущего экземпляра 3ds max'a. Остальные трогать не будем
cmd = '"{}" "{}" {}'.format(python_path, killer_path, pid) # если не работает, поставить python_path первым аргументом
Popen(cmd, shell=True)
MaxHelper.close_max()  # просим макс закрыться по-хорошему
