import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.analysis.regional_analysis import RegionalAnalysis
from src.report.base_visualizer import BaseVisualizer


class RegionalAnalysisVisualizer(BaseVisualizer):
    """
    Classe para visualização de análises regionais.
    """

    def __init__(self, df, output_dir="output/regional_analysis"):
        """
        Inicializa a instância com o DataFrame e o diretório de saída.

        Parameters:
            df (pd.DataFrame): O conjunto de dados a ser analisado.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)
        self.regional_analysis = RegionalAnalysis(df)

    def plot_average_salary_top_5_cities(self):
        """
        Gera um gráfico de barras mostrando a média salarial nas 5 cidades mais populosas do Paraná
        (Curitiba, Londrina, Maringá, Ponta Grossa, Cascavel) e salva o gráfico em PNG.
        """
        # Obter os dados das médias salariais nas 5 cidades mais populosas do Paraná
        salary_data = self.regional_analysis.average_salary_top_5_cities()

        # Converter o dicionário em um DataFrame para facilitar a visualização
        salary_df = (
            pd.DataFrame(list(salary_data.items()), columns=['Cidade', 'Média Salarial'])
            .sort_values(by="Média Salarial", ascending=False)
        )

        # Adicionar uma categoria genérica para uso com `hue`
        salary_df['Categoria'] = 'Top 5 Cidades do PR'

        # Criar o gráfico de barras
        plt.figure(figsize=(10, 6))
        sns.barplot(
            data=salary_df,
            x="Cidade",
            y="Média Salarial",
            hue="Categoria",  # Adiciona o `hue` para categorização
            palette="viridis"
        )

        # Configurações do gráfico
        plt.title("Média Salarial nas 5 Cidades Mais Populosas do Paraná", fontsize=14)
        plt.xlabel("Cidade", fontsize=12)
        plt.ylabel("Média Salarial", fontsize=12)
        plt.legend(title="Categoria", loc="upper right")

        # Adicionar os valores nas barras
        for i, bar in enumerate(plt.gca().patches):  # `patches` contém as barras
            value = bar.get_height()  # Obtém a altura da barra (o valor)
            if value > 0:
                plt.gca().text(  # Adiciona o texto no gráfico
                    bar.get_x() + bar.get_width() / 2,  # Coordenada X no centro da barra
                    value,  # Coordenada Y logo acima da barra
                    f'{value:,.2f}',  # Formata o número com 2 casas decimais
                    ha='center', va='bottom', fontsize=10  # Alinha o texto ao centro
                )

        plt.tight_layout()

        # Salvar o gráfico
        self.save_plot("average_salary_top_5_cities.png")

