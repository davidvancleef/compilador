from scanner import scanner,retornaTabela
import sintatico

if __name__ == '__main__':
    arquivoTeste = open("arquivoTeste.txt",'r',encoding='utf-8')
    arquivoTeste = arquivoTeste.readlines()
    arquivoTeste[-1] = arquivoTeste[-1] + ' $'
    
    sintatico.rodar(arquivoTeste)   