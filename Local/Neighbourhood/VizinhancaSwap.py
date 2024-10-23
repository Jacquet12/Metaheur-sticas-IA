import random
from Solucao import Solucao
from Local.Neighbourhood.Vizinhanca import Vizinhanca


class VizinhancaSwap(Vizinhanca):
    def __init__(self, distancias: tuple[tuple[int]]):
        super().__init__("swap", distancias, 2)  # Tipo swap, 2 elementos trocados

    def computar_qualidade(self, solucao: Solucao, i: int, j: int) -> int:
        qualidade = solucao.qualidade
        tamanho = len(solucao.ciclo)
        
        # Garantir que os elementos anteriores e posteriores existem, fazendo ajuste circular
        elemento_pre_i = solucao.ciclo[i - 1] if i > 0 else solucao.ciclo[-1]
        elemento_pos_i = solucao.ciclo[i + 1] if i < tamanho - 1 else solucao.ciclo[0]
        elemento_pre_j = solucao.ciclo[j - 1] if j > 0 else solucao.ciclo[-1]
        elemento_pos_j = solucao.ciclo[j + 1] if j < tamanho - 1 else solucao.ciclo[0]

        elemento_i = solucao.ciclo[i]
        elemento_j = solucao.ciclo[j]

        # Calcula a diferença de qualidade ao trocar os elementos i e j
        qualidade += (- self.distancias[elemento_i][elemento_pre_i] - self.distancias[elemento_i][elemento_pos_i] 
              - self.distancias[elemento_j][elemento_pre_j] - self.distancias[elemento_j][elemento_pos_j] 
              + self.distancias[elemento_j][elemento_pre_i] + self.distancias[elemento_j][elemento_pos_i] 
              + self.distancias[elemento_i][elemento_pre_j] + self.distancias[elemento_i][elemento_pos_j])

        return qualidade

    @staticmethod
    def gerar_novo_ciclo(solucao: Solucao, i: int, j: int) -> list:
        # Realiza a troca dos elementos i e j de maneira eficiente
        novo_ciclo = solucao.ciclo[:]
        novo_ciclo[i], novo_ciclo[j] = novo_ciclo[j], novo_ciclo[i]
        return novo_ciclo

    # Retorna a melhor solução da vizinhança, com uma amostragem limitada para reduzir a complexidade
    def melhor_vizinho(self, solucao: Solucao, tabu: set) -> Solucao:
        self.tamanho = len(solucao.ciclo)
        melhor_qualidade = solucao.qualidade
        imelhor = -1
        jmelhor = -1

        # Gera uma amostragem aleatória de vizinhos para testar
        vizinhos = [(i, j) for i in range(self.tamanho - 1) for j in range(i + 1, self.tamanho) if solucao.ciclo[i] not in tabu and solucao.ciclo[j] not in tabu]
        amostra_vizinhos = random.sample(vizinhos, min(100, len(vizinhos)))  # Testa no máximo 100 vizinhos

        for i, j in amostra_vizinhos:
            qualidade = self.computar_qualidade(solucao, i, j)
            if qualidade < melhor_qualidade:
                melhor_qualidade = qualidade
                imelhor = i
                jmelhor = j

        # Se uma melhoria foi encontrada
        if imelhor != -1 and jmelhor != -1:
            novo_ciclo = self.gerar_novo_ciclo(solucao, imelhor, jmelhor)
            return Solucao(melhor_qualidade, novo_ciclo, solucao.ciclo[imelhor], solucao.ciclo[jmelhor])

        # Retorna a solução original se nenhuma melhoria foi encontrada
        return solucao

    # Retorna o primeiro vizinho que seja melhor que a solução atual (parada antecipada)
    def primeiro_vizinho_melhor(self, solucao: Solucao, tabu: set) -> Solucao:
        self.tamanho = len(solucao.ciclo)
        melhor_qualidade = solucao.qualidade

        # Gera uma amostragem aleatória de vizinhos para testar
        vizinhos = [(i, j) for i in range(self.tamanho - 1) for j in range(i + 1, self.tamanho) if solucao.ciclo[i] not in tabu and solucao.ciclo[j] not in tabu]
        amostra_vizinhos = random.sample(vizinhos, min(100, len(vizinhos)))

        for i, j in amostra_vizinhos:
            qualidade = self.computar_qualidade(solucao, i, j)
            if qualidade < melhor_qualidade:
                novo_ciclo = self.gerar_novo_ciclo(solucao, i, j)
                return Solucao(qualidade, novo_ciclo, i, j)

        # Retorna a solução original se não houver vizinhos melhores
        return solucao
