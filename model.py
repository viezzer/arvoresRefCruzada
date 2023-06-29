import re
import unicodedata

class NodeL:
    def __init__(self, letra):
        self.letra = letra
        self.ant = None
        self.prox = None
        # self.lista = ListaDePalavras()

class NodeP:
    def __init__(self, palavra):
        self.palavra = palavra
        self.ocorrencias = 1
        self.left = None
        self.right = None

class ListaDePalavras:
    def __init__(self):
        self.head = None
        self.size = 0

    def inserePalavra(self, nodoP):
        if self.head is None:
            self.head = nodoP
        else:
            aux = self.head
            while aux.prox is not None:
                aux = aux.prox
            aux.prox = nodoP
        self.size += 1

    def remove(self, palavra):
        if self.head is None:
            return False
        if self.head.palavra == palavra:
            self.head = self.head.prox
            self.size -= 1
            return True
        aux = self.head
        while aux.prox is not None:
            if aux.prox.palavra == palavra:
                aux.prox = aux.prox.prox
                self.size -= 1
                return True
            aux = aux.prox
        return False

    def showList(self):
        if self.head is None:
            print("Lista de palavras vazia")
            return
        aux = self.head
        while aux is not None:
            print(aux.palavra)
            aux = aux.prox

    def showListInvertido(self):
        if self.head is None:
            print("Lista de palavras vazia")
            return
        self.recursivePrint(self.head)

    def recursivePrint(self, node):
        if node is None:
            return
        self.recursivePrint(node.prox)
        print(node.palavra)


class ListaDeLetras:
    def __init__(self, path):
        self.head = None
        self.tail = None
        self.size = 0
        self.createList(path)

    def remover_acentos(self, palavra):
        palavra_sem_acentos = ''.join(
            letra for letra in unicodedata.normalize('NFKD', palavra)
            if not unicodedata.combining(letra)
        )
        return palavra_sem_acentos
    
    def obter_palavras_do_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            texto = arquivo.read()
            palavras = re.findall(r'\b\w+\b', texto)
            return palavras

    def createList(self, path):
        self.head = None
        self.size = 0
        words = self.obter_palavras_do_arquivo(path)

        for word in words:
            print(word)
            l = self.remover_acentos(word[0].lower())
            print(l)
            if self.head is None:
                self.insereLetra(l)
            else:
                aux = self.head
                while aux is not None and aux.letra != l:
                    aux = aux.prox
                if aux is None:
                    self.insereLetra(l)
            # self.inserePalavra(l, word)

    def getPalavras(self):
        lp = ListaDePalavras()
        aux = self.head
        while aux is not None:
            auxPalavra = aux.lista.head
            while auxPalavra is not None:
                lp.inserePalavra(auxPalavra)
                auxPalavra = auxPalavra.prox
            aux = aux.prox
        if lp.size > 0:
            return lp
        return None

    def insereLetra(self, l):
        novoNodo = NodeL(l)

        if self.head is None:
            self.head = novoNodo
            self.tail = novoNodo
        else:
            atual = self.head
            anterior = self.head.ant

            while atual is not None and atual.letra < l:
                anterior = atual
                atual = atual.prox

            if anterior is None and atual is not None:
                atual.ant = novoNodo
                novoNodo.prox = atual
                self.head = novoNodo
            elif atual is None and anterior is not None:
                novoNodo.ant = anterior
                anterior.prox = novoNodo
                self.tail = novoNodo
            elif anterior is not None and atual is not None:
                novoNodo.ant = anterior
                novoNodo.prox = atual
                anterior.prox = novoNodo
                atual.ant = novoNodo

        self.size += 1

    def removeLetra(self, l):
        if self.head is not None and self.head.letra == l:
            self.head = self.head.prox
            self.size -= 1
            return True
        if self.tail is not None and self.tail.letra == l:
            self.tail = self.tail.ant
            self.tail.prox = None
            self.size -= 1
            return True
        aux = self.head
        ant = self.head.ant
        while aux is not None:
            if aux.letra == l:
                ant.prox = aux.prox
                self.size -= 1
                return True
            ant = aux
            aux = aux.prox
        return False

    def inserePalavra(self, l, p):
        nodo = self.pesquisaLetra(l)
        nodoP = NodeP(p)
        nodo.lista.inserePalavra(nodoP)

    def contaPalavras(self):
        conta = 0
        aux = self.head
        while aux is not None:
            conta += aux.lista.size
            aux = aux.prox
        return conta

    def contaOcorrencias(self):
        conta = 0
        aux = self.head
        while aux is not None:
            conta += aux.lista.ocorrencias
            aux = aux.prox
        return conta

    def filtraLetra(self, l):
        nodoL = self.pesquisaLetra(l)
        if nodoL is not None:
            lp = nodoL.lista
            if lp.size > 0:
                return lp
        return None

    def pesquisaLetra(self, l):
        aux = self.head
        while aux is not None:
            if aux.letra == l:
                return aux
            aux = aux.prox
        return None

    def removePalavra(self, p):
        nodoL = self.pesquisaLetra(p[0])
        if nodoL is not None:
            if nodoL.lista.remove(p):
                if nodoL.lista.size == 0:
                    print("Removendo Letra...")
                    if self.removeLetra(nodoL.letra):
                        print("Letra removida")
                return True
        return False

    def pesquisaPorNumeroDeOcorrencia(self, n):
        lp = ListaDePalavras()
        aux = self.head
        while aux is not None:
            auxP = aux.lista.head
            while auxP is not None:
                if auxP.freq == n:
                    lp.inserePalavra(auxP)
                auxP = auxP.prox
            aux = aux.prox
        if lp.size > 0:
            return lp
        return None

    def exibir(self):
        if self.head is None:
            print("Lista não possui conteúdo")
            return
        aux = self.head
        while aux is not None:
            print("Letra: " + aux.letra.upper())
            # aux.lista.showList()
            aux = aux.prox

    def exibirInvertido(self):
        if self.tail is None:
            print("Lista não possui conteúdo")
            return
        aux = self.tail
        while aux is not None:
            print("\nLetra: " + aux.letra.upper())
            aux.lista.showListInvertido()
            aux = aux.ant
