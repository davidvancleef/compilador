from tokenn import token
from tabela import tabela

tab = tabela()

def retornaTabela():
    return tab

def erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro):
    lexema = "".join(palavra)
    tokenErro = token('ERROR',lexema,'NULO')
    if estado == 3:
        print(f'ERRO LÉXICO: O numero "{lexema}" necessita de um digito após o ponto decimal. linha: {linha + 1}, coluna: {coluna}')
    elif estado == 5:
        print(f'ERRO LÉXICO: Para o caso de {lexema} é necessário um digito ou operador após o exponencial. linha: {linha + 1}, coluna: {coluna}')
    elif estado == 6:
        print(f'ERRO LÉXICO: Para o caso de {lexema} é necessário um digito após os operadores, linha: {linha + 1}, coluna: {coluna}')
    elif estado == 8:
        print(f'ERRO LÉXICO: Para o caso de {lexema} é necessário um fecha aspas na linha: {linhaComErro + 1}, coluna: {colunaComErro}')
    else:
        print(f'ERRO LÉXICO: O lexema "{lexema}" é inválido na linguagem dada, linha: {linha + 1}, coluna: {coluna}')


def aceita(linha,coluna,estado,palavra):
    lexema = "".join(palavra)
    tipo = 'NULO'
    
    if estado == 1 or estado == 2 or estado == 4 or estado == 7:
        classe = "NUM"
        if "." in palavra or "-" in palavra:
            tipo = "real"
        else:
            tipo = "inteiro"
    if estado == 9:
        classe = "LIT"
        tipo = "literal"
    if estado == 10:
        classe = "EOF"
    if estado == 11:
        classe = "ID"
        tipo = "NULO"
        tokenRegistrado = tab.buscaLexema(lexema)
        if tokenRegistrado != False:
            return [tokenRegistrado,linha,coluna]
        tab.insercaoTabela(token(classe,lexema,'NULO'))
    if estado == 14 or estado == 15 or estado == 17 or estado == 18 or estado == 19:
        classe = "OPR"
    if estado == 16:
        classe = "ATR"
    if estado == 20:
        classe = "OPM"
    if estado == 21:
        classe = "FC_P"
    if estado == 22:
        classe = "AB_P"
    if estado == 23:
        classe = "PT_V"    
    if estado == 24:
        classe = "VIR"
    return [token(classe,lexema,tipo),linha,coluna]

def scanner(arquivo,linha,coluna):
    palavra = []
    estado = 0
    letras = list("ABCDEFGHIJKLMNOPKRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
    digitos = list("0123456789")
    linhaComErro = -1
    colunaComErro = -1
    caractereLido = arquivo[linha][coluna]

    while True:
        if estado == 0:
            linhaComErro = linha
            colunaComErro = coluna

            if caractereLido in digitos:
                estado = 1
                palavra.append(caractereLido)
            
            elif caractereLido == '"':
                estado = 8
                palavra.append(caractereLido)

            elif caractereLido == '$' and arquivo[linha] == arquivo[-1]:
                palavra.append('EOF')
                return aceita(linha,coluna,10,palavra)
            elif caractereLido in letras:
                estado = 11
                palavra.append(caractereLido)
            
            elif caractereLido == '{':
                estado = 12
            
            elif caractereLido == '<':
                estado = 14
                palavra.append(caractereLido)

            elif caractereLido == '>':
                estado = 17
                palavra.append(caractereLido)

            elif caractereLido == '=':
                estado = 19
                palavra.append(caractereLido)
            
            elif caractereLido in ['+','-','*','/']:
                estado = 20
                palavra.append(caractereLido)
            
            elif caractereLido == ')':
                estado = 21
                palavra.append(caractereLido)
            
            elif caractereLido == '(':
                estado = 22
                palavra.append(caractereLido)
            
            elif caractereLido == ';':
                estado = 23
                palavra.append(caractereLido)
            
            elif caractereLido == ',':
                estado = 24
                palavra.append(caractereLido)
            
            elif caractereLido == '\n':
                estado = 0
                linha = linha + 1
                coluna = -1
            
            elif caractereLido == ' ' or caractereLido == '\t':
                estado = 0
                
            else:
                estado = 0
                palavra.append(caractereLido)
                erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro)
                palavra.clear()
        
        elif estado == 1:
            if caractereLido in digitos:
                palavra.append(caractereLido)
                estado = 2
            elif caractereLido == '.':
                estado = 3
                palavra.append(caractereLido)
            elif caractereLido == 'E' or caractereLido == 'e':
                estado = 5
                palavra.append(caractereLido) 
            else:
                return aceita(linha,coluna,estado,palavra)
            
        elif estado == 2:
            if caractereLido == '.':
                estado = 3
                palavra.append(caractereLido)
            elif caractereLido in digitos:
                estado = 2
                palavra.append(caractereLido)
            else:
                return aceita(linha,coluna,estado,palavra)

        elif estado == 3:
            if caractereLido in digitos:
                estado = 4
                palavra.append(caractereLido)               
            else:
                estado = 0
                palavra.append(caractereLido)
                erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro)
                palavra.clear()
        
        elif estado == 4:
            if caractereLido in digitos:
                estado = 4
                palavra.append(caractereLido)
            elif caractereLido == 'E' or caractereLido == 'e':
                estado = 5
                palavra.append(caractereLido)
            else:
                return aceita(linha,coluna,estado,palavra)

        elif estado == 5:        
            if caractereLido in digitos:
                estado = 7
                palavra.append(caractereLido)
            elif caractereLido == '+' or caractereLido == '-':
                estado = 6
                palavra.append(caractereLido)
            else:
                estado = 0
                palavra.append(caractereLido)
                erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro)
                palavra.clear()

        elif estado == 6:       
            if caractereLido in digitos:
                palavra.append(caractereLido)
                estado = 7
            else:
                estado = 0
                palavra.append(caractereLido)
                erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro)
                palavra.clear()
        
        elif estado == 7:       
            if caractereLido in digitos:
                palavra.append(caractereLido)
                estado = 7
            else:
                return aceita(linha,coluna,estado,palavra)
            
        elif estado == 8:
            if caractereLido == '"':
                estado = 9
                palavra.append(caractereLido)
            elif caractereLido != '\n':
                palavra.append(caractereLido)
            else:
                estado = 0
                palavra.append(caractereLido)
                erro(linha,coluna,palavra,estado,linhaComErro,colunaComErro)
                palavra.clear()
        
        elif estado == 9:
            return aceita(linha,coluna,estado,palavra)
        
        elif estado == 11:  
            if caractereLido in letras or caractereLido in digitos or caractereLido == '_':
                palavra.append(caractereLido)
            else:
                return aceita(linha,coluna,estado,palavra)
                    
        elif estado == 12:
            if caractereLido == '}' :
                estado = 0
            elif caractereLido == '$' and arquivo[linha] == arquivo[-1]:
                print(f"Comentário da linha {linhaComErro + 1} coluna {colunaComErro} não fechado")
                palavra.append('EOF')
                return aceita(linha,coluna,10,palavra)
            elif caractereLido == '\n':
                linha = linha + 1
                coluna = -1
                
        elif estado == 14:
            if caractereLido == '=' or caractereLido == '>':
                estado = 15
                palavra.append(caractereLido)
            elif caractereLido == '-':
                estado = 16
                palavra.append(caractereLido)
            else:
                return aceita(linha,coluna,estado,palavra)

        elif estado == 15:
            return aceita(linha,coluna,estado,palavra)

        elif estado == 16:
            return aceita(linha,coluna,estado,palavra)

        elif estado == 17:
            if caractereLido == '=':
                estado = 18
                palavra.append(caractereLido)
            else:
                return aceita(linha,coluna,estado,palavra)

        elif estado == 19:
            return aceita(linha,coluna,estado,palavra)

        elif estado == 20:
            return aceita(linha,coluna,estado,palavra)

        elif estado in [21,22,23,24]:
            return aceita(linha,coluna,estado,palavra)
        
        coluna = coluna + 1
        caractereLido = arquivo[linha][coluna]
            