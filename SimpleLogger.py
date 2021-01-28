from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

timestampFormat ='%Y-%m-%d,%H:%M:%S:%f'


class SimpleLogger():
    def __init__(self, verbose, loggerName):
        self.verbose = verbose
        self.save = False
        self.fileName = f"{loggerName}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.fileHandle = None
        return

    def log(self, s, messageType = "INFO", forcePrint = False):
        if self.verbose or forcePrint:

            timeStamp = datetime.now().strftime(timestampFormat)

            # Let's use some ANSI escape sequences to color the texts
            if messageType == "WARN":
                print(f"[{timeStamp}] [{bcolors.WARNING}{messageType.rjust(5)}{bcolors.ENDC}] {s}")
            elif messageType == "DEBUG":
                print(f"[{timeStamp}] [{bcolors.WARNING}{messageType.rjust(5)}{bcolors.ENDC}] {s}")
            elif messageType == "ERROR":
                print(f"[{timeStamp}] [{bcolors.FAIL}{messageType.rjust(5)}{bcolors.ENDC}] {s}")
            elif messageType == "OK":
                print(f"[{timeStamp}] [{bcolors.OKGREEN}{messageType.rjust(5)}{bcolors.ENDC}] {s}")
            else:    
                print(f"[{timeStamp}] [{messageType.rjust(5)}] {s}")

            if self.save:
                if self.fileHandle == None:
                    self.fileHandle = open(self.fileName, "a")

                self.fileHandle.write(f"[{timeStamp}] [{messageType.rjust(5)}] {s}\n")
                self.fileHandle.close()
                self.fileHandle = None
