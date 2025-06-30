import datetime
import colorama
import inspect
import os
import traceback
from colorama import Fore, Back, Style, init

init()

class YuConsole:

    def __init__(self, name=""):
        self.name = name

    def _format_message(self, level, message, color):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{Fore.WHITE}{timestamp} {color}[{level}] {self.name} - {message}{Style.RESET_ALL}"

    def log(self, message):
        print(self._format_message("LOG", message, Fore.GREEN))

    def warn(self, message):
        print(self._format_message("WARN", message, Fore.YELLOW))

    def error(self, message, exc_info=None):
        if exc_info is None:
            exc_info = traceback.format_exc()

        error_message = f"{message}\n{exc_info}"
        print(self._format_message("ERROR", error_message, Fore.RED))