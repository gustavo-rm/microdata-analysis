

# 🧮 **Microdata Analysis Project**

Análise de microdados do mercado de trabalho focado em ocupações tecnológicas. Este projeto utiliza um pipeline de análise completo, incluindo carregamento, limpeza, visualização de dados e aplicação de modelos preditivos e testes estatísticos.

---

## 📂 **Estrutura do Projeto**

```plaintext
project/
│
├── data/                     # Dados brutos e processados
│   ├── raw/                  # Dados originais
│   │   └── microdados.csv
│   ├── processed/            # Dados processados
│
├── output/                   # Resultados do projeto (gráficos, relatórios)
│
├── src/                      # Código-fonte principal
│   ├── analysis/             # Classes de análise
│   │   ├── basic_statistics.py
│   │   ├── employment_indexes.py
│   │   ├── gender_analysis.py
│   │   ├── position_analysis.py
│   │   ├── predictive_models.py
│   │   ├── regional_analysis.py
│   │   └── statistical_tests.py
│   ├── data/                 # Classes para manipulação de dados
│   │   ├── data_filter.py
│   │   ├── data_loader.py
│   │   └── __init__.py
│   ├── report/               # Visualizadores e gerador de relatórios
│   │   ├── base_visualizer.py
│   │   ├── basic_statistics_visualizer.py
│   │   ├── employment_indexes_visualizer.py
│   │   ├── gender_analysis_visualizer.py
│   │   ├── position_analysis_visualizer.py
│   │   ├── predictive_models_visualizer.py
│   │   ├── statistical_tests_visualizer.py
│   │   ├── report_generator.py
│   │   └── __init__.py
│   ├── config.py             # Configuração do projeto
│   └── __init__.py
│
├── main.py                   # Arquivo principal para execução do projeto
├── README.md                 # Documentação do projeto
```

---

## **📥 Dados de Entrada**

Os dados foram extraídos do **BigQuery** com a consulta abaixo. A tabela utilizada foi `basedosdados.br_me_rais.microdados_vinculos`, acessível por meio da plataforma [Basedosdados](https://console.cloud.google.com/bigquery?p=basedosdados&d=br_me_rais&t=microdados_vinculos&page=table).

### **Consulta Utilizada**
```sql
WITH 
dicionario_tipo_vinculo AS (
    SELECT
        chave AS chave_tipo_vinculo,
        valor AS descricao_tipo_vinculo
    FROM `basedosdados.br_me_rais.dicionario`
    WHERE
        TRUE
        AND nome_coluna = 'tipo_vinculo'
        AND id_tabela = 'microdados_vinculos'
),
-- Outras tabelas para dicionários de códigos...
SELECT
    dados.ano AS ano,
    dados.sigla_uf AS sigla_uf,
    diretorio_sigla_uf.nome AS sigla_uf_nome,
    dados.id_municipio AS id_municipio,
    diretorio_id_municipio.nome AS id_municipio_nome,
    descricao_tipo_vinculo AS tipo_vinculo,
    dados.valor_remuneracao_media AS valor_remuneracao_media,
    dados.cbo_2002 AS cbo_2002,
    diretorio_cbo_2002.descricao AS cbo_2002_descricao,
    dados.idade AS idade,
    descricao_sexo AS sexo
FROM `basedosdados.br_me_rais.microdados_vinculos` AS dados
LEFT JOIN (SELECT DISTINCT sigla, nome FROM `basedosdados.br_bd_diretorios_brasil.uf`) AS diretorio_sigla_uf
    ON dados.sigla_uf = diretorio_sigla_uf.sigla
LEFT JOIN (SELECT DISTINCT id_municipio, nome FROM `basedosdados.br_bd_diretorios_brasil.municipio`) AS diretorio_id_municipio
    ON dados.id_municipio = diretorio_id_municipio.id_municipio
LEFT JOIN (SELECT DISTINCT cbo_2002, descricao FROM `basedosdados.br_bd_diretorios_brasil.cbo_2002`) AS diretorio_cbo_2002
    ON dados.cbo_2002 = diretorio_cbo_2002.cbo_2002
LEFT JOIN `dicionario_tipo_vinculo`
    ON dados.tipo_vinculo = chave_tipo_vinculo
LEFT JOIN `dicionario_sexo`
    ON dados.sexo = chave_sexo
WHERE
    (dados.cbo_2002 LIKE '2123%' OR
     dados.cbo_2002 LIKE '2124%' OR
     dados.cbo_2002 LIKE '1236%' OR
     dados.cbo_2002 LIKE '1425%' OR
     dados.cbo_2002 LIKE '3172%' OR
     dados.cbo_2002 LIKE '3171%')
    AND dados.sigla_uf LIKE 'PR'
    AND dados.idade BETWEEN 18 AND 64;
```

---

## 🚀 **Recursos Principais**

### 🧩 **Análises**
- **BasicStatistics**: Estatísticas descritivas básicas.
- **GenderAnalysis**: Análise de disparidade salarial por gênero.
- **PositionAnalysis**: Frequência e distribuição de cargos tecnológicos.
- **PredictiveModels**: Modelos de Regressão Linear e Logística.
- **EmploymentIndexes**: Índices de disparidade salarial e escolaridade.
- **RegionalAnalysis**: Concentração de empregos tecnológicos por região.
- **StatisticalTests**: Testes estatísticos (ANOVA, t-test).

### 📊 **Visualizadores**
- Histogramas, boxplots e gráficos de barras para estatísticas descritivas.
- Nuvens de palavras e gráficos de frequência de cargos.
- Mapas geográficos para visualização de concentração de empregos.
- Heatmaps de correlação entre variáveis.

---

## 🛠️ **Tecnologias Utilizadas**

- **Linguagem**: Python 3.9
- **Bibliotecas**:
  - Manipulação de dados: `pandas`, `numpy`
  - Visualização: `matplotlib`, `seaborn`, `wordcloud`
  - Modelagem estatística: `scikit-learn`, `scipy`
  - Manipulação de dados públicos: `basedosdados`

---

## 🗂️ **Como Configurar o Ambiente**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/microdata-analysis.git
   cd microdata-analysis
   ```

2. **Crie um ambiente virtual e ative-o:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Para Linux/Mac
   .venv\Scripts\activate     # Para Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🔑 **Como Executar**

1. Coloque o arquivo de dados original em `data/raw/microdados.csv`.

2. Execute o arquivo principal:
   ```bash
   python main.py
   ```

3. Os gráficos e relatórios gerados serão salvos em `output/`.

---

## 📈 **Exemplo de Gráficos Gerados**

### 📊 Estatísticas Básicas
![Gráfico de métricas salariais](output/metrics_bar_chart.png)

### 🌍 Top 15 Cargos
![Mapa de concentração regional](output/top_15_positions.png)

### 📑 Disparidade Salarial por Gênero
![Gráfico de disparidade por gênero](output/gender_salary_gap.png)

---

## 🛡️ **Contribuição**

1. Faça um fork do repositório.
2. Crie uma branch para sua contribuição:
   ```bash
   git checkout -b feature/nova-analise
   ```
3. Envie um pull request!

---

## 📜 **Licença**

Este projeto está licenciado sob a licença **MIT**.

---
