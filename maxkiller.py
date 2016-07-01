# coding=utf-8
import psutil
import time

PROCNAME = "3dsmax.exe"

time.sleep(5)  # даём шанс максу самому завершить работу
for proc in psutil.process_iter():
    if proc.name() == PROCNAME:
        proc.kill()  # если не успел (завис) - находим и убиваем его!
