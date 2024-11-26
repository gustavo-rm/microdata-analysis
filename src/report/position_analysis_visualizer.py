from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from src.report.base_visualizer import BaseVisualizer
from src.analysis.position_analysis import PositionAnalysis

class PositionAnalysisVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações baseadas na análise de cargos.
    """

    def __init__(self, df, output_dir="output"):
        """
        Inicializa a instância com um DataFrame e o diretório de saída para salvar os gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações sobre cargos.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Herda o construtor da classe BaseVisualizer
        self.analysis = PositionAnalysis(df)  # Instancia PositionAnalysis com o DataFrame

    def plot_top_positions(self, top_n=10, sort_by="Frequência", ascending=False):
        """
        Gera um gráfico de barras horizontais para os cargos mais frequentes.

        Parameters:
            top_n (int): O número de cargos mais frequentes a serem exibidos.
            sort_by (str): O critério para ordenar os resultados (padrão: "Frequência").
            ascending (bool): Define se a ordenação será crescente ou decrescente.
        """
        positions = self.analysis.analyze_unique_positions(sort_by=sort_by, ascending=ascending)
        top_positions = positions['Cargos'].head(top_n)

        plt.figure(figsize=(12, 8))
        sns.barplot(
            y=top_positions['Cargo'],
            x=top_positions['Frequência'],
            palette="Blues_r"
        )
        plt.title(f"Top {top_n} Cargos Mais Frequentes")
        plt.xlabel("Frequência")
        plt.ylabel("Cargos")
        plt.tight_layout()

        self.save_plot(f"top_{top_n}_positions.png")

    def plot_wordcloud_positions(self):
        """
        Gera uma nuvem de palavras para representar a frequência dos cargos.
        """
        positions = self.analysis.analyze_unique_positions(sort_by="Frequência", ascending=False)
        position_counts = positions['Cargos']

        # Gerar dicionário para a nuvem de palavras
        wordcloud_data = dict(zip(position_counts['Cargo'], position_counts['Frequência']))

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="white"
        ).generate_from_frequencies(wordcloud_data)

        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title("Nuvem de Palavras: Frequência de Cargos")
        plt.tight_layout()

        self.save_plot("wordcloud_positions.png")
