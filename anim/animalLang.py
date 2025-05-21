from os import system
from time import sleep

class Animal:
    def __init__(self, code) -> None:
        self.code = code.replace(" ", "")
        self.delay = 0.5
        self.frames = [ 
        """

s                   _____
s                  / o 0 |
s                 /  . __|
s _______________/    /
s|                   /
s|                  /
s|      ___       _/
s \\    /   \\     /
s  |  |     |   |
s  |  |      \\--/
s  \\--/ 

        """,

        """

s                   _____
s                  / 0 o |
s                 /  . __|
s _______________/    /
s|                   /
s|                  /
s|      ___       _/
s \\    /   \\     /
s  |  |     |   |
s  \\--/     |   |
s            \\--/
        
        """
        ]
    
    def interpret(self):
        s = 0
        i = 0

        for c in self.code:
            
            print(self.frames[i].replace("s", " "*s))
            sleep(self.delay)
            self.clear()

            i = 1 if i == 0 else 0
            s += 1 if c == ">" else -1 if c == "<" else 0

        print(self.frames[i].replace("s", " "*s))
        
    def clear(self):
        system("cls || clear")


code = ">>>><<>>"

bixo = Animal(code)

bixo.interpret()
