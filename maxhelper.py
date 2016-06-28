# coding=utf-8
import sys
import imp

try:
    imp.find_module('MaxPlus')
except ImportError:
    pathTo3dsMax = r'C:\Program Files\Autodesk\3ds Max 2015'
    sys.path.append(pathTo3dsMax)

import MaxPlus


class MaxHelper:
    scriptPassLimit = 'renderers.current.progressive_passLimit'
    scriptNoiseLimit = 'renderers.current.adaptivity_targetError'
    scriptTimeLimit = 'renderers.current.progressive_timeLimit'

    @classmethod
    def getValue(cls):
        """
        Получает значения лимитов Corona Renderer'a
        Возвращает кортеж PassLimit, NoiseLimit, TimeLimit(в сек)
        """
        return (MaxPlus.Core.EvalMAXScript(cls.scriptPassLimit).GetInt64(),
                MaxPlus.Core.EvalMAXScript(cls.scriptNoiseLimit).GetFloat(),
                MaxPlus.Core.EvalMAXScript(cls.scriptTimeLimit).GetInt64() / 1000.0)

    @classmethod
    def setValue(cls, passLim=-1, noiseLim=-1.0, timeLim=-1):
        """ Устанавливает значения лимитов Corona Renderer'a """
        maxscript = ''
        if int(passLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptPassLimit, passLim)
        if float(noiseLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptNoiseLimit, noiseLim)
        if int(timeLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptTimeLimit, int(timeLim) * 1000)

        if maxscript:
            MaxPlus.Core.EvalMAXScript(maxscript)
