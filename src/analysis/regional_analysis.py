class RegionalAnalysis:
    """
    Classe para análise de métricas regionais relacionadas ao mercado de trabalho.

    Esta classe fornece métodos para calcular a concentração de empregos e a média salarial
    em diferentes estados ou municípios, permitindo identificar disparidades regionais.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações sobre regiões,
                               salários e empregos.
        """
        self.df = df

    def regional_analysis(self):
        """
        Calcula o número total de empregados e o salário médio por estado.

        Returns:
            pd.DataFrame: DataFrame com as seguintes colunas:
                - "sigla_uf": Sigla do estado.
                - "Total Empregados": Quantidade de empregados por estado.
                - "Salário Médio": Salário médio dos empregados no estado.

        Exemplo de Uso:
            Use este método para obter uma visão geral do mercado de trabalho por estado.
        """
        return self.df.groupby('sigla_uf')['valor_remuneracao_media'].agg(['mean', 'count']).rename(columns={
            'mean': 'Salário Médio',
            'count': 'Total Empregados'
        }).reset_index()

    def concentration_of_jobs(self, level="estado"):
        """
        Calcula a concentração de empregos em tecnologia por estado ou município.

        Parameters:
            level (str): Nível de agregação:
                         - "estado" para calcular por estado (coluna 'sigla_uf').
                         - "municipio" para calcular por município (coluna 'id_municipio').

        Returns:
            pd.DataFrame: DataFrame com as seguintes colunas:
                - "Local": Nome ou código do estado/município.
                - "Total Empregados": Quantidade total de empregados na região.

        Raises:
            ValueError: Se o nível especificado for diferente de "estado" ou "municipio".

        Exemplo de Uso:
            Para calcular a concentração de empregos por estado:
                concentration_of_jobs(level="estado")
            Para calcular por município:
                concentration_of_jobs(level="municipio")
        """
        if level == "estado":
            group_col = 'sigla_uf'
            label = 'Estado'
        elif level == "municipio":
            group_col = 'id_municipio'
            label = 'Município'
        else:
            raise ValueError("O nível deve ser 'estado' ou 'municipio'.")

        concentration = self.df.groupby(group_col)['quantidade_vinculos_ativos'].sum().reset_index()
        concentration.columns = [label, 'Total Empregados']
        return concentration

    def average_salary_by_region(self, level="estado"):
        """
        Calcula o salário médio por estado ou município.

        Parameters:
            level (str): Nível de agregação:
                         - "estado" para calcular por estado (coluna 'sigla_uf').
                         - "municipio" para calcular por município (coluna 'id_municipio').

        Returns:
            pd.DataFrame: DataFrame com as seguintes colunas:
                - "Local": Nome ou código do estado/município.
                - "Salário Médio": Salário médio dos empregados na região.

        Raises:
            ValueError: Se o nível especificado for diferente de "estado" ou "municipio".

        Exemplo de Uso:
            Para calcular o salário médio por estado:
                average_salary_by_region(level="estado")
            Para calcular por município:
                average_salary_by_region(level="municipio")
        """
        if level == "estado":
            group_col = 'sigla_uf'
            label = 'Estado'
        elif level == "municipio":
            group_col = 'id_municipio'
            label = 'Município'
        else:
            raise ValueError("O nível deve ser 'estado' ou 'municipio'.")

        average_salary = self.df.groupby(group_col)['valor_remuneracao_media'].mean().reset_index()
        average_salary.columns = [label, 'Salário Médio']
        return average_salary
