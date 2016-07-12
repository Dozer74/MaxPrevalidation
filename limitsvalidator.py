# coding=utf-8
from content import ValidateType
from jsonhelper import ValidateParamResult


class LimitsValidator:
    @staticmethod
    def __isValid(jsonLimit, currLimit):
        valid = False
        if jsonLimit[1] == ">" and currLimit > jsonLimit[0] or \
           jsonLimit[1] == "=" and currLimit == jsonLimit[0] or \
           jsonLimit[1] == "<" and currLimit < jsonLimit[0]:
                valid = True
        return valid

    @staticmethod
    def validate(jsonData, currLimits):
        validCounter = 0
        validCounter += int(LimitsValidator.__isValid(jsonData.pass_limit, currLimits[0]))
        validCounter += int(LimitsValidator.__isValid(jsonData.noise_limit, currLimits[1]))
        validCounter += int(LimitsValidator.__isValid(jsonData.time_limit, currLimits[2]))

        if validCounter == 3 and jsonData.validation_type == ValidateType['ALL_TRUE'] or \
           validCounter >= 2 and jsonData.validation_type == ValidateType['LEAST_TWO'] or \
           validCounter >= 1 and jsonData.validation_type == ValidateType['LEAST_ONE'] or \
           validCounter == 0 and jsonData.validation_type == ValidateType['ALL_FALSE']:
                return ValidateParamResult(0)

        return ValidateParamResult(3)
