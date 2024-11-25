import matplotlib.pyplot as plt

class Visualizations:
    def __init__(self, df):
        self.df = df

    def plot_employment_by_region(self):
        """Gera um gráfico de barras para empregados por região."""
        grouped = self.df.groupby('sigla_uf')['quantidade_vinculos_ativos'].sum()
        grouped.plot(kind='bar')
        plt.title('Empregos por Região')
        plt.ylabel('Quantidade de Empregos')
        plt.xlabel('Região')
        plt.show()
