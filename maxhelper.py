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
    def __set_corona_renderer(cls):
        """ Устанавливает Corona Renderer, если был выбран другой движок """
        scriptSwitchRenderer = '''if (classof renderers.current != Corona_1_4) then(
        renderers.current = Corona_1_4()
    )'''
        try:
            MaxPlus.Core.EvalMAXScript(scriptSwitchRenderer)
            return True
        except:
            return False

    @classmethod
    def getValue(cls):
        """
        Получает значения лимитов Corona Renderer'a
        Возвращает кортеж PassLimit, NoiseLimit, TimeLimit(в сек)
        """
        if not cls.__set_corona_renderer():
            return None

        return (MaxPlus.Core.EvalMAXScript(cls.scriptPassLimit).GetInt64(),
                MaxPlus.Core.EvalMAXScript(cls.scriptNoiseLimit).GetFloat(),
                MaxPlus.Core.EvalMAXScript(cls.scriptTimeLimit).GetInt64() / 1000.0)

    @classmethod
    def setValue(cls, passLim=-1, noiseLim=-1.0, timeLim=-1):
        """ Устанавливает значения лимитов Corona Renderer'a """

        if not cls.__set_corona_renderer():
            return None

        maxscript = ''
        if int(passLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptPassLimit, passLim)
        if float(noiseLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptNoiseLimit, noiseLim)
        if int(timeLim) >= 0:
            maxscript += '{0} = {1}'.format(cls.scriptTimeLimit, int(timeLim) * 1000)

        if maxscript:
            MaxPlus.Core.EvalMAXScript(maxscript)

        return True

    @classmethod
    def close_max(cls):
        MaxPlus.Core.EvalMAXScript("quitMAX(#noPrompt)")
