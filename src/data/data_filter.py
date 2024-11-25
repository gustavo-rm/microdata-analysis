class DataFilter:
    def __init__(self, df):
        self.df = df

    def filter_by_cbo(self, cbo_list):
        """Filtra os dados com base nos códigos CBO."""
        return self.df[self.df['cbo_2002'].astype(str).str.startswith(tuple(cbo_list))]

    def filter_by_age(self, min_age, max_age):
        """Filtra os dados com base na faixa etária."""
        return self.df[(self.df['idade'] >= min_age) & (self.df['idade'] <= max_age)]

    def filter_by_state(self, state_code):
        """Filtra os dados por estado."""
        return self.df[self.df['sigla_uf'] == state_code]

