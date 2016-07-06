# coding=utf-8
import json
from paraminfo import ParamInfo
from content import Content, ParamValue, ValidateType
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
    def __get_path_to_limits(element, dic, path):
        """ Возвращает иерархический список ключей до первого вхождения element в dic"""
        if element in dic:
            path = path + element
            return [unicode(string) for string in path.split('.')]
        for key in dic:
            if isinstance(dic[key], dict):
                return JsonParser.__get_path_to_limits(element, dic[key], path + key + '.')

    @staticmethod
    def parse(path):
        """ Выполняет чтение json фалйа и его преобразование в ParamsInfo """
        with open(path) as data_file:
            dic = json.load(data_file)
        name = JsonParser.__get_path_to_limits('Progressive rendering limits', dic, '')
        limits = JsonParser.__parse_content(dic, name)
        return ParamInfo(0, 0, name, limits)

    @staticmethod
    def __parse_content(data, name):
        for string in name:
            data = data[string]
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
        return Content(pass_lim, noise_lim, time_lim, val_type)

    @staticmethod
    def write(path, result):
        with open(path, 'w') as outfile:
            json.dump({'ValidateParamResult': result.name}, outfile)
