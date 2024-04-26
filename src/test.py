

from itertools import combinations
from scipy.stats import wilcoxon
import pandas as pd
import os

arquivos_csv = []
for dirname, _, filenames in os.walk('./output/aco/dim12'):
    aux = []
    for filename in filenames:
        path = os.path.join(dirname, filename)
        aux.append(path)
arquivos_csv.extend(aux)

# Calcular a média da "fitness" para cada configuração
medias_fitness = []
for arquivo in arquivos_csv:
    dados = pd.read_csv(arquivo)
    media_fitness = dados["fitness"].mean()
    medias_fitness.append((arquivo, media_fitness))

# Realizar o teste de Wilcoxon para todas as combinações de pares
for i, j in combinations(range(len(medias_fitness)), 2):
    config_a, media_a = medias_fitness[i]
    config_b, media_b = medias_fitness[j]
    
    # Carregar dados
    dados_a = pd.read_csv(config_a)["fitness"]
    dados_b = pd.read_csv(config_b)["fitness"]
    
    # Verificar e ajustar o tamanho dos conjuntos de dados, se necessário
    min_len = min(len(dados_a), len(dados_b))
    dados_a = dados_a[:min_len]
    dados_b = dados_b[:min_len]
    
    # Realizar o teste de Wilcoxon unicaudal à esquerda (left-tailed)
    stat, p = wilcoxon(dados_a, dados_b)

    # Avaliar o resultado
    print(f"Comparando {config_a} e {config_b}:")
    print("Estatística de Wilcoxon:", stat)
    print("Valor p (unicaudal à esquerda):", p)

    # Interpretar o resultado
    if p < 0.05:
        print("Diferença estatisticamente significativa. Uma configuração é melhor que a outra.")
        if media_a < media_b:  # Aqui mudamos a comparação de maior para menor, já que agora é um teste à esquerda
            print(f"{config_a} tem uma média de fitness menor (o que é considerado melhor para um teste à esquerda).")
        else:
            print(f"{config_b} tem uma média de fitness menor (o que é considerado melhor para um teste à esquerda).")
    else:
        print("Não há diferença estatisticamente significativa entre as configurações.")
    print()

# Encontrar a configuração com a maior média de "fitness"
melhor_configuracao = max(medias_fitness, key=lambda x: x[1])

print("Melhor configuração:")
print("Arquivo:", melhor_configuracao[0])
print("Média da fitness:", melhor_configuracao[1])