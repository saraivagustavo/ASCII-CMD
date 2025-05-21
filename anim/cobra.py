from time import sleep
from os import system
from colorama import Fore

SYM = Fore.GREEN + "o" + Fore.RESET
TABLE_I = 20
TABLE_J = 20
TABLE = [ ["." for _ in range(TABLE_J)] for _ in range(TABLE_I) ]
DELAY = 1
COBRA = [[i, 6] for i in range(5) ]

def set_delay(delay):
    global DELAY
    DELAY = delay

def clear():
    system("cls || clear")

def clear_table():
    for i in range(TABLE_I):
        for j in range(TABLE_J):
            TABLE[i][j] = "."

def update_table():
    for i, j in COBRA:
       TABLE[i][j] = SYM

def tab():
    for i in TABLE: print(*i)

def draw_cobra(func):
    
    def wrapper():
        func()
        clear_table()
        update_table()
        sleep(DELAY)
        clear()
        tab()

    return wrapper

@draw_cobra
def direita():
    if COBRA[-1][1]+1 != TABLE_J and COBRA[-1][1]+1 not in COBRA:
        COBRA.append([COBRA[-1][0], COBRA[-1][1] +1])
        del COBRA[0]

@draw_cobra
def esquerda():
    if COBRA[-1][1] != 0 and COBRA[-1][1]-1 not in COBRA:
        COBRA.append([COBRA[-1][0], COBRA[-1][1] -1])
        del COBRA[0]

@draw_cobra
def cima():
    if COBRA[-1][0] != 0 and COBRA[-1][0]-1 not in COBRA:
        COBRA.append([COBRA[-1][0] -1, COBRA[-1][1]])
        del COBRA[0]
   
@draw_cobra
def baixo():
    if COBRA[-1][0]+1 != TABLE_I and COBRA[-1][0]+1 not in COBRA:
        COBRA.append([COBRA[-1][0] +1, COBRA[-1][1]])
        del COBRA[0]

def main():
    
    movs = [ 
        (esquerda, 4), (baixo, 4),
        (direita, 4), (cima, 4),
        direita
           ]

    set_delay(.5)
    update_table()
    tab()
    
    for mov in movs:
        if isinstance(mov, tuple):
            mv, qtd = mov
        else:
            mv, qtd = mov, 1
        for _ in range(qtd):
            mv()
        

if __name__ == "__main__":
    main()
