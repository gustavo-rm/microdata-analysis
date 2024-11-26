import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
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
        # Obter os dados de diferença salarial
        gap = self.analysis.gender_salary_gap()

        # Criar um DataFrame com os dados
        salary_data = pd.DataFrame({
            'Gênero': ['Masculino', 'Feminino'],
            'Salário Médio': [gap["Salário Médio Masculino"], gap["Salário Médio Feminino"]],
            'Categoria': ['Comparação Salarial'] * 2  # Categoria genérica para uso de `hue`
        })

        # Configurar o gráfico
        plt.figure(figsize=(8, 6))
        sns.barplot(
            data=salary_data,
            x='Gênero',
            y='Salário Médio',
            hue='Gênero',  # Definir o hue para compatibilidade com versões futuras
            palette={"Masculino": "lightblue", "Feminino": "pink"}  # Cores personalizadas
        )

        # Configurações do gráfico
        plt.title("Diferença Salarial entre Gêneros")
        plt.ylabel("Salário Médio")
        plt.xlabel("Gênero")
        #plt.legend(title="Categoria", loc="upper right")
        plt.tight_layout()

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

        # Salvar o gráfico
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
        # Obter os dados de diferença salarial
        gap = self.analysis.gender_salary_gap()

        # Criar DataFrame para o gráfico de barras (diferença salarial)
        salary_data = pd.DataFrame({
            'Gênero': ['Masculino', 'Feminino'],
            'Salário Médio': [gap["Salário Médio Masculino"], gap["Salário Médio Feminino"]],
            'Categoria': ['Diferença Salarial'] * 2
        })

        # Calcular proporção de gêneros
        males = self.analysis.df[self.analysis.df['sexo'] == 'Masculino'].shape[0]
        females = self.analysis.df[self.analysis.df['sexo'] == 'Feminino'].shape[0]
        gender_sizes = [males, females]

        # Configurar o layout para gráficos lado a lado
        fig, axes = plt.subplots(1, 2, figsize=(16, 6))

        # Gráfico de barras (diferença salarial)
        sns.barplot(
            data=salary_data,
            x="Gênero",
            y="Salário Médio",
            hue="Categoria",  # Adiciona o hue para compatibilidade com Seaborn
            palette="Blues",
            ax=axes[0]
        )
        axes[0].set_title("Diferença Salarial entre Gêneros")
        axes[0].set_ylabel("Salário Médio")
        axes[0].set_xlabel("Gênero")
        axes[0].legend(title="Categoria", loc="upper right")

        # Gráfico de pizza (proporção de gêneros)
        axes[1].pie(
            gender_sizes,
            labels=['Masculino', 'Feminino'],
            autopct="%1.1f%%",
            colors=["#66b3ff", "#ff9999"],
            startangle=140
        )
        axes[1].set_title("Proporção de Gêneros")

        plt.tight_layout()
        self.save_plot("combined_gender_analysis.png")

    def plot_salary_comparison_top_10_jobs(self):
        """
        Gera um gráfico de barras comparando os salários médios de homens e mulheres
        nos 10 cargos com mais empregados e salva o gráfico em PNG.
        """
        # Obter os dados de comparação
        salary_comparison = self.analysis.compare_salary_by_gender_top_10_jobs()

        # Adicionar quebras de linha nos nomes dos cargos para evitar cortes
        salary_comparison['Cargo'] = salary_comparison['Cargo'].apply(
            lambda x: x.replace(' ', '\n') if len(x) > 20 else x)

        # Configurar o gráfico de barras
        plt.figure(figsize=(12, 8))
        bar_width = 0.35
        indices = range(len(salary_comparison))

        # Gráfico lado a lado para homens e mulheres
        plt.bar(
            indices,
            salary_comparison['Salário Médio Masculino'],
            bar_width,
            label='Homens',
            color='blue',
        )
        plt.bar(
            [i + bar_width for i in indices],
            salary_comparison['Salário Médio Feminino'],
            bar_width,
            label='Mulheres',
            color='pink',
        )

        # Configurações do gráfico
        plt.xlabel('Cargos', fontsize=12)
        plt.ylabel('Salário Médio', fontsize=12)
        plt.title('Comparação Salarial nos 10 Cargos com Mais Empregados', fontsize=14)
        plt.xticks(
            [i + bar_width / 2 for i in indices],
            salary_comparison['Cargo'],
            rotation=0,  # Rótulos centralizados
            ha='center'
        )
        plt.legend()

        # Salvar gráfico
        self.save_plot("salary_comparison_top_10_jobs.png")

    def plot_top_active_employees_by_year(self):
        """
        Gera um gráfico de barras mostrando o total de vínculos ativos por ano
        para homens e mulheres e salva o gráfico em PNG.
        """
        # Obter os dados de vínculos ativos
        active_employees = self.analysis.top_active_employees_by_year()

        # Configurar o gráfico
        plt.figure(figsize=(12, 8))
        sns.barplot(
            data=active_employees,
            x="Ano",
            y="Total de Vínculos Ativos",
            hue="Gênero",
            palette={"Masculino": "blue", "Feminino": "pink"},
        )

        # Configurações do gráfico
        plt.xlabel('Ano', fontsize=12)
        plt.ylabel('Total de Vínculos Ativos', fontsize=12)
        plt.title('Vínculos Ativos por Gênero em Cada Ano', fontsize=14)
        plt.legend(title="Gênero")

        # Salvar gráfico
        self.save_plot("top_active_employees_by_year.png")