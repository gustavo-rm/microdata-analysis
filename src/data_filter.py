class DataFilter:
    def __init__(self, df):
        self.df = df

    def filter_by_year(self, year):
        """Filtra os dados pelo ano especificado."""
        return self.df[self.df['ano'] == year]

    def filter_by_age(self, min_age, max_age):
        """Filtra os dados por faixa etária."""
        return self.df[(self.df['idade'] >= min_age) & (self.df['idade'] <= max_age)]
