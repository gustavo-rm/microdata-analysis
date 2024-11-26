import matplotlib.pyplot as plt
import seaborn as sns
from src.report.base_visualizer import BaseVisualizer
from src.analysis.gender_analysis import GenderAnalysis


class GenderAnalysisVisualizer(BaseVisualizer):
    """
    Classe para gerar visualizações baseadas na análise de gênero.
    """

    def __init__(self, df, output_dir="output"):
        """
        Inicializa a instância com um DataFrame e o diretório de saída para salvar os gráficos.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações de gênero, salários e ocupações.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        super().__init__(output_dir)  # Herda o construtor da classe BaseVisualizer
        self.analysis = GenderAnalysis(df)  # Instancia GenderAnalysis com o DataFrame

    def plot_gender_salary_gap(self):
        """
        Gera um gráfico de barras comparando os salários médios entre gêneros e salva o gráfico.
        """
        gap = self.analysis.gender_salary_gap()

        # Dados para o gráfico
        labels = ['Masculino', 'Feminino']
        salaries = [gap["Salário Médio Masculino"], gap["Salário Médio Feminino"]]

        plt.figure(figsize=(8, 6))
        sns.barplot(x=labels, y=salaries, palette="Blues")
        plt.title("Diferença Salarial entre Gêneros")
        plt.ylabel("Salário Médio")
        plt.xlabel("Gênero")
        plt.tight_layout()

        self.save_plot("gender_salary_gap.png")

    def plot_gender_ratio(self, occupation=None, region=None):
        """
        Gera um gráfico de pizza mostrando a proporção entre homens e mulheres.

        Parameters:
            occupation (str, optional): O nome da ocupação para filtrar os dados.
            region (str, optional): A sigla da UF para filtrar os dados.
        """
        metrics = self.analysis.gender_equality_metrics(occupation=occupation, region=region)

        # Dados para o gráfico
        labels = ['Masculino', 'Feminino']
        males = self.analysis.df[self.analysis.df['sexo'] == 'Masculino'].shape[0]
        females = self.analysis.df[self.analysis.df['sexo'] == 'Feminino'].shape[0]
        sizes = [males, females]

        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=["#66b3ff", "#ff9999"], startangle=140)
        plt.title("Proporção de Gêneros")
        plt.tight_layout()

        # Nome personalizado do arquivo com filtros
        filename = "gender_ratio"
        if occupation:
            filename += f"_occupation_{occupation.replace(' ', '_')}"
        if region:
            filename += f"_region_{region}"
        filename += ".png"

        self.save_plot(filename)

    def plot_combined_analysis(self):
        """
        Combina análise de diferença salarial e proporção de gêneros em um único gráfico.
        """
        gap = self.analysis.gender_salary_gap()

        # Dados para o gráfico de barras
        labels = ['Masculino', 'Feminino']
        salaries = [gap["Salário Médio Masculino"], gap["Salário Médio Feminino"]]

        males = self.analysis.df[self.analysis.df['sexo'] == 'Masculino'].shape[0]
        females = self.analysis.df[self.analysis.df['sexo'] == 'Feminino'].shape[0]
        gender_sizes = [males, females]

        # Configurar o layout para gráficos lado a lado
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Gráfico de barras (diferença salarial)
        sns.barplot(x=labels, y=salaries, palette="Blues", ax=axes[0])
        axes[0].set_title("Diferença Salarial entre Gêneros")
        axes[0].set_ylabel("Salário Médio")
        axes[0].set_xlabel("Gênero")

        # Gráfico de pizza (proporção de gêneros)
        axes[1].pie(gender_sizes, labels=labels, autopct="%1.1f%%", colors=["#66b3ff", "#ff9999"], startangle=140)
        axes[1].set_title("Proporção de Gêneros")

        plt.tight_layout()
        self.save_plot("combined_gender_analysis.png")
