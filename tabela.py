from tokenn import token

class tabela:
    def __init__(self) -> None:
        self.tabela = []
        self.insercaoInicial("inicio")
        self.insercaoInicial("varinicio")
        self.insercaoInicial("varfim")
        self.insercaoInicial("escreva")
        self.insercaoInicial("leia")
        self.insercaoInicial("se")
        self.insercaoInicial("entao")
        self.insercaoInicial("fimse")
        self.insercaoInicial("repita")
        self.insercaoInicial("fimrepita")
        self.insercaoInicial("fim")
        self.insercaoInicial("inteiro")
        self.insercaoInicial("literal")
        self.insercaoInicial("real")

    def insercaoTabela(self,tokenInserido):
        self.tabela.append(tokenInserido)

    def insercaoInicial(self,lexema):
        self.tabela.append(token(lexema,lexema,lexema))
    
    def buscaLexema(self,lexema):
        for tokenRegistrado in self.tabela:
            if tokenRegistrado.lexema == lexema:
                return tokenRegistrado
        return False
    
    def atualizar(self, lexema, tipo):
        for i,tk in enumerate(self.tabela):
            if tk.lexema == lexema:
                token_aux = token(tk.classe,lexema,tipo)
                self.tabela.pop(i)
                self.tabela.insert(i,token_aux)
                break

    def printarTabelaAtualizada(self):
        print('\n---TABELA DE SIMBOLOS---')
        for simbolo in self.tabela:
            print(f'Classe: {simbolo.classe}, Lexema: {simbolo.lexema}, Tipo: {simbolo.tipo}')