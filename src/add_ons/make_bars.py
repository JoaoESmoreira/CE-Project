

import numpy as np
import matplotlib.pyplot as plt

# Verificando estilos disponíveis e escolhendo um

# Dados
# categorias = ['Q1', 'Q3', 'Q5', 'Q9']
# all_values = [3823.781, 3065.320, 3066.237, 3504.514]
# t_values = [1866.404, 1100.932, 1664.786, 2622.168]
# p_values = [2375.236, 1168.913, 1413.966, 1795.969]
# categorias = ['Q1', 'Q3', 'Q5', 'Q9']
# all_values = [3823.979, 3025.224, 3457.441, 3764.954]
# t_values   = [1898.932, 1044.221, 2062.554, 1732.832]
# p_values   = [1962.943, 1015.513, 1417.949, 1828.635]

categorias = ['Global_Q1', 'Global_Q3', 'Global_Q5', 'Global_Q9', 'Local_Q1', 'Local_Q3', 'Local_Q5', 'Local_Q9']
all_values = [3823.979, 3025.224, 3457.441, 3764.954, 8898.832, 12254.764, 5084.585, 5992.403]
t_values   = [1898.932, 1044.221, 2062.554, 1732.832, 10813.889, 9546.714, 8478.289, 6876.620]
p_values   = [1962.943, 1015.513, 1417.949, 1828.635, 9783.804, 8119.028, 7013.569, 5594.323]  


# Definindo a largura das barras
barWidth = 0.25

# Definindo a posição das barras
r1 = np.arange(len(all_values))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]

# Configurando o tamanho da figura
plt.figure(figsize=(10, 6))

# Criando as barras
plt.bar(r1, all_values, color='#1f77b4', width=barWidth, edgecolor='grey', label='all')
plt.bar(r2, t_values, color='#ff7f0e', width=barWidth, edgecolor='grey', label='t')
plt.bar(r3, p_values, color='#2ca02c', width=barWidth, edgecolor='grey', label='p')

# Adicionando legendas, títulos e ajustando as fontes
plt.xlabel('Categoria', fontweight='bold', fontsize=14)
plt.ylabel('Valores', fontweight='bold', fontsize=14)
plt.title('Comparação dos Valores Globais com os Locais', fontweight='bold', fontsize=16)
plt.xticks([r + barWidth for r in range(len(all_values))], categorias, fontsize=12)
plt.yticks(fontsize=12)

# Adicionando a grade e a legenda
plt.grid(True, which='major', linestyle='--', linewidth=0.5)
plt.legend(fontsize=12)

# Mostrar o gráfico
plt.show()

