from tokenn import token
from scanner import scanner, tab
import semantico
import pandas as pd

tabelaTransicao = pd.read_csv('tabelaAtualizada.csv')
regrasGramatica = pd.read_csv('regrasGramatica.csv')

def rodar(arquivoTeste):
    linha = 0
    coluna = 0
    estado = 0
    pilha = [0]
    pilhaAux = []
    flagS = True
    tokenObtido = scanner(arquivoTeste,linha,coluna)
 
    while linha+1 < len(arquivoTeste):

        a = tokenObtido[0].classe

        regra = tabelaTransicao[a].values[estado]
        if regra[0] == 'S':
            
            estado = int(regra[1:])
            pilha.append(estado)

            linha = tokenObtido[1] 
            coluna = tokenObtido[2]
            tokenObtido = scanner(arquivoTeste,linha,coluna)

            if tokenObtido[0].classe in ['ID','LIT','NUM','OPM','OPR']:
                pilhaAux.append(tokenObtido[0])

        elif regra[0] == 'R':
            
            Beta = regrasGramatica['B'].values[int(regra[1:]) - 1]
            Alfa = regrasGramatica['A'].values[int(regra[1:]) - 1]

            BetaL = len(str.split(Beta,','))

            pilha = pilha[:len(pilha)-BetaL] 

            estado = int(tabelaTransicao[Alfa].values[pilha[-1]])
            pilha.append(estado)
  
            print(f'{Alfa} -> {Beta}')
            pilhaAux = semantico.semantico(int(regra[1:]),pilhaAux,tab, linha, coluna, flagS)
        elif regra == 'ACC':
            break
        
        else:
            flagS = False
            esp = str.split(regra[2:],sep='-')
            print("ERRO SINTÁTICO")
            print("ERRO: esperava-se", esp, '-', "e foi encontrado (", tokenObtido[0].lexema, ")", "- Linha:", linha+1, "/ Coluna:", coluna, ".")     
            
            flag = phraseLevel(esp,linha,coluna,a)
            
            if flag == -1:
                linha = tokenObtido[1]
                coluna = tokenObtido[2]
                tokenObtido = panic(arquivoTeste,linha,coluna,esp)
            else:
                tokenObtido = flag
    
    semantico.gerarArquivo()

def panic(arquivoTeste,linha,coluna,esp):
    tokenObtido = scanner(arquivoTeste,linha,coluna)
    linha = tokenObtido[1]
    coluna = tokenObtido[2]
    
    a = tokenObtido[0].classe
  
    while (a != 'PT_V' and a !='EOF'):
        if a in esp:
            return tokenObtido
        else:
            tokenObtido = scanner(arquivoTeste,linha,coluna)
            linha = tokenObtido[1]
            coluna = tokenObtido[2]
            a = tokenObtido[0].classe
    return tokenObtido
     
def phraseLevel(esp,linha,coluna,a):
    if 'PT_V' in esp:
        tokenRegistrado = token('PT_V',';','NULO')
        return [tokenRegistrado,linha,coluna]
    
    elif 'VIR' in esp:
        tokenRegistrado = token('PT_V',',','NULO')
        return [tokenRegistrado,linha,coluna]
    
    elif 'inicio' in esp:
        tokenRegistrado = token('inicio','inicio','inicio')
        return [tokenRegistrado,linha,coluna]
    
    elif 'fim' in esp and a == 'EOF':
        tokenRegistrado = token("fim","fim","fim")
        return [tokenRegistrado,linha,coluna]
    
    return -1