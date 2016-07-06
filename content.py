from collections import namedtuple

from enum import Enum

ValidateType = Enum('ValidateType', 'ALL_TRUE ALL_FALSE LEAST_ONE LEAST_TWO')
ParamValue = namedtuple('ParamValue', ['value', 'operator'])


class Content:
    def __init__(self, pass_lim, noise_lim, time_lim, val_type):
        self.pass_limit = pass_lim
        self.noise_limit = noise_lim
        self.time_limit = time_lim
        self.validation_type = val_type
