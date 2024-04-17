import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Tamanho da grelha NxN
N = 5

# Matriz de feromonas inicial (pode ser uma matriz aleatória para este exemplo)
pheromones = np.random.rand(N, N, 4)

print(pheromones)
# Função para plotar o grafo com cores representando as feromonas
def plot_pheromones(pheromones):
    fig, ax = plt.subplots()

    # Função de mapeamento de cores
    colormap = cm.ScalarMappable(cmap='viridis')
    colormap.set_clim(0, np.max(pheromones))  # Define o intervalo de valores

    # Plotar linhas horizontais
    for i in range(N):
        for j in range(N-1):
            x = [i, i+1]
            y = [j+0.02, j+0.02]  # Ajuste na posição para sobreposição
            intensity = pheromones[i, j, 2]
            color = colormap.to_rgba(intensity)
            ax.plot(x, y, color=color)
    for i in range(N):
        for j in range(N-1):
            x = [i, i+1]
            y = [j-0.02, j-0.02]  # Ajuste na posição para sobreposição
            intensity = pheromones[i, j, 0]
            color = colormap.to_rgba(intensity)
            ax.plot(x, y, color=color)

    # Plotar linhas verticais
    for j in range(N):
        for i in range(N-1):
            x = [i+0.02, i+0.02]  # Ajuste na posição para sobreposição
            y = [j, j+1]
            intensity = pheromones[i, j, 1]
            color = colormap.to_rgba(intensity)
            ax.plot(x, y, color=color)

    ax.set_xlim(-0.5, N-0.5)
    ax.set_ylim(-0.5, N-0.5)
    ax.set_aspect('equal')
    ax.set_xticks(np.arange(N))
    ax.set_yticks(np.arange(N))
    ax.grid(True, linestyle='--', alpha=0.5)

    # Barra de cores
    cbar = plt.colorbar(colormap, ax=ax)
    cbar.set_label('Intensity of Pheromone')

    plt.show()

# Plotar as feromonas inicialmente
plot_pheromones(pheromones)
