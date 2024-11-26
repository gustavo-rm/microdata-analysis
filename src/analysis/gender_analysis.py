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

    def compare_salary_by_gender_top_10_jobs(self):
        """
        Compara a média salarial entre homens e mulheres nos 10 cargos com mais empregados.

        Returns:
            pd.DataFrame: Um DataFrame contendo os 10 cargos com mais empregados e as seguintes informações:
                - Cargo
                - Total de Empregados
                - Salário Médio Masculino
                - Salário Médio Feminino
                - Diferença Salarial (Homens - Mulheres)
        """
        # Contar o número de empregados por cargo
        job_counts = self.df['cbo_2002_descricao'].value_counts().head(10).index

        # Filtrar o DataFrame para os 10 cargos com mais empregados
        top_jobs_df = self.df[self.df['cbo_2002_descricao'].isin(job_counts)]

        # Calcular a média salarial por gênero e cargo
        gender_salary = (
            top_jobs_df.groupby(['cbo_2002_descricao', 'sexo'])['valor_remuneracao_media']
            .mean()
            .unstack(fill_value=0)  # Organiza em colunas para "Masculino" e "Feminino"
            .reset_index()
        )

        # Adicionar total de empregados por cargo
        total_employees = (
            top_jobs_df.groupby('cbo_2002_descricao')['cbo_2002_descricao']
            .count()
            .rename("Total de Empregados")
        )

        # Adicionar a diferença salarial
        gender_salary['Diferença Salarial'] = (
                gender_salary.get('Masculino', 0) - gender_salary.get('Feminino', 0)
        )

        # Combinar os dados em um único DataFrame
        result = gender_salary.merge(
            total_employees, left_on='cbo_2002_descricao', right_index=True
        )

        # Renomear as colunas para melhor interpretação
        result.rename(
            columns={
                'cbo_2002_descricao': 'Cargo',
                'Masculino': 'Salário Médio Masculino',
                'Feminino': 'Salário Médio Feminino',
            },
            inplace=True,
        )

        return result.sort_values('Total de Empregados', ascending=False).reset_index(drop=True)

    def top_active_employees_by_year(self):
        """
        Calcula qual empregado (homem ou mulher) tem mais vínculos ativos para cada ano.

        Returns:
            pd.DataFrame: Um DataFrame contendo:
                - Ano
                - Sexo
                - ID do Município
                - Total de Vínculos Ativos
        """
        # Contar um vínculo ativo apenas se 'vinculo_ativo_3112' for 'Sim'
        self.df['quantidade_vinculos_ativos'] = self.df['vinculo_ativo_3112'].apply(lambda x: 1 if x == 'Sim' else 0)

        # Filtrar apenas os registros com vínculos ativos
        active_df = self.df[self.df['vinculo_ativo_3112'] == "Sim"]

        # Agrupar por ano, sexo e município, somando os vínculos ativos
        grouped = (
            active_df.groupby(['ano', 'sexo', 'id_municipio'])
            .agg({'quantidade_vinculos_ativos': 'sum'})
            .reset_index()
        )

        # Identificar o registro com mais vínculos ativos para cada ano e gênero
        top_active = grouped.loc[grouped.groupby(['ano', 'sexo'])['quantidade_vinculos_ativos'].idxmax()]

        # Renomear as colunas para facilitar a leitura
        top_active.rename(
            columns={
                'ano': 'Ano',
                'sexo': 'Gênero',
                'id_municipio': 'ID Município',
                'quantidade_vinculos_ativos': 'Total de Vínculos Ativos',
            },
            inplace=True,
        )

        return top_active.reset_index(drop=True)
