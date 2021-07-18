import colorama
import sys
import platform
from os import system

class CMD:
    def __init__(self) -> None:
        pass

    def exit(self, system=False, finished=False, noLog=False):
        if noLog is not True:
            if finished is True:
                print ("[SYSTEM]: Finished")
            else:
                if system is True:
                    print ("[SYSTEM]: Quit")
                else:
                    print ("[USER]: Quit")
        sys.exit(0)

    def clear(self):
        system("clear" if platform.system() == "Linux" else "cls")