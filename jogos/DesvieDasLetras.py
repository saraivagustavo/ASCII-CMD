from colorama import Fore
from random import choice, randrange
from string import ascii_letters as alfabeto
from time import sleep
from os import system
from keyboard import is_pressed

def todos_valores_iguais(lista):
    return len(set(lista)) == 1

class DesvieDasLetras:
    def __init__(self, I=20, J=10):
        self.I, self.J = I, J

        self.jogador = Jogador(3, f"{Fore.GREEN}0", (I-1, J//2))
        self.tela_fundo = " "
        self.mapa = [[self.tela_fundo for _ in range(J)] for _ in range(I)]

        self.VELOCIDADE_JOGADOR = 1
        self.FREQUENCIA_OBSTACULO = 3
        self.contador_obstaculo = 0

        self.posicoes_jogador = [] 

        self.score = 0

    def mostrar_mapa(self, tab=0):
        tab = tab * " "
        cor_margem=Fore.YELLOW

        for i in self.mapa:
            print(f"{cor_margem}{tab}|{f''.join(i)}", end=f"{cor_margem}|\n")
        print(f"""{Fore.LIGHTMAGENTA_EX}VIDA: {Fore.CYAN}{self.jogador.vida}
{Fore.LIGHTMAGENTA_EX}SCORE: {Fore.CYAN}{self.score}""")

    def mover_obstaculos(self):
        for i in range(self.I-1, 0, -1):
            aux = self.mapa[i]
            self.mapa[i] = self.mapa[i-1]
            self.mapa[i-1] = aux

    def gerar_obstaculo(self):
        obstaculo = randrange(0, self.J)

        self.posicoes_jogador.append(self.jogador.y)
        qtd_posicoes = len(self.posicoes_jogador)

        if todos_valores_iguais(self.posicoes_jogador) and qtd_posicoes == 3:
            self.posicoes_jogador.clear()
            obstaculo = self.jogador.y

        if qtd_posicoes == 3:
            self.posicoes_jogador.clear()
        
        self.mapa[0][obstaculo] = f"{Fore.RED}{choice(alfabeto)}"

    def update(self):
        system("cls")

    def mover_jogador(self, direcao):
        jg = self.jogador
        if direcao == 'd':
            jg.x += self.VELOCIDADE_JOGADOR
        elif direcao == 'a':
            jg.x -= self.VELOCIDADE_JOGADOR

        jg.x = max(0, min(jg.x, self.J-1))

    def verificar_teclas_pressionadas(self):
        if is_pressed('d'):
            self.mover_jogador('d')
        elif is_pressed('a'):
            self.mover_jogador('a')

    def verificar_colisao(self):
        return self.mapa[self.jogador.y-1][int(self.jogador.x)] != self.tela_fundo
    
    def verificar_morte(self):
        return self.jogador.vida == 0
            
    def main(self):
        jg = self.jogador

        while True:
            self.contador_obstaculo += 1
            self.score += 10
            
            if self.contador_obstaculo % self.FREQUENCIA_OBSTACULO == 0:
                self.gerar_obstaculo()

            self.mapa[jg.y][int(jg.x)] = f"{Fore.GREEN}{jg}"
           
            self.mostrar_mapa()

            self.verificar_teclas_pressionadas()

            if self.verificar_colisao():
                jg.vida -= 1

                if self.verificar_morte():
                    print(f"{Fore.RED}\nMORREU!{Fore.RESET}")
                    break
          
            self.mapa[jg.y] = [self.tela_fundo] * self.J

            self.mover_obstaculos()

            sleep(max(0, .1 - int(self.score/500)/200))
            self.update()

class Jogador:
    def __init__(self, vida, c, pos):
        self.vida = vida
        self.c = c
        self.pos = pos
        self.y = pos[0]
        self.x = pos[1]

    def __str__(self):
        return self.c

if __name__ == "__main__":
    try:
        game = DesvieDasLetras(20,20)
        game.main()
    except Exception as e:
        print(Fore.RESET, e)
