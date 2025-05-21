from colorama import Fore
from time import sleep
from random import randint
from os import system

colors = dir(Fore)[:17]
len_colors = len(colors)
tamanho = 10

try:
    i = 0
    chuva = []
    while True:
        chuva.append(f"{getattr(Fore, colors[i])}{' '*randint(1, 150)}chuva\n") #troque a palavra {chuva} por outra palavra 
        print(''.join(chuva[::-1]))
        sleep(.03)
        system("cls || clear")
        i = (i+1) % len_colors

        if len(chuva) == tamanho:
            chuva.pop(0)
except (KeyboardInterrupt, AttributeError):
    print(Fore.RESET)
