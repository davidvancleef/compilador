from tokenn import token
from scanner import scanner
import pandas as pd

regrasGramatica = pd.read_csv('regrasGramatica.csv')
tabelaTransicao = pd.read_csv('tabelaAtualizada.csv')

def rodar(arquivo):
    linha = 0
    coluna = 0
    estado = 0
    pilha = [0]
    tokenObtido = scanner(arquivo,linha,coluna)
 
    while linha+1 < len(arquivo):
        
        linha = tokenObtido[1]
        coluna = tokenObtido[2]
        
        a = tokenObtido[0].classe
        rule = tabelaTransicao[a].values[estado]

        if rule[0] == 'S':
            
            estado = int(rule[1:])
            pilha.append(estado)
            
            tokenObtido = scanner(arquivo,linha,coluna)

        elif rule[0] == 'R':
            
            Beta = regrasGramatica['B'].values[int(rule[1:]) - 1]
            Alfa = regrasGramatica['A'].values[int(rule[1:]) - 1]
            
            BetaL = len(str.split(Beta,','))

            pilha = pilha[:len(pilha)-BetaL]

            estado = int(tabelaTransicao[Alfa].values[pilha[-1]])
            pilha.append(estado)
            
            print(f'{Alfa} -> {Beta}')
            
        elif rule == 'ACC':
            break
        
        else:
            print("Erro sintatico: esperava-se", str.split(rule[2:], '-'), ", porem foi encontrado (", tokenObtido[0].lexema, ")", "- Linha:", linha+1, "/ coluna:", coluna)

            tokenObtido = scanner(arquivo,linha,coluna)
            linha = tokenObtido[1]
            coluna = tokenObtido[2]
            
            while (a != 'PT_V' and a !='EOF'):  

                a = tokenObtido[0].classe
                rule = tabelaTransicao[a].values[estado]

                if rule[0] == 'S':
                    estado = int(rule[1:])
                    pilha.append(estado)
                    tokenObtido = scanner(arquivo,linha,coluna)

                elif rule[0] == 'R':
                    Beta = regrasGramatica['B'].values[int(rule[1:]) - 1]
                    Alfa = regrasGramatica['A'].values[int(rule[1:]) - 1]
                    BetaL = len(str.split(Beta,','))
                    pilha = pilha[:len(pilha)-BetaL]
                    estado = int(tabelaTransicao[Alfa].values[pilha[-1]])
                    pilha.append(estado)

                elif rule == 'ACC':
                    break
                
                else:
                    print("Erro sintatico: era esperado ", str.split(rule[2:], '-'), ", porem foi encontrado (", tokenObtido[0].lexema(), ")", "- Linha:", linha+1, "/ coluna:", coluna)

                    tokenObtido = scanner(arquivo,linha,coluna)
                    linha = tokenObtido[1]
                    coluna = tokenObtido[2]
