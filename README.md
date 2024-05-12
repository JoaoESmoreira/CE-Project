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
O **Frozen Lake** é um problema popular no domínio do aprendizagem por reforço, que oferece um excelente terreno de teste para algoritmos de decisão sequencial. Neste desafio, um agente deve aprender a atravessar um lago congelado, representado por uma matriz, para alcançar um objetivo sem cair em buracos no gelo.
O ambiente do Frozen Lake é representado como uma grade matriz onde cada célula pode ser:
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
O problema do Frozen Lake é geralmente abordado com técnicas de aprendizagem por reforço, como Q-Learning, SARSA, ou Deep Q-Networks (DQN), onde o agente aprende uma política de ação ótima através da exploração do ambiente e da experiência obtida com as recompensas de suas ações.

Neste projeto tentarei resolver o problema com recurso a técnicas de computação evolucionária.
### 💡 Contribuições
Contribuições são sempre bem-vindas! Se você tem ideias ou melhorias para o projeto, por favor, sinta-se à vontade para contribuir.

Este README fornece uma visão geral básica do problema do Frozen Lake e um ponto de partida para a implementação de soluções. Claro, cada projeto é único, então sinta-se à vontade para ajustar e expandir este projeto conforme a necessidade do seu.
# Usage
## Gerar instâncias
```shel
python3 problem.py --generate-data true
```
## Correr um programa
```shel
pypy3 problem.py --input-file data/MAP_4_BY_4/input01.txt --algorithm random
```
## Repository Structure
- **data**: Contains the dataset file(s).
- **src**: 
	- **data**: Ficheiros de input
	- **output**
		- **aco** - resultado das execuções do algoritmo *aco*
		- **qtables** - resultado das execuções do algoritmo *qtables*
		- **sea** - resultado das execuções do algoritmo *sea*
		- **stasts.** - analise das experiências
		- **ouput.txt** - ficheiro com os melhores resultados segunto as estatisticas
	- Scripts do código usado para resolver os problemas e testes
- **docs**: Documentos PDF e relatório
- **README.md**: Visão geral do projeto e instruções para execução do código.
- **requirements.txt**: Lista das dependencias das librarias de python.
# 📝 Next Steps

- [x] criar ambiente ✅ 2024-03-10
- [x] criar gerador de instâncias ✅ 2024-03-24
- [x] criar avaliador de soluçoes / ver se é existe independencia do gym para correr com o pypy ✅ 2024-03-24
- [x] criar random solution ✅ 2024-03-24
- [x] criar random com restart ✅ 2024-03-24
- [x] criar generalização do SEA e os seus métodos ✅ 2024-03-25

- [x] setup repository ✅ 2024-03-24
- [x] estou com um bug ao passar o path, é com ele que vejo se a soluçao é admissivel e esta a dar um problema gigantesco ✅ 2024-03-28
- [x] resolver o problema com componentes == passo a tomar ✅ 2024-03-28
	- [x] corrigir o problema de a soluçao nao terminar quando perde ✅ 2024-04-10
	- [x] fazer um uniforme crossover ✅ 2024-04-12
	- [x] filtrar colisões com as paredes ✅ 2024-04-11
- [x] resolver o problema com evolução de Qtables ✅ 2024-04-15
	- [x] random constructions with random restart ✅ 2024-04-12
	- [x] seleçao de pais ✅ 2024-04-15
	- [x] crossover ✅ 2024-04-15
	- [x] mutaçao ✅ 2024-04-15
- [x] impolentar o ACO 📅 2024-04-10 ✅ 2024-04-10
	- [x] melhorar a tabela das feromonas para uma lista de adjacência ✅ 2024-04-18
	- [x] visualização das feromonas ✅ 2024-04-18
- [x] Guardar informação em ficheiros csv ✅ 2024-04-30
	- [x] função de fitness geral ✅ 2024-04-30
	- [x] encontrou a solução final ✅ 2024-04-30
	- [x] diversidade ✅ 2024-04-30
	- [x] melhor individuo ✅ 2024-04-30
- [x] fazer os testes estatisticos ✅ 2024-05-05
	- [x] distribuiçao dos dados ✅ 2024-05-05
- [x] terminar o relatório ✅ 2024-05-06
# 📋 Notes

[[Evolutionary Computation]]
[[Introduction to Evolutionary Computing]]
[[Essentials of Metaheuristics]]
