from scanner import scanner,retornaTabela

if __name__ == '__main__':
    arquivo = open("arquivoTeste.txt",'r',encoding='utf-8')
    arquivo = arquivo.readlines()
    arquivo[-1] = arquivo[-1] + ' $'
    linha = 0
    coluna = 0

    while (linha <= len(arquivo)):
        tokenObtido = scanner(arquivo,linha,coluna)
        linha = tokenObtido[1]
        coluna = tokenObtido[2]

        if tokenObtido[0].classe != 'ERROR':
            print(f'Classe: {tokenObtido[0].classe}, Lexema: {tokenObtido[0].lexema}, Tipo: {tokenObtido[0].tipo}')
            if tokenObtido[0].classe == 'EOF':
                break
            
    tab = retornaTabela()
    tab.printarTabelaAtualizada()