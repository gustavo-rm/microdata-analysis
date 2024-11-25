class EmploymentIndexes:
    """
    Classe para calcular índices relacionados ao mercado de trabalho em tecnologia.

    Esta classe fornece métodos para calcular:
    - Índice de Disparidade Salarial (IDS): Mede a disparidade salarial em termos percentuais.
    - Índice de Concentração Regional (ICR): Mede a proporção do total de empregados
      tecnológicos em um estado específico em relação ao total nacional.
    - Índice de Escolaridade: Mede a proporção de empregados com ensino superior completo
      ou mais avançado em relação ao total.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações de salários,
                               região e escolaridade.
        """
        self.df = df

    def salary_disparity_index(self):
        """
        Calcula o Índice de Disparidade Salarial (IDS).

        O IDS é calculado como:
            IDS = ((Salário Médio Masculino - Salário Médio Feminino) / Salário Médio Masculino) * 100

        Returns:
            float: Índice de disparidade salarial em termos percentuais.

        Exemplo de Uso:
            Use este método para identificar disparidades salariais entre gêneros.
        """
        salaries = self.df.groupby('sexo')['valor_remuneracao_media'].mean()
        male_salary = salaries.get('Masculino', 0)
        female_salary = salaries.get('Feminino', 0)

        if male_salary == 0:  # Evita divisão por zero
            return None

        ids = ((male_salary - female_salary) / male_salary) * 100
        return ids

    def regional_concentration_index(self, state):
        """
        Calcula o Índice de Concentração Regional (ICR).

        O ICR mede a proporção do total de empregados em tecnologia em um estado
        específico em relação ao total nacional.

        Parameters:
            state (str): Sigla do estado para o qual calcular o ICR.

        Returns:
            float: Índice de concentração regional em termos percentuais.

        Exemplo de Uso:
            Para calcular o ICR de São Paulo:
                regional_concentration_index("SP")
        """
        total_national = self.df['quantidade_vinculos_ativos'].sum()
        total_state = self.df[self.df['sigla_uf'] == state]['quantidade_vinculos_ativos'].sum()

        if total_national == 0:  # Evita divisão por zero
            return None

        icr = (total_state / total_national) * 100
        return icr

    def education_index(self):
        """
        Calcula o Índice de Escolaridade.

        O índice mede a proporção de empregados com ensino superior completo ou mais avançado
        em relação ao total de empregados.

        Returns:
            float: Índice de escolaridade em termos percentuais.

        Exemplo de Uso:
            Use este método para avaliar o nível de qualificação educacional dos empregados.
        """
        # Considera que a coluna 'grau_instrucao_apos_2005' contém a escolaridade
        higher_education_levels = ['MEDIO COMPL', 'SUP. INCOMP', 'SUP. COMP', 'MESTRADO', 'DOUTORADO']

        total_employees = len(self.df)
        higher_education_employees = self.df[self.df['grau_instrucao_apos_2005'].isin(higher_education_levels)].shape[0]

        if total_employees == 0:  # Evita divisão por zero
            return None

        education_index = (higher_education_employees / total_employees) * 100
        return education_index
