import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.report.base_visualizer import BaseVisualizer
from src.analysis.statistical_tests import StatisticalTests

class StatisticalTestsVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações baseadas nos resultados dos testes estatísticos.
    """

    def __init__(self, df, output_dir="visualizations"):
        """
        Inicializa a instância com um DataFrame e o diretório de saída para salvar os gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as variáveis para os testes estatísticos.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Herda o construtor da classe BaseVisualizer
        self.tests = StatisticalTests(df)  # Instancia StatisticalTests com o DataFrame

    def plot_gender_salary_comparison(self, test="t-test"):
        """
        Gera um gráfico de barras para comparar salários médios entre homens e mulheres.

        Parameters:
            test (str): O teste estatístico a ser realizado:
                        - "t-test": Teste t de Student.
                        - "mann-whitney": Mann-Whitney U Test.
        """
        # Executa o teste estatístico
        result = self.tests.compare_gender_salaries(test=test)

        # Calcula os salários médios por gênero
        male_salary = self.tests.df[self.tests.df['sexo'] == 'Masculino']['valor_remuneracao_media'].mean()
        female_salary = self.tests.df[self.tests.df['sexo'] == 'Feminino']['valor_remuneracao_media'].mean()

        # Dados para o gráfico
        genders = ['Masculino', 'Feminino']
        salaries = [male_salary, female_salary]

        plt.figure(figsize=(8, 6))
        sns.barplot(x=genders, y=salaries, palette="coolwarm")
        plt.title(f"Comparação Salarial por Gênero ({result['Teste']})")
        plt.ylabel("Salário Médio")
        plt.xlabel("Gênero")
        plt.annotate(
            f"Valor-p: {result['Valor-p']:.4f}",
            xy=(0.5, max(salaries) * 0.95),
            xycoords="axes fraction",
            ha="center",
            fontsize=12,
            color="black",
        )
        plt.tight_layout()
        self.save_plot(f"gender_salary_comparison_{test}.png")

    def plot_anova_by_region(self):
        """
        Gera um gráfico de caixa comparando salários entre diferentes estados.
        """
        # Executa o teste ANOVA
        result = self.tests.anova_salary_by_region()

        # Dados para o gráfico
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='sigla_uf', y='valor_remuneracao_media', data=self.tests.df, palette="viridis")
        plt.title(f"Comparação Salarial entre Estados (ANOVA)\nValor-p: {result['Valor-p']:.4f}")
        plt.ylabel("Salário Médio")
        plt.xlabel("Estado")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot("anova_salary_by_region.png")

    def plot_anova_by_sector(self):
        """
        Gera um gráfico de caixa comparando salários entre diferentes setores econômicos.
        """
        # Executa o teste ANOVA
        result = self.tests.anova_salary_by_sector()

        # Dados para o gráfico
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='subsetor_ibge', y='valor_remuneracao_media', data=self.tests.df, palette="magma")
        plt.title(f"Comparação Salarial entre Setores (ANOVA)\nValor-p: {result['Valor-p']:.4f}")
        plt.ylabel("Salário Médio")
        plt.xlabel("Setor Econômico")
        plt.xticks(rotation=45)
        plt.tight_layout()
        self.save_plot("anova_salary_by_sector.png")