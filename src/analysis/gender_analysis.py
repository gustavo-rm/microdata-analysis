class GenderAnalysis:
    """
    Classe para análise de métricas relacionadas a gênero.

    Esta classe fornece métodos para calcular a diferença salarial entre gêneros
    e outras métricas de igualdade de gênero, como a proporção entre homens e mulheres
    em um conjunto de dados.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo informações de gênero,
                               salários e ocupações.
        """
        self.df = df

    def gender_salary_gap(self):
        """
        Calcula a diferença salarial entre gêneros.

        Agrupa os dados por gênero e calcula a média salarial para cada grupo.
        Em seguida, calcula a diferença salarial entre homens e mulheres.

        Returns:
            dict: Um dicionário contendo as seguintes informações:
                - "Salário Médio Masculino": Salário médio dos homens.
                - "Salário Médio Feminino": Salário médio das mulheres.
                - "Diferença Salarial": Diferença absoluta entre o salário médio dos homens e das mulheres.

        Exemplo de Uso:
            Use este método para identificar disparidades salariais entre gêneros
            no conjunto de dados.
        """
        salaries = self.df.groupby('sexo')['valor_remuneracao_media'].mean()
        return {
            "Salário Médio Masculino": salaries.get('Masculino', 0),
            "Salário Médio Feminino": salaries.get('Feminino', 0),
            "Diferença Salarial": salaries.get('Masculino', 0) - salaries.get('Feminino', 0)
        }

    def gender_equality_metrics(self, occupation=None, region=None):
        """
        Calcula métricas de igualdade de gênero com base em filtros opcionais de ocupação e região.

        Este método calcula:
        - A proporção entre o número de homens e mulheres (Razão de Gêneros).
        - A diferença salarial entre gêneros para os dados filtrados.

        Parameters:
            occupation (str, optional): O nome da ocupação para filtrar os dados (exemplo: "Desenvolvedor").
                                        Se None, considera todos os dados.
            region (str, optional): A sigla da UF para filtrar os dados (exemplo: "SP").
                                    Se None, considera todos os dados.

        Returns:
            dict: Um dicionário contendo:
                - "Razão de Gêneros": Proporção de homens para mulheres.
                - "Diferença Salarial": Diferença absoluta entre o salário médio dos homens e das mulheres
                                        nos dados filtrados.

        Exemplo de Uso:
            Para calcular a igualdade de gênero em uma ocupação específica e região:
                gender_equality_metrics(occupation="Desenvolvedor", region="SP")
        """
        # Cria uma cópia dos dados para evitar modificações no original
        df_filtered = self.df.copy()

        # Filtra por ocupação, se especificada
        if occupation:
            df_filtered = df_filtered[df_filtered['cbo_2002_descricao'] == occupation]

        # Filtra por região, se especificada
        if region:
            df_filtered = df_filtered[df_filtered['sigla_uf'] == region]

        # Conta o número de homens e mulheres
        gender_counts = df_filtered['sexo'].value_counts()
        males = gender_counts.get('Masculino', 0)
        females = gender_counts.get('Feminino', 0)

        # Calcula a média salarial por gênero
        salary_by_gender = df_filtered.groupby('sexo')['valor_remuneracao_media'].mean()

        return {
            "Razão de Gêneros": males / females if females > 0 else None,
            "Diferença Salarial": salary_by_gender.get('Masculino', 0) - salary_by_gender.get('Feminino', 0)
        }
