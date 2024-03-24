---
Start: 2024-03-06 11:17
DeadLine: 2024-05-13
Status:
  - Active
Priority: 
tags:
  - EvolutionaryComputation
Arquive: false
End: 
Author: João E. Moreira
---

---
# 📔 Description
## Frozen Lake Problem
O **Frozen Lake** é um problema popular no domínio do aprendizado por reforço, que oferece um excelente terreno de teste para algoritmos de decisão sequencial. Neste desafio, um agente deve aprender a atravessar um lago congelado, representado por uma grade, para alcançar um objetivo sem cair em buracos no gelo.
### 🧊 Sobre o Frozen Lake
O **Frozen Lake** é um problema popular no domínio do aprendizado por reforço, que oferece um excelente terreno de teste para algoritmos de decisão sequencial. Neste desafio, um agente deve aprender a atravessar um lago congelado, representado por uma grade, para alcançar um objetivo sem cair em buracos no gelo.
O ambiente do Frozen Lake é representado como uma grade quadrada onde cada célula pode ser:
- **S (Start)**: o ponto de partida do agente.
- **F (Frozen)**: superfície congelada segura para o agente caminhar.
- **H (Hole)**: buracos no gelo, onde se o agente cair, o episódio termina.
- **G (Goal)**: o destino final do agente.

O objetivo é criar um agente que aprenda a navegar do ponto de partida até o objetivo sem cair em buracos, apenas caminhando sobre a superfície congelada. O desafio é realizado sob incerteza, pois os movimentos do agente podem não resultar sempre na direção pretendida devido ao gelo escorregadio.
Os movimentos permitidos são:
- **0 (Left)**: o ponto de partida do agente.
- **1 (Down)**: superfície congelada segura para o agente caminhar.
- **2 (Right)**: buracos no gelo, onde se o agente cair, o episódio termina.
- **3 (Up)**: o destino final do agente.
### 🤖 Como o Agente Aprende
O problema do Frozen Lake é geralmente abordado com técnicas de aprendizado por reforço, como Q-Learning, SARSA, ou Deep Q-Networks (DQN), onde o agente aprende uma política de ação ótima através da exploração do ambiente e da experiência obtida com as recompensas de suas ações.

Neste projeto tentarei resolver o problema com recurso a técnicas de computação evolucionária.
### 💡 Contribuições
Contribuições são sempre bem-vindas! Se você tem ideias ou melhorias para o projeto, por favor, sinta-se à vontade para contribuir.

Este README fornece uma visão geral básica do problema do Frozen Lake e um ponto de partida para a implementação de soluções. Claro, cada projeto é único, então sinta-se à vontade para ajustar e expandir este template conforme a necessidade do seu projeto.

# Usage
## Gerar instâncias
```shel
python3 problem.py --generate-data true
```

## Correr um programa
```shel
pypy3 problem.py --input-file data/MAP_4_BY_4/input01.txt --algorithm random
```

# 📝 Next Steps

- [x] criar ambiente ✅ 2024-03-10
- [x] criar gerador de instâncias ✅ 2024-03-24
- [x] criar avaliador de soluçoes / ver se é existe independencia do gym para correr com o pypy ✅ 2024-03-24
- [x] criar random solution ✅ 2024-03-24
- [x] criar random com restart ✅ 2024-03-24
- [ ] criar generalização do SEA e os seus métodos

- [x] setup repository ✅ 2024-03-24
# 📋 Notes

> [!danger]
> É suposto fazer este projeto no sentido de querer publicar um paper.
> Sendo assim o formato e a estrutura do relatório devem seguir esse formato.

> [!danger]
> Nao inventes, é para fazer evolucionário!!

Deve ser experimentadas várias fitness functions.


