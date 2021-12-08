#Importação da biblioteca.
import random
import matplotlib.pyplot as plt

class PontoDeEntrega:

    #Permite que a classe inicialize seus atributos.
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Permite representar os objetos da classe como uma string.
    def __repr__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    #Calcula e retorna a distância entre 2 pontos.
    def distancia_pontos(self, outro_ponto):

        return abs(self.x - outro_ponto.x) + abs(self.y - outro_ponto.y)


# DEFINIÇÃO DA POPULAÇÃO INICIAL #

#Gera uma rota aleatória com todas os pontos (menos o inicial/final).
#Na lista de pontos não está contido o ponto de partida/retorno, pois eles são fixos.
def criar_rota(lista_pontos):

    rota = lista_pontos.copy()
    random.shuffle(rota)

    return rota

#Define qual vai ser a população inicial.
def populacao_inicial(tamanho_pop, lista_pontos):

    populacao = []

    for i in range(tamanho_pop):
        populacao.append(criar_rota(lista_pontos))

    return populacao

#Calcula e retorna a distância a ser percorrida em uma determinada rota.
def distancia_rota(rota):

    distancia_total = 0

    #Adiciona o ponto de origem para que ele seja considerado no cálculo da distância.
    rota_inicio_fim = [ponto_inicial]
    for i in range(len(rota)):
        rota_inicio_fim.append(rota[i])

    #Seleciona os pontos da rota dois a dois para que seja calculada a distância entre eles.
    for i in range(len(rota_inicio_fim)):
        partida = rota_inicio_fim[i]
        destino = None


        #Se o ponto de partida não for o último da rota -> Define destino = próximo ponto da rota.
        if i + 1 < len(rota_inicio_fim):
            destino = rota_inicio_fim[i + 1]

        #A rota precisa começar e terminar no mesmo ponto.
        #Se o ponto de partida for o último da rota -> Define destino = ponto de origem (retorna para o início).
        else:
            destino = rota_inicio_fim[0]

        distancia_total += partida.distancia_pontos(destino)

    return distancia_total


# FITNESS - FUNÇÃO DE APTIDÃO #

#Calcula e retorna o valor de aptidão de determinada rota.
def fitness_rota(distancia):

    #O valor do fitness é inversamente proporcional a distância da rota.
    fitness_valor = 1 / float(distancia_rota(distancia))

    return fitness_valor

#Ordena as rotas pelo valor do fitness (fundação de aptidão).
def rank_rotas(populacao):

    fitness_rotas = []

    #Adiciona o índice de cada rota -> Para cada linha da matriz: [indice da rota, valor do fitness].
    for i in range(len(populacao)):
        fitness_rotas.append([i, fitness_rota(populacao[i])])

    #Ordena a matriz utilizando como critério o valor do fitness (decrescente).
    fitness_rotas.sort(reverse=True, key=lambda x: x[1])
    melhores.append(fitness_rotas[0][1])

    total = 0
    for i in range(len(fitness_rotas[1])):
        total = total + fitness_rotas[i][1]
    media = total/len(fitness_rotas[1])
    medias.append(media)
    return fitness_rotas


# SELEÇÃO #

#Seleciona os melhores indivíduos.
def selecionador(rotas_rankeadas):

    selecao = []

    rank = rotas_rankeadas
    probabilidade = 0
    fitness_total = 0

    #Calcula o somatório do valor fitness de todas as rotas.
    for i in range(len(rank)):
        fitness_total += rank[i][1]

    #Calcula a probabilidade cumulativa de cada rota.
    for i in range(len(rank)):
        probabilidade += (rank[i][1] * 100) / fitness_total
        rank[i].append(probabilidade)

    #Seleciona as rotas
    while len(selecao) != len(rotas_rankeadas):
        num_aleatorio = 100 * random.random()
        for i in range(len(rotas_rankeadas)):
            if num_aleatorio <= rank[i][2]:
                selecao.append(rotas_rankeadas[i][0])
                break

    return selecao

#Usa o indice de cada rota que foi selecionada para buscar e retornar cada uma delas.
def encontrar_rotas(populacao, selecao_resultado):
    rotas = []
    for i in range(len(selecao_resultado)):
        rotas.append(populacao[selecao_resultado[i]])

    return rotas

# REPRODUÇÃO #

#Gera um indivíduo (filho) a partir de outros dois (pais).
def crossover(pais1, pais2): #Cruzamento/Crossover

    filho = []

    filho_parte1 = []
    filho_parte2 = []

    #Seleciona dois números que vão indicar onde começa/termina o subconjunto escolhido do pai 1.
    gene1 = int(random.random() * len(pais1))
    gene2 = int(random.random() * len(pais1))

    #Define qual dos números indica o início e qual indica o fim
    if gene1 > gene2:
        gene_inicio = gene2
        gene_fim = gene1
    else:
        gene_inicio = gene1
        gene_fim = gene2

    #Adiciona à parte 1 do filho os genes selecionados do pai 1.
    for i in range(gene_inicio, gene_fim):
        filho_parte1.append(pais1[i])

    #Adiciona os genes do pai 2 (que não foram selecionados do pai 1) para completar.
    for i in range(len(pais2)):
        if pais2[i] not in filho_parte1:
            filho_parte2.append(pais2[i])

    #Junta a parte vinda do pai 1 com a parte vida do pai 2.
    filho = filho_parte1 + filho_parte2

    return filho


# NOVA POPULAÇÃO #

#Define a nova geração (indivíduos ainda não foram mutados).
def nova_populacao(rotas_selecionadas):

    filhos_lista = []
    rotas_selecioadas_random = random.sample(rotas_selecionadas, len(rotas_selecionadas))

    #Completa a próxima geração com os filhos gerados pelos pais selecionados.
    for i in range(len(rotas_selecionadas)):
        filho = crossover(rotas_selecioadas_random[i], rotas_selecioadas_random[len(rotas_selecionadas)-i-1])
        filhos_lista.append(filho)

    return filhos_lista

#Mutação
#Identidica se haverá mutação em determinado individuo e caso haja, muta ele e retorna.
def mutacao(individuo, taxa_mutacao):

    #Confere se haverá mutação.
    if (random.random() < taxa_mutacao):

        #Seleciona o indice dos genes que trocarão de lugar.
        geneA = int(random.random() * len(individuo))
        geneB = int(random.random() * len(individuo))

        #Troca os genes de lugar.
        ponto1 = individuo[geneA]
        ponto2 = individuo[geneB]

        individuo[geneA] = ponto2
        individuo[geneB] = ponto1

    return individuo

#Chama a função "mutação" para cada indivíduo da população.
def mutar_populacao(populacao, taxa_mutacao):
    população_mutada = []

    for i in range(len(populacao)):
        individuo_mutado = mutacao(populacao[i], taxa_mutacao)
        população_mutada.append(individuo_mutado)

    return populacao

#Define a geração seguinte com base na geração atual.
def geracao_seguinte(geracao_atual, taxa_mutacao):
    rotas_rankeadas = rank_rotas(geracao_atual)
    selecao_resultado = selecionador(rotas_rankeadas)
    rotas_selecionadas = encontrar_rotas(geracao_atual, selecao_resultado)
    filhos = nova_populacao(rotas_selecionadas)
    proxima_geracao = mutar_populacao(filhos, taxa_mutacao)

    return proxima_geracao


# FUNÇÃO PRINCIPAL DO ALGORITMO GENÉTICO #

def principal(populacao, tamanha_populacao, taxa_mutacao, geracoes):

    #Define a população inicial como a atual.
    populacao_atual = populacao_inicial(tamanha_populacao, populacao)

    #Gera novas gerações de acordo com a quantidade de gerações definidas.
    for i in range(geracoes):

        #Define a nova geração como a atual.
        populacao_atual = geracao_seguinte(populacao_atual, taxa_mutacao)

    #Imprime a distância que será percorrida na melhor rota.
    #print("Distância final: " + str(int(1 / rank_rotas(populacao_atual)[0][1])))

    #Pega o índice referente a melhor rota.

    melhor_rota_indice = rank_rotas(populacao_atual)[0][0]
    #Usa o índice da melhor nota para retorna-lá.
    melhor_rota = populacao_atual[melhor_rota_indice]

    return melhor_rota


#Abre o arquivo com a matriz de entrada.
arquivo = open("matriz.txt")

#PRIMEIRA LINHA DA ENTRADA - Recebe o tamanho da matriz (linha, coluna).
linha, coluna = list(map(int, arquivo.readline().split()))

#Lista vazia
mapa = []

#DEMAIS LINHAS DA ENTRADA - Recebe as linhas e a transforma em uma matriz (lista de listas).
for i in range(linha + 1):
    if i >= 1:
        mapa.append(' '.join(arquivo.readline()).split())

#Lista vazia
ponto_identificacao = []

#Identficica onde os pontos estão localizados na matriz e salva a letra correspondente e a localização(x,y).
for i in range(linha):
    for j in range(coluna):
        if mapa[i][j] != '0':
            ponto_identificacao.append([mapa[i][j], PontoDeEntrega(i, j)])

#Lista vazia.
pontos_de_entrega = []
melhores = []
medias=[]
#Usa as informações armazenadas em "ponto_identificacao" para montar uma lista com os todos pontos de entrega.
for i in range(len(ponto_identificacao)):
    if ponto_identificacao[i][0] != 'R':
        pontos_de_entrega.append(ponto_identificacao[i][1])
    else:
        ponto_inicial = ponto_identificacao[i][1]

resposta = principal(pontos_de_entrega, 200, 0.03, 80)
#print(resposta)

#Imprime na tela a letra referente a coordenada de cada ponto da rota.
for i in range(len(resposta)):
    for j in range(len(ponto_identificacao)):
        if resposta[i] == ponto_identificacao[j][1]:
            if i < len(resposta) - 1:
                print(ponto_identificacao[j][0], end=" ")
            else:
                print(ponto_identificacao[j][0])
geracoes = []
for i in range(len(melhores)):
    geracoes.append(i)

plt.plot(melhores, label='Melhor da geração')
plt.plot(medias, label='Média da geração')
plt.ylabel('Valor Fitness')
plt.xlabel('Quantidade de gerações')
plt.legend()
plt.show()