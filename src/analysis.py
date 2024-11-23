class Analysis:
    def __init__(self, df):
        self.df = df

    def calculate_total_employees(self):
        """Calcula o total de empregados."""
        return self.df['quantidade_vinculos_ativos'].sum()

    def calculate_average_salary(self):
        """Calcula o salário médio."""
        return self.df['salario_medio'].mean()

    def group_by_region_and_gender(self):
        """Agrupa dados por região e gênero, retornando estatísticas resumidas."""
        return self.df.groupby(['sigla_uf', 'genero']).agg({
            'quantidade_vinculos_ativos': 'sum',
            'salario_medio': 'mean'
        }).reset_index()
