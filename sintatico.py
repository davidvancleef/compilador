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
    pilhaAux = []  #Talvez seja a pilha semantica!
    flagS = True
    tokenObtido = scanner(arquivoTeste,linha,coluna)
 
    while linha+1 < len(arquivoTeste):
        #print ("Lexema:", tokenObtido[0].lexema, "Classe:" ,tokenObtido[0].classe, "Tipo: ",tokenObtido[0].tipo,".")
        a = tokenObtido[0].classe # Acessa [0] porque nele está o token. Em [1] e [2] estão linha e coluna. Ele acessa especificamente a classe do token.

        regra = tabelaTransicao[a].values[estado] #Usa a classe e o estado atual pra achar a regra correspondente
        if regra[0] == 'S': #Se a classe tornar o nosso estado para um Shift
            
            estado = int(regra[1:]) #Pega o estado para qual deve dar shift
            pilha.append(estado)  #Empilha o estado na pilha

            linha = tokenObtido[1] 
            coluna = tokenObtido[2]
            tokenObtido = scanner(arquivoTeste,linha,coluna) #escaneia proxima linha do arquivo

            if tokenObtido[0].classe in ['ID','LIT','NUM','OPM','OPR']:  #Por que salva especificamente esses?
                pilhaAux.append(tokenObtido[0]) #Pra que serve a pilha auxiliar?

        elif regra[0] == 'R': #se for shift
            
            Beta = regrasGramatica['B'].values[int(regra[1:]) - 1]  #pega as derivacoes
            Alfa = regrasGramatica['A'].values[int(regra[1:]) - 1]  #pega a regra

            BetaL = len(str.split(Beta,',')) #pega o numero de derivacoes da regra, desempilhando

            pilha = pilha[:len(pilha)-BetaL] 

            estado = int(tabelaTransicao[Alfa].values[pilha[-1]]) #empilha GOTO (aparentemente)
            pilha.append(estado)
  
            print(f'{Alfa} -> {Beta}') #Imprime a producao
            pilhaAux = semantico.semantico(int(regra[1:]),pilhaAux,tab, linha, coluna, flagS) #invoca semantico
        elif regra == 'ACC': #parar caso a analise termine
            break
        
        else: #Rotinas de erro.
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
    
    semantico.gerarArquivo() #Faz o semantico anotar tudo armazenado num arquivo

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