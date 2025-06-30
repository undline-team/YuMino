from colorama import Fore, Style, init
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

full = """
            /\\___/\\
            )     (
           =\\     /=
             )   (
            /     \\
            )     (
           /       \\
           \\       /
            \\__ __/
               ))
              //
             ((
              \\)
     YuMino || v 
"""
version = "1.0 alpha"
def screen():
    pink_cat = Fore.MAGENTA + full + Style.RESET_ALL
    text_to_replace = "     YuMino || v "  # Определите строку для замены
    green_text = pink_cat.replace(text_to_replace, Fore.GREEN + text_to_replace + version + Style.RESET_ALL)
    clear_console()
    print(green_text)