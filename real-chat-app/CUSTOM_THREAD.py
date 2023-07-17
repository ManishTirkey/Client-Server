# Python program using
# traces to kill threads

import sys
import trace
import threading
import time


class thread_with_trace(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
            return self.localtrace

    def kill(self):
        self.killed = True


def Func():
    i = 0
    while True:
        print(f"h {i}")
        i = i+1


if __name__ == '__main__':
    threa = thread_with_trace(target=Func)
    threa.start()

    time.sleep(2)
    print("going to kill")
    threa.kill()
    print(threa.isAlive())
    if not threa.isAlive():
        print("thread is killed")
        print(threa.isAlive())
        print(not threa.isAlive())

