import re
import unicodedata

class NodeL:
    def __init__(self, letra):
        self.letra = letra
        self.ant = None
        self.prox = None
        self.abp = ArvoreBinariaDePesquisa()

class NodeP:
    def __init__(self, palavra):
        self.palavra = palavra
        self.ocorrencias = 1
        self.left = None
        self.right = None

class ArvoreBinariaDePesquisa:
    def __init__(self):
        self.raiz = None
        self.size = 0
        self.ocorrencias = 0 

    def exibir_palavras_com_ocorrencia_unica(self):
        if self.raiz is None:
            print("A árvore está vazia.")
            return

        print("Palavras com ocorrência única:")
        self.exibir_palavras_com_ocorrencia_unica_recursivo(self.raiz)

    def exibir_palavras_com_ocorrencia_unica_recursivo(self, no):
        if no is not None:
            self.exibir_palavras_com_ocorrencia_unica_recursivo(no.left)

            if no.ocorrencias == 1:
                print(no.palavra)

            self.exibir_palavras_com_ocorrencia_unica_recursivo(no.right)

    def encontrar_maior_ocorrencia(self):
        if self.raiz is None:
            return None, 0

        max_ocorrencias = [-1]
        palavras_max_ocorrencias = []

        self.encontrar_maior_ocorrencia_recursivo(self.raiz, max_ocorrencias, palavras_max_ocorrencias)

        return palavras_max_ocorrencias, max_ocorrencias[0]
    
    def encontrar_maior_ocorrencia_recursivo(self, no, max_ocorrencias, palavras_max_ocorrencias):
        if no is not None:
            self.encontrar_maior_ocorrencia_recursivo(no.left, max_ocorrencias, palavras_max_ocorrencias)

            if no.ocorrencias > max_ocorrencias[0]:
                max_ocorrencias[0] = no.ocorrencias
                palavras_max_ocorrencias.clear()  # Clear the list since we found a new maximum
                palavras_max_ocorrencias.append(no.palavra)
            elif no.ocorrencias == max_ocorrencias[0]:
                palavras_max_ocorrencias.append(no.palavra)

            self.encontrar_maior_ocorrencia_recursivo(no.right, max_ocorrencias, palavras_max_ocorrencias)

    def inserePalavra(self, palavra):
        print("inserindo: ", palavra)
        
        if self.raiz is None:
            self.raiz = NodeP(palavra)
            self.size += 1
        else:
            self.inserir_recursivo(self.raiz, palavra)
        self.ocorrencias+=1

    def inserir_recursivo(self, nodo, palavra):
        if palavra == nodo.palavra:
            nodo.ocorrencias+=1
            return
        if palavra < nodo.palavra:
            if nodo.left is None:
                nodo.left = NodeP(palavra)
                self.size+=1
            else:
                self.inserir_recursivo(nodo.left, palavra)
        elif palavra > nodo.palavra:
            if nodo.right is None:
                nodo.right = NodeP(palavra)
                self.size+=1
            else:
                self.inserir_recursivo(nodo.right, palavra)

    def pesquisaPalavra(self, palavra):
        no_atual = self.raiz

        while no_atual is not None:
            if palavra == no_atual.palavra:
                return no_atual
            elif palavra < no_atual.palavra:
                no_atual = no_atual.left
            else:
                no_atual = no_atual.right

        return None

    def em_ordem_inversa(self):
        self.em_ordem_inversa_recursivo(self.raiz)

    def em_ordem_inversa_recursivo(self, nodo):
        if nodo is not None:
            self.em_ordem_inversa_recursivo(nodo.right)
            print(nodo.palavra, " - ", nodo.ocorrencias)
            self.em_ordem_inversa_recursivo(nodo.left)

    def em_ordem(self):
        self.em_ordem_recursivo(self.raiz)

    def em_ordem_recursivo(self, nodo):
        if nodo is not None:
            self.em_ordem_recursivo(nodo.left)
            print(nodo.palavra, " - ", nodo.ocorrencias)
            self.em_ordem_recursivo(nodo.right)

    def encontrar_menor_sucessor(self, no):
        atual = no
        while atual.left is not None:
            atual = atual.left
        return atual

    def remover_palavra(self, palavra):
        nodo = self.remover_palavra_recursivo(self.raiz, palavra)
        if nodo is None:
            return False
        return True

    def remover_palavra_recursivo(self, no, palavra):
        if no is None:
            return no

        if palavra < no.palavra:
            no.left = self.remover_palavra_recursivo(no.left, palavra)
        elif palavra > no.palavra:
            no.right = self.remover_palavra_recursivo(no.right, palavra)
        else:
            # Caso 1: Nó é uma folha (não tem filhos)
            if no.left is None and no.right is None:
                no = None
            # Caso 2: Nó tem apenas um filho
            elif no.left is None:
                no = no.right
            elif no.right is None:
                no = no.left
            # Caso 3: Nó tem dois filhos
            else:
                menor_sucessor = self.encontrar_menor_sucessor(no.right)
                no.palavra = menor_sucessor.palavra
                no.right = self.remover_palavra_recursivo(no.right, menor_sucessor.palavra)

        return no

    def palavras_mais_longas(self):
        if self.raiz is None:
            print("A árvore está vazia.")
            return

        palavras_longas = []
        tamanho_max = self.encontrar_tamanho_max_recursivo(self.raiz)

        self.encontrar_palavras_mais_longas_recursivo(self.raiz, palavras_longas, tamanho_max)

        print("Palavras mais longas:")
        for palavra in palavras_longas:
            print(palavra)

    def encontrar_tamanho_max_recursivo(self, no):
        if no is None:
            return 0

        tamanho_esquerda = self.encontrar_tamanho_max_recursivo(no.left)
        tamanho_direita = self.encontrar_tamanho_max_recursivo(no.right)

        return max(len(no.palavra), tamanho_esquerda, tamanho_direita)

    def encontrar_palavras_mais_longas_recursivo(self, no, palavras_longas, tamanho_max):
        if no is not None:
            self.encontrar_palavras_mais_longas_recursivo(no.left, palavras_longas, tamanho_max)

            if len(no.palavra) == tamanho_max:
                palavras_longas.append(no.palavra)

            self.encontrar_palavras_mais_longas_recursivo(no.right, palavras_longas, tamanho_max)

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
            # print(l)
            # se a lista estiver vazia insere como primeira letra da lista
            if self.head is None:
                nodoLetra = self.insereLetra(l)
                nodoLetra.abp.inserePalavra(word)
            else:
                #lista ja possui letras, insere nova letra em ordem
                aux = self.head
                while aux is not None and aux.letra != l:
                    aux = aux.prox
                if aux is None:
                    nodoLetra = self.insereLetra(l)
                    nodoLetra.abp.inserePalavra(word)
                else:
                    aux.abp.inserePalavra(word)

    def exibirUnicaOcorrencia(self):
        if self.head is None:
            print("Lista não possui conteúdo")
            return
        aux = self.head
        while aux is not None:
            print("\nLetra: " + aux.letra.upper())
            aux.abp.exibir_palavras_com_ocorrencia_unica()
            aux = aux.prox

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
        return novoNodo

    def exibirPalavrasMaisLongas(self):
        if self.head is None:
            print("Lista não possui conteúdo")
            return
        aux = self.head
        while aux is not None:
            print("\nLetra: " + aux.letra.upper())
            aux.abp.palavras_mais_longas()
            aux = aux.prox

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

    def contaPalavras(self):
        conta = 0
        aux = self.head
        while aux is not None:
            conta += aux.abp.size
            aux = aux.prox
        return conta

    def contaOcorrencias(self):
        conta = 0
        aux = self.head
        while aux is not None:
            conta += aux.abp.ocorrencias
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

    # def pesquisaPorNumeroDeOcorrencia(self, n):
    #     lp = ListaDePalavras()
    #     aux = self.head
    #     while aux is not None:
    #         auxP = aux.lista.head
    #         while auxP is not None:
    #             if auxP.freq == n:
    #                 lp.inserePalavra(auxP)
    #             auxP = auxP.prox
    #         aux = aux.prox
    #     if lp.size > 0:
    #         return lp
    #     return None

    def exibir(self):
        if self.head is None:
            print("Lista não possui conteúdo")
            return
        aux = self.head
        while aux is not None:
            print("\nLetra: " + aux.letra.upper())
            aux.abp.em_ordem()
            aux = aux.prox

    def exibirInvertido(self):
        if self.tail is None:
            print("Lista não possui conteúdo")
            return
        aux = self.tail
        while aux is not None:
            print("\nLetra: " + aux.letra.upper())
            aux.abp.em_ordem_inversa()
            aux = aux.ant

    def encontrar_palavra_maior_ocorrencia(self):
        palavra_maior_ocorrencia = None
        maior_ocorrencia = 0

        nodo_letra = self.head
        while nodo_letra:
            abp = nodo_letra.abp
            if abp:
                palavra, ocorrencias = abp.encontrar_maior_ocorrencia()
                if ocorrencias > maior_ocorrencia:
                    palavra_maior_ocorrencia = palavra
                    maior_ocorrencia = ocorrencias
            nodo_letra = nodo_letra.prox

        return palavra_maior_ocorrencia, maior_ocorrencia



class App:
    def __init__(self, path_arquivo):
        self.lista = ListaDeLetras(path_arquivo)
        self.executar()
        

    def executar(self):
        opcao = None
        while opcao!= 0:
            self.exibir_opcoes()
            opcao = int(input("\n-> Digite o número da sua opção: "))
            if opcao == 0:
                print("Tchau!...")
                return
            elif opcao==1:
                self.opcao1()
            elif opcao==2:
                self.opcao2()
            elif opcao==3:
                self.opcao3()
            elif opcao==4:
                self.opcao4()
            elif opcao==5:
                self.opcao5()
            elif opcao==6:
                self.opcao6()
            elif opcao==7:
                self.opcao7()
            elif opcao==8:
                self.opcao8()
            elif opcao==9:
                self.opcao9()

    def exibir_opcoes(self):
        print("\n---{ MENU DE OPÇÕES }---")
        print("0. Sair;")
        print("1. Consulta uma palavra na estrutura, e seu número de ocorrências;")
        print("2. Remove uma palavra da estrutura;")
        print("3. Exibe número total de palavras da estrutura;")
        print("4. Exibe número total de ocorrências de palavras na estrutura;")
        print("5. Exibe a lista das palavras da estrutura;")
        print("6. Exibe a lista das palavras da estrutura iniciadas por uma determinada letra;")
        print("7. Exibe a palavra (ou as palavras) com maior número de ocorrências;")
        print("8. Exibe, em ordem alfabética, as palavras que só tem uma ocorrência;")
        print("9. Exibe as palavras mais longas da estrutura;")

    def opcao9(self):
        self.lista.exibirPalavrasMaisLongas()

    def opcao8(self):
        self.lista.exibirUnicaOcorrencia()

    def opcao7(self):
        palavra_maior_ocorrencia, maior_ocorrencia = self.lista.encontrar_palavra_maior_ocorrencia()
        print(palavra_maior_ocorrencia, maior_ocorrencia)

    def opcao6(self):
        letra = input("\nLetra: ")
        nodoLetra = self.lista.pesquisaLetra(letra)
        if nodoLetra is None:
            print("\n-> Letra não encontrada na estrutura")
            return
        opcao2 = int(input("\n1. Ordem alfabética\n2. Ordem alfabética inversa\nSelecione uma ordem: \n"))
        if opcao2==1:
            nodoLetra.abp.em_ordem()
        elif opcao2==2:
            nodoLetra.abp.em_ordem_inversa()
        else:
            print("\nNenhuma opção selecionada")

    def opcao5(self):
        opcao2 = int(input("\n1. Ordem alfabética\n2. Ordem alfabética inversa\nSelecione uma ordem: "))
        if opcao2==1:
            self.lista.exibir()
        elif opcao2==2:
            self.lista.exibirInvertido()
        else:
            print("\nNenhuma opção selecionada")

    def opcao4(self):
        num = self.lista.contaOcorrencias()
        print("\n", num," ocorrências de palavras na estrutura")

    def opcao3(self):
        num = self.lista.contaPalavras()
        print("\n", num, " palavras na estrutura")

    def opcao2(self):
        palavra = input("\nPalavra: ")
        nodoLetra = self.lista.pesquisaLetra(palavra[0])
        if nodoLetra is None:
            print("\n-> Palavra não encontrada na estrutura")
            return
        palavra_removida = nodoLetra.abp.remover_palavra(palavra)
        if not palavra_removida:
            print("\n-> Palavra não encontrada na estrutura")
            return
        print("Removida da estrutura")

    def opcao1(self):
        palavra = input("\nPalavra: ")
        nodoLetra = self.lista.pesquisaLetra(palavra[0])
        if nodoLetra is None:
            print("\n-> Palavra não encontrada na estrutura")
            return
        nodoPalavra = nodoLetra.abp.pesquisaPalavra(palavra)
        if nodoPalavra is None:
            print("\n-> Palavra não encontrada na estrutura")
            return
        print("Ocorrências: ", nodoPalavra.ocorrencias)

        
