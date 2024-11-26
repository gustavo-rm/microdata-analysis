import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from src.report.base_visualizer import BaseVisualizer
from src.analysis.basic_statistics import BasicStatistics

class BasicStatisticsVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações com base nas estatísticas calculadas pela classe BasicStatistics.
    """

    def __init__(self, df, output_dir="output"):
        """
        Inicializa a instância com um DataFrame e herda a funcionalidade de salvar gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações de empregados.
            output_dir (str): Diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Chama o construtor da classe base
        self.df = df

    def save_plot(self, filename):
        """
        Salva o gráfico atual no diretório especificado.

        Parameters:
            filename (str): Nome do arquivo onde o gráfico será salvo.
        """
        import os
        os.makedirs(self.output_dir, exist_ok=True)  # Cria o diretório, se não existir
        plt.savefig(os.path.join(self.output_dir, filename), format="png", dpi=300)
        plt.close()  # Fecha o gráfico para liberar memória

    import matplotlib.ticker as mticker

    def plot_average_salary_by_year(self):
        """
        Gera um gráfico de linha mostrando a média salarial por ano e salva o gráfico.
        """
        stats = BasicStatistics(self.df)
        salary_by_year = stats.calculate_average_salary_by_year()

        plt.figure(figsize=(12, 6))
        sns.lineplot(data=salary_by_year, x='Ano', y='Média Salarial', marker='o', color='blue')

        # Configurar o título e os rótulos
        plt.title("Média Salarial por Ano")
        plt.xlabel("Ano")
        plt.ylabel("Média Salarial")

        # Garantir que os valores do eixo X sejam inteiros
        ax = plt.gca()
        ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

        # Adicionar grade e layout
        plt.grid(True)
        plt.tight_layout()

        self.save_plot("average_salary_by_year.png")

    def plot_salary_distribution(self):
        """
        Gera um histograma para visualizar a distribuição salarial e salva o gráfico.
        """
        stats = BasicStatistics(self.df).salary_distribution()
        mean_salary = stats['Média Salarial']
        median_salary = stats['Mediana Salarial']

        plt.figure(figsize=(12, 6))
        sns.histplot(self.df['valor_remuneracao_media'], bins=30, kde=True, color='skyblue')
        plt.axvline(mean_salary, color='red', linestyle='--', label=f'Média: {mean_salary:.2f}')
        plt.axvline(median_salary, color='green', linestyle='--', label=f'Mediana: {median_salary:.2f}')
        plt.title("Distribuição Salarial")
        plt.xlabel("Salário")
        plt.ylabel("Frequência")
        plt.legend()

        self.save_plot("salary_distribution.png")

    def plot_salary_boxplot(self):
        """
        Gera um boxplot para visualizar a dispersão e identificar outliers nos salários, e salva o gráfico.
        """
        plt.figure(figsize=(8, 6))
        sns.boxplot(x=self.df['valor_remuneracao_media'], color='lightblue')
        plt.title("Boxplot da Distribuição Salarial")
        plt.xlabel("Salário")

        self.save_plot("salary_boxplot.png")

    def plot_metrics_bar_chart(self):
        """
        Gera um gráfico de barras para comparar as métricas calculadas e salva o gráfico.
        """
        # Obter as métricas
        stats = BasicStatistics(self.df).salary_distribution()

        metrics = {
            "Média\nSalarial": stats['Média Salarial'],
            "Mediana\nSalarial": stats['Mediana Salarial'],
            "Desvio\nPadrão": stats['Desvio Padrão'],
            "Coeficiente de\nVariação (%)": stats['Coeficiente de Variação (%)']
        }

        # Criar o gráfico
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(metrics.keys()), y=list(metrics.values()), palette="viridis")
        plt.title("Comparação de Métricas Salariais")
        plt.ylabel("Valor")

        # Ajustar os rótulos do eixo x com quebra de linha
        plt.xticks(rotation=0)  # Mantém os rótulos alinhados
        plt.tight_layout()  # Ajusta o layout para evitar cortes

        # Salvar o gráfico
        self.save_plot("metrics_bar_chart.png")

    def plot_cumulative_distribution(self):
        """
        Gera um gráfico de distribuição cumulativa (ECDF) para os salários e salva o gráfico.
        """
        sorted_salaries = self.df['valor_remuneracao_media'].sort_values()
        cumulative = sorted_salaries.rank(pct=True)

        plt.figure(figsize=(12, 6))
        plt.plot(sorted_salaries, cumulative, marker='.', linestyle='none', color='blue')
        plt.title("Distribuição Cumulativa de Salários (ECDF)")
        plt.xlabel("Salário")
        plt.ylabel("Proporção Acumulada")
        plt.grid()

        self.save_plot("cumulative_distribution.png")
