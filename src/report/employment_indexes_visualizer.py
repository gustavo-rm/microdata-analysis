from src.report.base_visualizer import BaseVisualizer
from src.analysis.employment_indexes import EmploymentIndexes
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class EmploymentIndexesVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações dos índices calculados pela classe EmploymentIndexes.
    """

    def __init__(self, df, output_dir="output"):
        """
        Inicializa a instância com um DataFrame e herda a funcionalidade de salvar gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações de salários, região e escolaridade.
            output_dir (str): Diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Chama o construtor da classe base
        self.df = df

    def plot_salary_disparity(self):
        """
        Gera um gráfico de barras para mostrar a disparidade salarial entre gêneros.
        """
        # Obter as médias salariais por gênero
        salaries = self.df.groupby('sexo')['valor_remuneracao_media'].mean().reset_index()

        # Renomear as colunas para facilitar a interpretação
        salaries.columns = ['Gênero', 'Salário Médio']

        # Criar uma categoria genérica para o parâmetro `hue`
        salaries['Categoria'] = 'Salários por Gênero'

        # Configurar o gráfico
        plt.figure(figsize=(8, 6))
        sns.barplot(
            data=salaries,
            x='Gênero',
            y='Salário Médio',
            hue='Categoria',  # Categoria genérica para demonstrar uso de `hue`
            palette="Blues"
        )

        # Configurações do gráfico
        plt.title("Disparidade Salarial entre Gêneros")
        plt.ylabel("Salário Médio")
        plt.xlabel("Gênero")
        plt.legend(title="Categoria", loc="upper right")
        plt.tight_layout()

        # Salvar o gráfico
        self.save_plot("salary_disparity.png")

    def plot_regional_concentration(self):
        """
        Gera um gráfico de barras mostrando a concentração regional de empregos tecnológicos.
        """
        indexes = EmploymentIndexes(self.df)
        states = self.df['sigla_uf'].unique()

        icr_values = {state: indexes.regional_concentration_index(state) for state in states}

        plt.figure(figsize=(12, 8))
        sns.barplot(x=list(icr_values.keys()), y=list(icr_values.values()), palette="Greens")
        plt.title("Índice de Concentração Regional")
        plt.ylabel("Proporção de Empregos (%)")
        plt.xlabel("Estado")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot("regional_concentration.png")

    def plot_education_index(self):
        """
        Gera um gráfico de pizza mostrando a proporção de empregados com ensino superior completo ou mais.
        """
        indexes = EmploymentIndexes(self.df)
        education_index = indexes.education_index()
        non_education_index = 100 - education_index

        labels = ['Ensino Superior ou Mais', 'Outros Níveis de Escolaridade']
        values = [education_index, non_education_index]

        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct="%1.1f%%", colors=["#66b3ff", "#ff9999"], startangle=140)
        plt.title("Índice de Escolaridade")
        plt.tight_layout()
        self.save_plot("education_index.png")
