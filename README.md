# 📊 Dashboard Estatístico

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Shiny for Python](https://img.shields.io/badge/Shiny_for_Python-0.10%2B-blueviolet)](https://shiny.posit.co/py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Dashboard interativo desenvolvido com **Shiny for Python** para análise estatística de dados, como atividade avaliativa da disciplina de Estatística — Universidade Federal Rural de Pernambuco (UFRPE).
---

## 👤 Autor

**Caio César Farias da Silva**
Universidade Federal Rural de Pernambuco — UFRPE

---

## 🎥 Vídeo Explicativo

🔗 [Link do YouTube](https://www.youtube.com/watch?v=aATMCj8k5wk)

---

## Funcionalidades

### 01 — Análise Descritiva
- Upload de arquivo CSV pelo usuário
- Seleção de variável quantitativa
- Histograma com linhas de média e mediana
- Boxplot interativo
- Estatísticas: média, mediana, desvio-padrão, n, mínimo e máximo

### 02 — Teste de Hipóteses para a Média
- Teste Z com variância populacional conhecida
- Variância calculada automaticamente da amostra ou informada manualmente
- Tipos de teste: bilateral, unilateral à direita, unilateral à esquerda
- Controles deslizantes para μ₀ e nível de significância (α)
- Visualização da curva normal com regiões críticas
- Legenda das variáveis do dataset (Body Performance)

### 03 — Intervalo de Confiança Normal
- Intervalo de confiança para a média populacional
- Nível de confiança ajustável via slider (0,80 a 0,99)
- Exibe limite inferior, limite superior e nível de confiança utilizado

### 04 — Regressão Linear Simples
- Upload simultâneo de múltiplos datasets
- Seleção do dataset ativo e das variáveis X e Y
- Coeficientes R, R² e equação da reta ajustada
- Gráfico de dispersão com reta de regressão
- Interpretação automática dos coeficientes

---

## 🗂️ Estrutura do Projeto

```
dashboard-estatistica/
├── app.py                   # Entrada principal da aplicação
├── styles.py                # Paleta de cores e CSS compartilhado
├── tab_01_descritiva.py     # Análise descritiva
├── tab_02_hipoteses.py      # Teste de hipóteses
├── tab_03_ic.py             # Intervalo de confiança
├── tab_04_regressao.py      # Regressão linear simples
└── data/
    ├── 01_iris.csv
    ├── 02_bodyPerformance_800_sample.csv
    └── 03_housing.csv
```

---

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/dashboard-estatistica.git
cd dashboard-estatistica
pip install -r requirements.txt
shiny run app.py
```

---

## 🗃️ Datasets utilizados

### 🌸 Iris
Dataset clássico que contém medidas morfológicas de 150 flores de íris — comprimento e largura de sépalas e pétalas — distribuídas em três espécies: *Iris setosa*, *Iris versicolor* e *Iris virginica*. Utilizado na aba de **Análise Descritiva**.

🔗 [Kaggle — Iris Dataset](https://www.kaggle.com/datasets/uciml/iris)

---

### 🏋️ Body Performance
Contém dados de avaliação física de 13.393 indivíduos, incluindo idade, altura, peso, percentual de gordura corporal, pressão arterial, força de preensão manual, flexibilidade, abdominais e salto em distância. Utilizado na aba de **Teste de Hipóteses**.

🔗 [Kaggle — Body Performance Data](https://www.kaggle.com/datasets/kukuroo3/body-performance-data)

#### Pré-processamento realizado no RStudio

Os dados foram exportados para o RStudio para verificação prévia e limpeza. Foram removidas linhas com valores zerados nas variáveis de pressão arterial (`diastolic` e `systolic`) e força de preensão (`gripForce`), que são fisiologicamente inviáveis e indicam erro de registro. Em seguida, foi extraída uma amostra aleatória de 800 observações com semente fixa para garantir reprodutibilidade:

```r
dados <- read.csv(file.choose())

# Remoção de zeros inviáveis
dados <- dados[dados$diastolic != 0, ]
dados <- dados[dados$gripForce != 0, ]

# Amostragem
set.seed(42)
amostra <- dados[sample(nrow(dados), 800), ]

write.csv(amostra, "02_bodyPerformance_800_sample.csv", row.names = FALSE)
```

A redução para 800 observações foi necessária para tornar os resultados do teste Z mais adequados para fins didáticos, reduzindo o efeito do tamanho amostral sobre a estatística.

---

### 🏠 California Housing
Reúne dados censitários de distritos residenciais do estado da Califórnia, coletados no censo de 1990. Cada linha representa um distrito e traz informações como número de cômodos, número de quartos, população, número de domicílios, renda mediana e valor mediano dos imóveis. Utilizado nas abas de **Intervalo de Confiança** e **Regressão Linear**.

🔗 [Kaggle — California Housing Prices](https://www.kaggle.com/datasets/camnugent/california-housing-prices)
---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
