from colorama import Fore
from random import choice, randrange
from time import sleep
from os import system

class JogoDaMemoria:
    ocult_sym = "O"

    def __init__(self):

        self.__author__ = "Marcuss42"
        self.symbols = "#", "%", "&", "@", "!" # 249 simbolos no máximo
        
        self.count_sym = {s:0 for s in self.symbols}
        self.len_symbols = len(self.symbols)
        self.pares = 2
        self.I, self.J = self.pares*2, self.len_symbols
        self.tabuleiro = [[Sym(self.random_sym()) for j in range(self.J)] for i in range(self.I) ]

        self.selecionar = []

        for i in range(self.I):
            for j in range(self.J):
                self.selecionar.append((i, j))
                

    @staticmethod
    def valid_int_input(text = '', r = None):
        while True:
            try:
                inp = int(input(text))
            except ValueError:
                continue
            if r:
                if r[0] <= inp <= r[1]:
                    return inp
            else:
                return inp

    @staticmethod
    def clear():
        system("cls || clear")   

    def embaralhar(self):
        matriz = self.tabuleiro
        I, J = len(matriz), len(matriz[0])
        pos = []
        for i in range(I):
            for j in range(J):
                while True:
                    pi, pj = randrange(0, I), randrange(0, J)
                    if (i, j) != (pi, pj) not in pos:
                        pos.append((pi, pj))
                        break
        
        length = len(pos)
        for n in range(length-1):
            i, j = pos[n][0], pos[n][1]
            pi, pj = pos[n+1][0], pos[n+1][1]
            
            aux = matriz[i][j]
            matriz[i][j] = matriz[pi][pj]
            matriz[pi][pj] = aux

    def menu(self):
        titulo = f"""{Fore.GREEN}
░░░░░██╗░█████╗░░██████╗░░█████╗░  ██████╗░░█████╗░  ███╗░░░███╗███████╗███╗░░░███╗░█████╗░██████╗░██╗░█████╗░
░░░░░██║██╔══██╗██╔════╝░██╔══██╗  ██╔══██╗██╔══██╗  ████╗░████║██╔════╝████╗░████║██╔══██╗██╔══██╗██║██╔══██╗
░░░░░██║██║░░██║██║░░██╗░██║░░██║  ██║░░██║███████║  ██╔████╔██║█████╗░░██╔████╔██║██║░░██║██████╔╝██║███████║
██╗░░██║██║░░██║██║░░╚██╗██║░░██║  ██║░░██║██╔══██║  ██║╚██╔╝██║██╔══╝░░██║╚██╔╝██║██║░░██║██╔══██╗██║██╔══██║
╚█████╔╝╚█████╔╝╚██████╔╝╚█████╔╝  ██████╔╝██║░░██║  ██║░╚═╝░██║███████╗██║░╚═╝░██║╚█████╔╝██║░░██║██║██║░░██║
░╚════╝░░╚════╝░░╚═════╝░░╚════╝░  ╚═════╝░╚═╝░░╚═╝  ╚═╝░░░░░╚═╝╚══════╝╚═╝░░░░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝╚═╝░░╚═╝

                                                                                         {Fore.CYAN}saraivagustavo
""" + Fore.RESET
 
        print(titulo)
    def random_sym(self):
        while True:
            sym = choice(self.symbols)
            sleep(ord(sym)/1000)
            if self.count_sym[sym] < self.I:
                self.count_sym[sym] += 1
                return sym

    def ocult_syms(self, pos_syms):
        for i, j in pos_syms:
            self.tabuleiro[i][j].sym_ocult()

    
    def sym_equals(self, syms):
        sym1 = self.tabuleiro[syms[0][0]][syms[0][1]].sym
        sym2 = self.tabuleiro[syms[1][0]][syms[1][1]].sym
        
        return sym1 == sym2

    def ganhou(self):
        for i in self.tabuleiro:
            for sym in i:
                if not sym.achou:
                    return False
        return True

    def mostrar_tabuleiro(self, line_color = Fore.MAGENTA, 
    colum_color = Fore.LIGHTMAGENTA_EX, num_color = Fore.CYAN, 
    sym_color = Fore.LIGHTBLUE_EX, c1='-', c2='|', tab=0):

        nums = '₀', '₁', '₂', '₃', '₄', '₅', '₆', '₇', '₈', '₉'
        coordenada = 1
        n = len(self.tabuleiro[0])
        tabuleiro = line_color
        

        for linha in self.tabuleiro:
            tabuleiro += line_color + " "*tab + (c1 * n * 4) + f"{c1}\n"
            tabuleiro += " "*tab
            for i in range(coordenada, coordenada+n):
                pos = ''.join(map(lambda i: nums[int(i)], str(i)))
                n_pos = len(pos)
                tabuleiro += f"{colum_color}{c2}{num_color}{pos}{line_color}" + " " * (3-n_pos)
            tabuleiro += f"{colum_color}{c2} \n" + " " * tab
            for sym in linha:
                tabuleiro += f"{colum_color}{c2} {sym_color}{sym}{line_color} "
                coordenada += 1
            tabuleiro += colum_color + c2 + " "*tab + "\n"
            tabuleiro += " "*tab + (f"{c2}   " * (n+1)) + "\n"
        tabuleiro += line_color + " "*tab + (c1 * n * 4) + c1 + Fore.RESET + "\n"
        
        print(tabuleiro)

    def run(self):
        pos_syms = []
        errou = False
        acertou = False
        self.embaralhar()
        while True:
            self.clear()

            if len(pos_syms) == 2 and self.sym_equals(pos_syms): acertou = True
            elif len(pos_syms) == 2: errou = True

            self.menu()
            self.mostrar_tabuleiro(sym_color = Fore.LIGHTBLUE_EX,
                c1 = '█', c2 = '█', tab = 38)

            if errou:   
                errou = False
                sleep(1.5)
                self.ocult_syms(pos_syms)
                pos_syms.clear()
                continue

            elif acertou:
                acertou = False
                i1, j1 = pos_syms[0]
                i2, j2 = pos_syms[1]
                self.tabuleiro[i1][j1].achou = True
                self.tabuleiro[i2][j2].achou = True
                sleep(1.5)
                self.ocult_syms(pos_syms)
                pos_syms.clear()

                if self.ganhou():
                    self.clear()
                    break
            
   
            coord = self.valid_int_input(
                f"{Fore.YELLOW}Selecione {Fore.LIGHTBLACK_EX}(Ex: 3){Fore.WHITE}: {Fore.YELLOW}",
                (0, len(self.selecionar)))
            

            i, j = self.selecionar[coord-1]

            if not self.tabuleiro[i][j].achou:
                if (i, j) not in pos_syms:
                    pos_syms.append((i, j))

            self.tabuleiro[i][j].change()
        
        self.mostrar_tabuleiro(sym_color = Fore.LIGHTBLUE_EX,
                c1 = '█', c2 = '█', tab = 38)
        
        print(Fore.LIGHTGREEN_EX + """

██╗░░░██╗░█████╗░░█████╗░███████╗  ░██████╗░░█████╗░███╗░░██╗██╗░░██╗░█████╗░██╗░░░██╗
██║░░░██║██╔══██╗██╔══██╗██╔════╝  ██╔════╝░██╔══██╗████╗░██║██║░░██║██╔══██╗██║░░░██║
╚██╗░██╔╝██║░░██║██║░░╚═╝█████╗░░  ██║░░██╗░███████║██╔██╗██║███████║██║░░██║██║░░░██║
░╚████╔╝░██║░░██║██║░░██╗██╔══╝░░  ██║░░╚██╗██╔══██║██║╚████║██╔══██║██║░░██║██║░░░██║
░░╚██╔╝░░╚█████╔╝╚█████╔╝███████╗  ╚██████╔╝██║░░██║██║░╚███║██║░░██║╚█████╔╝╚██████╔╝
░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝  ░╚═════╝░╚═╝░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝░╚════╝░░╚═════╝░

                                                                 Obrigado por jogar :)
""" + Fore.RESET)

            

class Sym(JogoDaMemoria):
    def __init__(self, sym):
        self.sym = sym
        self.ocult = True
        self.achou = False

    def change(self):
        if not self.achou:
            self.ocult = not self.ocult

    def sym_ocult(self):
        if not self.achou:
            self.ocult = True

    def __repr__(self):
        return self.ocult_sym if self.ocult else self.sym

if __name__ == "__main__":
    try:
     
        memoria = JogoDaMemoria()
        memoria.run()       
        input("\n\nAperte qualquer tecla para sair: ")
    except:
        print(Fore.RESET)
 
