from jsonhelper import JsonParser
from maxhelper import MaxHelper
from limitsvalidator import LimitsValidator

data = JsonParser.parse('data.json')
currLimits = MaxHelper.getValue()
res = LimitsValidator.validate(data, currLimits)
JsonParser.write('result.json', res)
