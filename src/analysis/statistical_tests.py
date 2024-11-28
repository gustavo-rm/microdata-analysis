from scipy.stats import ttest_ind, mannwhitneyu, f_oneway

class StatisticalTests:
    """
    Classe para execução de testes estatísticos.

    Esta classe fornece métodos para realizar:
    - Teste t de Student ou Mann-Whitney U Test: Para comparar salários entre homens e mulheres.
    - Análise de Variância (ANOVA): Para comparar salários entre diferentes regiões ou setores.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as variáveis para os testes estatísticos.
        """
        self.df = df

    def compare_gender_salaries(self, test="t-test"):
        """
        Compara salários entre homens e mulheres usando o Teste t de Student ou o Mann-Whitney U Test.

        Parameters:
            test (str): O teste a ser utilizado:
                        - "t-test": Teste t de Student.
                        - "mann-whitney": Mann-Whitney U Test.

        Returns:
            dict: Resultado do teste estatístico, incluindo o valor-p (p-value).

        Raises:
            ValueError: Se o teste especificado não for suportado.

        Exemplo de Uso:
            compare_gender_salaries(test="t-test")
        """
        # Filtra os salários por gênero
        male_salaries = self.df[self.df['sexo'] == 'Masculino']['valor_remuneracao_media'].dropna()
        female_salaries = self.df[self.df['sexo'] == 'Feminino']['valor_remuneracao_media'].dropna()

        # Verifica qual teste aplicar
        if test == "t-test":
            stat, p_value = ttest_ind(male_salaries, female_salaries, equal_var=False)
            test_name = "Teste t de Student"
        elif test == "mann-whitney":
            stat, p_value = mannwhitneyu(male_salaries, female_salaries, alternative='two-sided')
            test_name = "Mann-Whitney U Test"
        else:
            raise ValueError("Teste não suportado. Escolha 't-test' ou 'mann-whitney'.")

        return {
            "Teste": test_name,
            "Estatística": stat,
            "Valor-p": p_value
        }

    def anova_salary_by_region(self):
        """
        Compara salários entre diferentes regiões (estados) usando ANOVA.

        Returns:
            dict: Resultado do teste ANOVA, incluindo o valor-p (p-value).

        Exemplo de Uso:
            anova_salary_by_region()
        """
        # Agrupa salários por estado
        grouped_salaries = self.df.groupby('sigla_uf')['valor_remuneracao_media'].apply(list)

        # Aplica ANOVA apenas se houver mais de um grupo
        if len(grouped_salaries) < 2:
            return {"Erro": "ANOVA requer pelo menos dois grupos para comparação."}

        stat, p_value = f_oneway(*grouped_salaries)

        return {
            "Teste": "ANOVA",
            "Estatística": stat,
            "Valor-p": p_value
        }

    def anova_salary_by_sector(self):
        """
        Compara salários entre diferentes setores usando ANOVA.

        Returns:
            dict: Resultado do teste ANOVA, incluindo o valor-p (p-value).

        Exemplo de Uso:
            anova_salary_by_sector()
        """
        # Agrupa salários por setor (coluna 'cbo_2002')
        grouped_salaries = self.df.groupby('cbo_2002_descricao_familia')['valor_remuneracao_media'].apply(list)

        # Aplica ANOVA apenas se houver mais de um grupo
        if len(grouped_salaries) < 2:
            return {"Erro": "ANOVA requer pelo menos dois grupos para comparação."}

        stat, p_value = f_oneway(*grouped_salaries)

        return {
            "Teste": "ANOVA por Setor",
            "Estatística": stat,
            "Valor-p": p_value
        }
