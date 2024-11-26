class BasicStatistics:
    """
    Classe para cálculos básicos de estatísticas sobre o conjunto de dados.

    Essa classe fornece métodos para calcular métricas fundamentais, como o número total
    de empregados, a média salarial e estatísticas de distribuição salarial.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as informações de empregados.
        """
        self.df = df

    def calculate_average_salary_by_year(self):
        """
        Calcula a média salarial para cada ano.

        Returns:
            pd.DataFrame: DataFrame com os anos e as médias salariais.
        """
        if 'ano' not in self.df.columns or 'valor_remuneracao_media' not in self.df.columns:
            raise ValueError("As colunas 'ano' e 'valor_remuneracao_media' são necessárias para esta análise.")

        # Agrupar por ano e calcular a média salarial
        salary_by_year = self.df.groupby('ano')['valor_remuneracao_media'].mean().reset_index()
        salary_by_year.columns = ['Ano', 'Média Salarial']
        return salary_by_year

    def calculate_total_employees(self):
        """
        Calcula o número total de empregados no conjunto de dados.

        Returns:
            int: Total de registros no DataFrame, representando o número de empregados.
        """
        return len(self.df)

    def calculate_average_salary(self):
        """
        Calcula o salário médio dos empregados.

        Returns:
            float: Média dos valores na coluna 'valor_remuneracao_media'.

        Exemplo de Uso:
            Use este método para obter uma visão geral do salário médio no conjunto de dados.
        """
        return self.df['valor_remuneracao_media'].mean()

    def salary_distribution(self):
        """
        Calcula estatísticas descritivas sobre os salários.

        Retorna informações sobre a média, mediana, desvio padrão e o coeficiente
        de variação dos salários no conjunto de dados.

        Returns:
            dict: Um dicionário contendo as seguintes métricas:
                - "Média Salarial": Média dos salários.
                - "Mediana Salarial": Valor central da distribuição salarial.
                - "Desvio Padrão": Variabilidade dos salários em relação à média.
                - "Coeficiente de Variação (%)": Proporção da variabilidade em relação à média.

        Exemplo de Uso:
            Use este método para entender a dispersão e a centralidade dos salários, especialmente
            útil para identificar se os salários estão uniformemente distribuídos ou possuem outliers.
        """
        return {
            "Média Salarial": self.df['valor_remuneracao_media'].mean(),
            "Mediana Salarial": self.df['valor_remuneracao_media'].median(),
            "Desvio Padrão": self.df['valor_remuneracao_media'].std(),
            "Coeficiente de Variação (%)": (self.df['valor_remuneracao_media'].std() / self.df['valor_remuneracao_media'].mean()) * 100
        }
