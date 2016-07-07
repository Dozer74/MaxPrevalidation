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
        if s == '0':  # просто 0 -- допустимое значение
            return 0
        l = s.split(':')
        if len(l) != 3:  # все остальные должны быть в формате HH:MM:SS!
            raise ValueError('Bad time format!')
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    @staticmethod
    def __check_structure(item):
        return {'Corona', 'Scene', 'General Settings'}.issubset(item)

    @staticmethod
    def __get_path_to_limits(element, dic, path):
        """ Возвращает иерархический список ключей до вхождения element в dic"""
        if element in dic:
            path = path + element
            return [unicode(string) for string in path.split('.')]
        for k, v in dic.items():
            if isinstance(v, dict):
                item = JsonParser.__get_path_to_limits(element, v, path + k + '.')
                # убедимся, что найденый путь содержит требуюмую структуру
                if item is not None and JsonParser.__check_structure(item):
                    return item


    @staticmethod
    def __parse_content(data, name):
        for string in name:
            data = data[string]

        # некоторых данных может не быть. Зададим значения по умолчанию
        # TODO выяснить, какие значения устанавливать по умолчанию
        pass_lim = noise_lim = time_lim = ParamValue(value=0, operator='>')
        val_type = ValidateType['ALL_TRUE']

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
                raise ValueError('Unknown key!')
        return Content(pass_lim, noise_lim, time_lim, val_type)

    @staticmethod
    def parse(path):
        """ Выполняет чтение json фалйа и его преобразование в ParamsInfo """
        with open(path) as data_file:
            dic = json.load(data_file)
        full_name = JsonParser.__get_path_to_limits('Progressive rendering limits', dic, '')
        limits = JsonParser.__parse_content(dic, full_name)

        # сохраняем в названии только часть пути, начинающуюся с Corona
        short_name = full_name[full_name.index('Corona'):]
        return ParamInfo(0, 0, short_name, limits)

    @staticmethod
    def write(path, result):
        with open(path, 'w') as outfile:
            json.dump({'ValidateParamResult': result.name}, outfile)
