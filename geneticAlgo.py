# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 12:16:49 2017

@author: helto
"""
from  math import ceil, log
from random import randint
import math

limite_inferior = -10
limite_superior = 10
precisao = 1
populacao_maxima = 3000
populacao_inicial = 200
tam_populacao_atual = populacao_inicial
taxa_crossover_maxima = 100
taxa_crossover_inicial = 10
taxa_crossover_atual = taxa_crossover_inicial
pressao_sel_maxima = 16
pressao_sel_inicial = 2
pressao_sel_atual = pressao_sel_inicial


dim = 1
param_pop = []
param_crossover = []
param_presss_selc = []
size_generations = 0
solucao_atual = 0.0
geracao_init = 0
geracao = 0



class quadratica:

    geracoes = 0
    metade_cromo = None
    tam_ps = None
    dif_sup_inf = None
    pop = []
    melhor_solucao = None

    taxa_erro_treino = 000.1
    taxa_erro_aproximada = 0.1

    geracao_fitness_inicial = 0.0
    geracao_fitness_atual = 0.0

    def __init__(self, limite_inferior, limite_superior, precisao, tam_ps, tam_populacao, dim=1, taxa_crossover = 80):

        self.limite_inferior = limite_inferior
        self.limite_superior = limite_superior
        self.dif_sup_inf = (limite_superior - (limite_inferior))
        self.precisao = precisao
        self.dim = dim
        self.taxa_crossover = taxa_crossover

        self.tam_ps = tam_ps
        self.tam_populacao = tam_populacao

        self.tam_cromossomo = self.define_tam_cromossomo()
        self.quant_bits = ((self.tam_cromossomo) - 1)

        self.metade_cromo = int(self.tam_cromossomo)

    ''' Valores inteiros dos individuos (fitness) '''
    def BIN_DEC(self, individual):

        binario_inteiro = int(individual, 2)

        return (self.limite_inferior + binario_inteiro * (self.dif_sup_inf / self.quant_bits))

    '''Quantidade de possibilidades'''
    def define_tam_cromossomo(self):

        qtd_possibilidades = (self.dif_sup_inf * (10 ** self.precisao))

        return ceil(log(qtd_possibilidades, 2))

    def gerar_populacao(self):

        for d in range(self.dim):
            list_aux = []

            for i in range(self.tam_populacao):

                individual = ''

                for j in range(self.tam_cromossomo):

                    random_value = randint(0, 1)
                    individual += str(random_value)

                list_aux.append(individual)

            self.pop.insert(d,list_aux)

    def melhor_individuo(self):

        best_individuals = []
        fitness_best = 0.0

        self.geracao_fitness_atual = 0.0

        for i in range(self.tam_populacao):
            individuals = []

            for d in range(self.dim):
                individuals.append(self.pop[d][i])

            #Calcular média da população
            self.geracao_fitness_atual += float(self.fitness(individuals)/self.tam_populacao)

            if len(best_individuals) > 0:

                fitness_current = self.fitness(individuals)

                if fitness_best > fitness_current:
                    best_individuals = individuals
                    fitness_best = float(self.fitness(individuals))
            else:
                best_individuals = individuals
                fitness_best = float(self.fitness(individuals))

        return best_individuals

    def sort_individuals(self):

        melhor_individuo = []

        for i in range(self.tam_ps):

            index_sorted = randint(0, (self.tam_populacao-1))

            individual_sorted = []
            for d in range(self.dim):
                individual_sorted.append(self.pop[d][index_sorted])

            if (i == 0):
                melhor_individuo = individual_sorted
            else:
                fitness_best = self.fitness(melhor_individuo)
                fitness_sorted = self.fitness(individual_sorted)

                if (fitness_best > fitness_sorted):
                    melhor_individuo = individual_sorted.copy()

        return melhor_individuo

    ''' Metodo calcular o Fitness na funcao x^2 '''
    def fitness(self, individuals):

        valor_func = 0

        for i in range(self.dim):

            decimal_individual = float(self.BIN_DEC(individuals[i]))

            valor_func = math.pow(decimal_individual,2)

        return valor_func

    def crossover(self, parents):

        pai_1 = parents[0]
        pai_2 = parents[1]

        filho_1 = pai_1[:self.metade_cromo] + pai_2[self.metade_cromo:]
        filho_2 = pai_2[:self.metade_cromo] + pai_1[self.metade_cromo:]

        filhos = [filho_1, filho_2]

        return filhos

    def evoluir_taxa_crossover(self):

        random_value = randint(1, 100)

        if random_value <= self.taxa_crossover:
            return True

        return False

    def resetar_param_funcao(self):

        self.pop.clear()
        self.geracoes = 0
        self.melhor_solucao = None

    def evoluir(self):

        #Limpar configurações anteriores
        self.resetar_param_funcao()

        #gera Pop Inicial
        self.gerar_populacao()
        self.melhor_solucao = self.melhor_individuo()

        self.fitness_best = self.fitness(self.melhor_solucao)

        #diferença entre as médias da população atual e antiga
        while abs(self.geracao_fitness_atual - self.geracao_fitness_inicial) > self.taxa_erro_treino:

            # Armazena o média da geração
            self.geracao_fitness_inicial = self.geracao_fitness_atual

            # População Temporária
            list_childs_x = []

            #print('Criando novos filhos...')
            for j in range(int(self.tam_populacao/2)):

                parents_1 = self.sort_individuals()#Primeiros pais
                parents_2 = self.sort_individuals()#Segundos pais

                #Separa os pais de cada variável
                parents_x = [parents_1[0],parents_2[0]]


                #Probabilidade de Crossover
                if self.evoluir_taxa_crossover():
                    childs_x = self.crossover(parents_x)

                else:
                    childs_x = parents_x

                list_childs_x.extend(childs_x)

            self.pop = [list_childs_x].copy()

            self.melhor_solucao = self.melhor_individuo()

            #Calcula o fitness do melhor indivíduo da nova população
            self.fitness_best = self.fitness(self.melhor_solucao)

            self.geracoes = self.geracoes + 1

            self.decimal_x = self.BIN_DEC(self.melhor_solucao[0])


with open('arquivo.txt', 'w') as result_file:

    for i in range(tam_populacao_atual, populacao_maxima + populacao_inicial, populacao_inicial):

        taxa_crossover_atual = taxa_crossover_inicial
        pressao_sel_atual = pressao_sel_inicial


        for i in range(taxa_crossover_atual,taxa_crossover_maxima + taxa_crossover_inicial,taxa_crossover_inicial):

            pressao_sel_atual = pressao_sel_inicial

            for i in range(pressao_sel_atual, pressao_sel_maxima + pressao_sel_inicial, pressao_sel_inicial):

                geracao_init = 0

                funcao_x2 = quadratica(limite_inferior, limite_superior, precisao,tam_ps=pressao_sel_atual,tam_populacao=tam_populacao_atual,taxa_crossover=taxa_crossover_atual)

                for i in range(30):

                    funcao_x2.evoluir()

                    geracao += funcao_x2.geracoes

                    ''' impedir a influência do sinal do erro sobre o comportamento '''
                    if abs(funcao_x2.fitness(funcao_x2.melhor_solucao) - (solucao_atual)) <= funcao_x2.taxa_erro_aproximada:
                        geracao_init += 1

                if geracao_init >= 29:
                    param_pop.append(tam_populacao_atual)
                    param_crossover.append(taxa_crossover_atual)
                    param_presss_selc.append(pressao_sel_atual)

                    result_file.write('%s\n' % str(str(tam_populacao_atual) + ', ' + str(taxa_crossover_atual) + ', '+str(pressao_sel_atual) ))

                pressao_sel_atual += pressao_sel_inicial

            print('Geracao: ',geracao)
            print("Populacao Atual: ",tam_populacao_atual, "--> Crossover atual: ",taxa_crossover_atual , "--> PS atual: ",pressao_sel_atual)

            taxa_crossover_atual += taxa_crossover_inicial

        #Incrementa tamanho da população
        tam_populacao_atual += populacao_inicial

























