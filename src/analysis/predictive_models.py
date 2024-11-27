from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd

class PredictiveModels:
    """
    Classe para criação e avaliação de modelos preditivos.

    Esta classe fornece métodos para executar modelos de Regressão Linear
    e Regressão Logística, usados para prever valores numéricos e probabilidades,
    respectivamente.
    """

    def __init__(self, df):
        """
        Inicializa a instância da classe com um DataFrame.

        Parameters:
            df (pd.DataFrame): O conjunto de dados contendo as variáveis independentes e dependentes
                               para treinar e avaliar os modelos preditivos.
        """
        self.df = df

    def linear_regression_salary(self):
        """
        Executa Regressão Linear para prever salários com base em idade, tempo de emprego
        e grau de instrução.

        Este método treina um modelo de Regressão Linear para estimar a variável
        dependente `valor_remuneracao_media` usando as variáveis independentes
        `idade`, `tempo_emprego` e `grau_instrucao_apos_2005` (convertida para valores numéricos).

        Returns:
            dict: Contém os resultados do modelo, incluindo:
                - "Coeficientes": Um dicionário mapeando cada variável independente para seu coeficiente.
                - "Intercepto": O valor do intercepto da regressão.
                - "R²": O coeficiente de determinação (indicador de ajuste do modelo).
                - "Erro Quadrático Médio": Mede o erro médio das previsões.

        Exemplo de Uso:
            Use este método para prever salários em um conjunto de dados com variáveis
            como idade e tempo de emprego:
                results = linear_regression_salary()
                print(results['R²'], results['Erro Quadrático Médio'])
        """
        # Define as variáveis independentes
        features = ['idade', 'tempo_emprego']

        # Adiciona grau de instrução como variável numérica, se disponível
        if 'grau_instrucao_apos_2005' in self.df.columns:
            self.df['grau_instrucao_num'] = self.df['grau_instrucao_apos_2005'].factorize()[0]
            features.append('grau_instrucao_num')

        # Remove valores nulos das colunas relevantes
        df_clean = self.df.dropna(subset=features + ['valor_remuneracao_media'])

        # Define X (variáveis independentes) e y (variável dependente)
        X = df_clean[features]
        y = df_clean['valor_remuneracao_media']

        # Divide os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treina o modelo de Regressão Linear
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Retorna os resultados
        return {
            "Coeficientes": dict(zip(features, model.coef_)),
            "Intercepto": model.intercept_,
            "R²": model.score(X_test, y_test),
            "Erro Quadrático Médio": mean_squared_error(y_test, model.predict(X_test))
        }

    def logistic_regression_active_link(self):
        """
        Executa Regressão Logística para prever a probabilidade de vínculos ativos
        com base em idade, gênero e região.

        Este método treina um modelo de Regressão Logística para prever a variável
        dependente `vinculo_ativo_3112` (convertida para binária: "Sim" -> 1, "Não" -> 0)
        usando variáveis independentes como `idade`, `sigla_uf` e `sexo` (convertido para numérico).

        Returns:
            dict: Contém as métricas de avaliação do modelo:
                - "Acurácia": Proporção de previsões corretas.
                - "Relatório de Classificação": Métricas detalhadas (precisão, recall, F1-score)
                  para cada classe (ativo ou inativo).

        Exemplo de Uso:
            Use este método para prever vínculos ativos:
                results = logistic_regression_active_link()
                print(results['Acurácia'])
                print(results['Relatório de Classificação'])
        """
        # Define as variáveis independentes
        features = ['idade', 'sigla_uf', 'sexo']

        # Remove valores nulos das colunas relevantes
        df_clean = self.df.dropna(subset=features + ['vinculo_ativo_3112'])

        # Define X (variáveis independentes) e y (variável dependente)
        X = df_clean[features]
        y = df_clean['vinculo_ativo_3112'].apply(lambda x: 1 if x == "Sim" else 0)  # Binário

        # Converter variáveis categóricas para numéricas
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first'), ['sigla_uf', 'sexo']),
                ('num', 'passthrough', ['idade']),
            ]
        )

        # Criar o pipeline com o modelo
        model = Pipeline([
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(max_iter=1000))
        ])

        # Dividir os dados em conjuntos de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Treinar o modelo
        model.fit(X_train, y_train)

        # Retorna as métricas de avaliação
        predictions = model.predict(X_test)
        return {
            "Acurácia": accuracy_score(y_test, predictions),
            "Relatório de Classificação": classification_report(y_test, predictions, output_dict=True)
        }

    def predict_gender_salary_2024(self):
        """
        Prevê o salário médio de homens e mulheres em 2024 com base em um modelo de regressão linear.

        Returns:
            dict: Contém as previsões de salário médio para homens e mulheres.
        """
        predictions = {}

        # Definir o mapeamento de escolaridade
        education_mapping = {
            "ANALFABETO": 0,
            "ATE 5.A INC": 1,
            "5.A CO FUND": 2,
            "6. A 9. FUND": 3,
            "FUND COMPL": 4,
            "MEDIO INCOMP": 5,
            "MEDIO COMPL": 6,
            "SUP. INCOMP": 7,
            "SUP. COMP": 8,
            "MESTRADO": 9,
            "DOUTORADO": 10,
            "IGNORADO": -1
        }

        for gender in ['Masculino', 'Feminino']:
            # Filtrar o DataFrame para o gênero atual
            gender_df = self.df[self.df['sexo'] == gender].copy()

            # Aplicar o mapeamento na coluna grau_instrucao_apos_2005
            gender_df['grau_instrucao_num'] = gender_df['grau_instrucao_apos_2005'].map(education_mapping)

            # Treinar o modelo de regressão linear
            features = ['idade', 'tempo_emprego', 'grau_instrucao_num']
            gender_df_clean = gender_df.dropna(subset=features + ['valor_remuneracao_media'])
            X = gender_df_clean[features]
            y = gender_df_clean['valor_remuneracao_media']

            model = LinearRegression()
            model.fit(X, y)

            # Criar os dados futuros para previsão (ajustar conforme o contexto)
            future_data = pd.DataFrame({
                'idade': [25, 35, 40],  # Idades médias previstas
                'tempo_emprego': [12, 24, 36],  # Tempo de emprego médio esperado
                'grau_instrucao_num': [8, 9, 10]  # SUP. COMP, MESTRADO, DOUTORADO
            })

            # Prever os salários médios
            predicted_salaries = model.predict(future_data)
            predictions[gender] = predicted_salaries.mean()  # Salário médio previsto para o gênero

        return predictions
