# coding=utf-8
import psutil
import time
import sys

pid = int(sys.argv[1])  # убиваем только процесс с указанным pid
time.sleep(5)  # даём шанс максу самому завершить работу
proc = [p for p in psutil.process_iter() if p.pid == pid][0]
proc.kill()  # если не успел (завис) - находим и убиваем его!
