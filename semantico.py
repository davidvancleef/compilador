from tabela import tabela
from tokenn import token

cabecalho = "#include <stdio.h>\ntypedef char literal[256];\nvoid main(void)\n{"
str1 = "\t/*-------Variaveis temporarias---------*/\n"
str2 = ""
straux = ""


token_aux = token(None,None,None)
oprd1 = None
oprd2 = None
ld = token(None,None,None)
expr = token(None,None,None)
contadorTemporarias = 0
corretude = True
tabulacao = 1

def semantico(t,a:list,tab: tabela, linha, coluna, corretude1):
    global cabecalho
    global str1
    global str2
    global token_aux
    global oprd1
    global oprd2
    global ld
    global contadorTemporarias
    global corretude
    global tabulacao
    if corretude1 == False:
        corretude = corretude1

    if t == 6: #Coloca ; e pula linha depois de receber com sucesso uma declaracao de variavel
        
        str2 = str2 + ";\n"
    
    if t == 7: #No reduce de declaracao de variaveis, Ex: "literal A;"
        tk = tab.buscaLexema(a[0].lexema) #Token tk procura nome da variavel declarada
        if tk == False: #Caso nao encontadorTemporariasre, 
            return a[1:]
        
        if tk.tipo == 'NULO':
            tab.atualizar(a[0].lexema,token_aux.tipo)
            str2 += f",{a[0].lexema}"
        return a[1:]
        
    if t == 8:
        tk = tab.buscaLexema(a[0].lexema)
        
        if tk == False:
            return a[1:]
        
        if tk.tipo == 'NULO':
            tab.atualizar(a[0].lexema,token_aux.tipo)
            str2 += f"{a[0].lexema}"
            
        else:
            print(f"\nVARIAVEL {tk.lexema} JA DECLARADA ANTERIORMENTE\n")
            corretude = False
                
        return a[1:]
    
    if t == 9:
        token_aux.tipo = "inteiro"
        str2 = tabular(str2, tabulacao)
        str2 += "int " 

    if t == 10:
        token_aux.tipo = "real"
        str2 = tabular(str2, tabulacao)
        str2 += "double "
        
    if t == 11:
        token_aux.tipo = "literal"
        str2 = tabular(str2, tabulacao)
        str2 += "literal "

    if t == 13:
        tk = tab.buscaLexema(a[0].lexema)
        if tk == False:
            print(f"\nERRO SEMANTICO - VARIAVEL NÃO DECLARADA LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
            return a[1:]
        if tk.tipo == 'NULO':
            print(F"\nERRO SEMANTICO - VARIAVEL '{tk.lexema}' NÃO DECLARADA LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
        
        elif tk.tipo == 'inteiro':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'scanf("%d", &{a[0].lexema});\n'
        elif tk.tipo == 'real':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'scanf("%lf", &{a[0].lexema});\n'
        elif tk.tipo == 'literal':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'scanf("%s", &{a[0].lexema});\n'
        
        return a[1:]

    if t == 14:
        if token_aux.classe != 'ID':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'printf("{token_aux.lexema}");\n'
        
        elif token_aux.tipo == 'inteiro':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'printf("%d",{token_aux.lexema});\n'

        elif token_aux.tipo == 'real':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'printf("%lf",{token_aux.lexema});\n'
        
        elif token_aux.tipo == 'literal':
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f'printf("%s",{token_aux.lexema});\n'
    
        
    if t == 15:
        token_aux.lexema = a[0].lexema.replace('"','')
        token_aux.tipo = a[0].tipo
        token_aux.classe = a[0].classe
        a.pop(0)
    
    
    if t == 16:
        token_aux.lexema = a[0].lexema
        token_aux.tipo = a[0].tipo
        token_aux.classe = a[0].classe
        a.pop(0)
    
    if t == 17:
        tk = tab.buscaLexema(a[0].lexema)
        if tk == False:
            print(f"\nERRO SEMANTICO - VARIAVEL {a[0].lexema} NÃO DECLARADA LINHA {linha+1} COLUNA {coluna}\n")
        elif tk.tipo == 'NULO':
            print(f"\nERRO SEMANTICO - VARIÁVEL '{tk.lexema}' NÃO DECLARADA LINHA {linha+1} COLUNA {coluna}\n")
        else:
            token_aux.lexema = a[0].lexema
            token_aux.tipo = a[0].tipo
            token_aux.classe = a[0].classe
        a.pop(0)
    
    
    if t == 19:
        tk = tab.buscaLexema(a[0].lexema)
        
        if tk == False:
            print(f"\nERRO SEMANTICO - VARIAVEL NÃO DECLARADA LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
            a.pop(0)
            return a
        
        elif tk.tipo == ld.tipo:
            
            if tk.tipo == ld.tipo:
                str2 = tabular(str2, tabulacao)
                str2 = str2 + f"{tk.lexema} = {ld.lexema};\n"
        
        else:
            print(f"\nERRO SEMANTICO: OPERANDOS {tk.lexema} e {ld.lexema} COM TIPOS INCOMPATIVEIS LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
        a.pop(0)
    
    
    if t == 20:
        if oprd1.tipo in ['inteiro','real'] and oprd2.tipo in ['inteiro', 'real'] and oprd1.tipo != 'literal':
            
            opm = a[1].lexema
            # linha Tx = oprd1 opm Oprd2
            str2 = tabular(str2, tabulacao)
            str2 = str2 + f"T{contadorTemporarias} = {oprd1.lexema} {opm} {oprd2.lexema};\n"
            
            # verifica se declara a temporária como int ou double
            if opm == '/' or oprd1.tipo == 'real':
                declaraTemp('double')
                ld = token(None, f'T{contadorTemporarias}', 'real')
            else: 
                declaraTemp('inteiro')
                ld = token(None, f'T{contadorTemporarias}', 'inteiro')
        
        else:
            print(f"\nERRO SEMANTICO: OPERANDOS '{oprd1.lexema}' e '{oprd2.lexema}' COM TIPOS INCOMPATIVEIS LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
        
        oprd1 = None
        oprd2 = None
            
        contadorTemporarias += 1
        a.pop(1)
    
        
    if t == 21:
        ld = oprd1
        oprd1 = None
    
    
    if t == 22:
        # verifica se é uma operação relacional, aritmetica ou outra
        if a[1].classe == 'OPR':
            temp = a[0]
            a.pop(0)
            
        elif a[1].classe == 'OPM':
            temp = a[2]
            a.pop(2)
            
        else:
            temp = a[1]
            a.pop(1)
        
        # pega o tk na tabela de simbolos    
        tk = tab.buscaLexema(temp.lexema)
        if tk == False:
            print(f"\nERRO SEMANTICO - VARIAVEL NÃO DECLARADA LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
            return a
        
        if tk.tipo == 'NULO':
            print(f"\nERRO SEMANTICO - VARIAVEL '{tk.lexema}' NÃO DECLARADA LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
            return a
        
        else:
            # se o oprd1 estiver vazio, salva no oprd2
            if oprd1 == None:
                oprd1 = tk
                
            else:
                oprd2 = tk

        
    if t == 23:
        if a[1].classe == 'OPR':
            temp = a[0]
            a.pop(0)
            
        elif a[1].classe == 'OPM':
            temp = a[2]
            a.pop(2)
            
        else:  
            temp = a[1]
            a.pop(1)
        
            
        if oprd1 == None:
            oprd1 = temp
        else:
            oprd2 = temp
            
    
      
    if t == 25:
        str2 = tabular(str2, tabulacao-1)
        str2 += "}\n"
        tabulacao = tabulacao - 1
    
    
    if t == 26:
        str2 = tabular(str2, tabulacao)
        str2 += f"if({expr.lexema})\n"
        str2 = tabular(str2, tabulacao)
        str2 += f"{{\n"
        tabulacao = tabulacao + 1
    
    if t == 27:       #Cria variavel Tx para receber o valor da operacao sendo realizada
        # verifica se os tipos sao compativeis
        if (oprd1.tipo == 'inteiro' or oprd1.tipo == 'real') and (oprd2.tipo == 'inteiro' or oprd2.tipo == 'real'):
            #lexema da expr recebe Tx
            expr.lexema = f"T{contadorTemporarias}"
            
            #linha Tx = oprd1 opr oprd2
            str2 = tabular(str2, tabulacao)
            str2 += f"T{contadorTemporarias} = {oprd1.lexema} {a[0].lexema} {oprd2.lexema};\n"
            
            if oprd1.tipo == 'inteiro':
                declaraTemp('inteiro')
            else:
                declaraTemp('double')
            
        else:
            print(f"\nERRO SEMANTICO - OPERANDOS COM TIPOS INCOMPATIVEIS LINHA {linha + 1} COLUNA {coluna}\n")
            corretude = False
        
        oprd1 = None
        oprd2 = None
        
        contadorTemporarias += 1
        a.pop(0)

    if t == 33:
        str2 = tabular(str2, tabulacao-1)
        str2 += f"}}\n"
        tabulacao = tabulacao - 1
    
    if t == 34:
        str2 = tabular(str2, tabulacao)
        str2 += f"while({expr.lexema})\n"
        str2 = tabular(str2, tabulacao)
        str2 += f"{{\n"
        tabulacao = tabulacao + 1

    #if t == 38:
        #criar lista lastWhile que armazena exp_r que iniciou o(s) ultimo(s) while.
        #quando t=38 se lastWhile[0] for true, sai pra linha depois do seu fim. Se nao, volta a analise pra linha de comeco do while em questao.
    
    if t == 39:
        str2 += f'}}'
        str1 += '\t/*------------------------------*/\n'
    return a

def gerarArquivo():
    if corretude == True:
        arquivo = open("teste.c",'w')
        arquivo.write(cabecalho + str1 + str2)
    
    
def declaraTemp(tipo):
    global str1
    global contadorTemporarias
    str1 = tabular(str1, 1)
    if tipo == "inteiro":
        str1 += f"int T{contadorTemporarias};\n"
    if tipo == "double":
        str1 += f"double T{contadorTemporarias};\n"
    if tipo == "literal":
        str1 += f"literal T{contadorTemporarias};\n"

def tabular(stringAlterada, tabulacao):
    i = 0
    while (i < tabulacao):
        stringAlterada = stringAlterada + f'\t'
        i = i+1
    return stringAlterada