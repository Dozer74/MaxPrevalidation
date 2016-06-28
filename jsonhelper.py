# coding=utf-8
import json
from paramsinfo import ParamsInfo, ParamValue, ValidateType
from enum import Enum


class ValidateParamResult(Enum):
    DONE = 0
    CHANGED = 1
    REQUEST_CHANGE = 2
    USER_CHANGE = 3


class JsonParser:
    @staticmethod
    def __to_sec(s):
        l = s.split(':')
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    @staticmethod
    def parse(path):
        """ Выполняет чтение json фалйа и его преобразование в ParamsInfo """
        with open(path) as data_file:
            data = json.load(data_file)['Corona']['Scene']['General Settings']['Progressive rendering limits']
        for key in data:
            if key.lower().find('pass') != -1:
                pass_lim = ParamValue(int(data[key]['value']), data[key]['operator'])
            elif key.lower().find('noise') != -1:
                noise_lim = ParamValue(int(data[key]['value']), data[key]['operator'])
            elif key.lower().find('time') != -1:
                time_lim = ParamValue(JsonParser.__to_sec(data[key]['value']), data[key]['operator'])
            elif key.lower().find('validation') != -1:
                val_type = ValidateType[data[key]]
            else:
                raise ValueError('недопустимый ключ!')
        return ParamsInfo(pass_lim, noise_lim, time_lim, val_type)

    @staticmethod
    def write(path, result):
        with open(path, 'w') as outfile:
            json.dump({'ValidateParamResult': result.name}, outfile)
