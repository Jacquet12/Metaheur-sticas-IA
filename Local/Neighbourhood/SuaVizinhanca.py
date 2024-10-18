import math

from Local.Neighbourhood.Vizinhanca import Vizinhanca
from Solucao import Solucao


# Discente: Jacquet Leme

class VizinhancaSwap(Vizinhanca):
    def __init__(self, distancias: tuple[tuple[int]]):
        super().__init__("swap", distancias, 2)  # Tipo swap, 2 elementos trocados

    # Método que computa e retorna a qualidade da solução vizinha
    # Considera a mudança na qualidade da solução atual a partir da troca de dois elementos
    def computar_qualidade(self, solucao: Solucao, i: int, j: int) -> int:
        qualidade = solucao.qualidade
        elemento_pre_i, elemento_i, elemento_pos_i, elemento_pre_j, elemento_j, elemento_pos_j = solucao.retornar_elementos(i, j)

        # Calcula a diferença de qualidade ao trocar os elementos i e j
        if i < j:
            qualidade += - self.distancias[elemento_i][elemento_pre_i] - self.distancias[elemento_i][elemento_pos_i] \
                         - self.distancias[elemento_j][elemento_pre_j] - self.distancias[elemento_j][elemento_pos_j] \
                         + self.distancias[elemento_j][elemento_pre_i] + self.distancias[elemento_j][elemento_pos_i] \
                         + self.distancias[elemento_i][elemento_pre_j] + self.distancias[elemento_i][elemento_pos_j]
        else:
            qualidade += - self.distancias[elemento_i][elemento_pre_i] - self.distancias[elemento_i][elemento_pos_i] \
                         - self.distancias[elemento_j][elemento_pre_j] - self.distancias[elemento_j][elemento_pos_j] \
                         + self.distancias[elemento_j][elemento_pre_i] + self.distancias[elemento_j][elemento_pos_i] \
                         + self.distancias[elemento_i][elemento_pre_j] + self.distancias[elemento_i][elemento_pos_j]

        return qualidade

    # Aplica a troca de dois elementos na solução atual e retorna o novo ciclo
    @staticmethod
    def gerar_novo_ciclo(solucao: Solucao, i: int, j: int) -> list:
        novo_ciclo = solucao.ciclo[:]
        novo_ciclo[i], novo_ciclo[j] = novo_ciclo[j], novo_ciclo[i]  # Troca os elementos i e j
        return novo_ciclo

    # Retorna a melhor solução da vizinhança, ou seja, com a melhor qualidade após a troca
    def melhor_vizinho(self, solucao: Solucao, tabu: set) -> Solucao:
        melhor_qualidade = math.inf
        imelhor = -1
        jmelhor = -1
        for i in range(self.tamanho - 1):
            if solucao.ciclo[i] not in tabu:
                for j in range(i + 1, self.tamanho):
                    if solucao.ciclo[j] not in tabu:
                        qualidade = self.computar_qualidade(solucao, i, j)
                        if qualidade < melhor_qualidade:
                            melhor_qualidade = qualidade
                            imelhor = i
                            jmelhor = j
        return Solucao(melhor_qualidade, self.gerar_novo_ciclo(solucao, imelhor, jmelhor), solucao.ciclo[imelhor], solucao.ciclo[jmelhor])

    # Retorna o primeiro vizinho que seja melhor que a solução atual
    def primeiro_vizinho_melhor(self, solucao: Solucao, tabu: set) -> Solucao:
        melhor_qualidade = solucao.qualidade
        for i in range(self.tamanho - 1):
            if solucao.ciclo[i] not in tabu:
                for j in range(i + 1, self.tamanho):
                    if solucao.ciclo[j] not in tabu:
                        qualidade = self.computar_qualidade(solucao, i, j)
                        if qualidade < melhor_qualidade:
                            return Solucao(qualidade, self.gerar_novo_ciclo(solucao, i, j), i, j)
        return solucao
