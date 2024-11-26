import os

class ReportGenerator:
    """
    Classe para gerar relatórios gráficos de todas as análises.

    Essa classe integra todas as visualizações geradas pelas classes de visualização específicas,
    criando um relatório completo.
    """

    def __init__(self, df, output_dir="report_visualizations"):
        """
        Inicializa a instância com o DataFrame e o diretório de saída.

        Parameters:
            df (pd.DataFrame): O conjunto de dados a ser analisado.
            output_dir (str): O diretório onde os gráficos serão salvos.
        """
        self.df = df
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_all_reports(self):
        """
        Gera todos os gráficos das análises realizadas pelas classes de visualização.
        """
        print("Gerando relatórios...")

        # Visualizações Básicas de Estatísticas
        print("Gerando gráficos básicos de estatísticas...")
        from src.report.basic_statistics_visualizer import BasicStatisticsVisualizer
        basic_visualizer = BasicStatisticsVisualizer(self.df, output_dir=self.output_dir)
        basic_visualizer.plot_metrics_bar_chart()
        basic_visualizer.plot_average_salary_by_year()

        # Análises dos Índices
        from src.report.employment_indexes_visualizer import EmploymentIndexesVisualizer
        indexes_visualizer = EmploymentIndexesVisualizer(self.df, output_dir=self.output_dir)
        indexes_visualizer.plot_salary_disparity()
        indexes_visualizer.plot_education_index()

        # Análises de Gênero
        print("Gerando gráficos de análise de gênero...")
        from src.report.gender_analysis_visualizer import GenderAnalysisVisualizer
        gender_visualizer = GenderAnalysisVisualizer(self.df, output_dir=self.output_dir)
        gender_visualizer.plot_gender_salary_gap()
        gender_visualizer.plot_gender_ratio()
        gender_visualizer.plot_combined_analysis()
        gender_visualizer.plot_salary_comparison_top_10_jobs()
        gender_visualizer.plot_top_active_employees_by_year()

        # Análises de Cargos
        print("Gerando gráficos de análise de cargos...")
        from src.report.position_analysis_visualizer import PositionAnalysisVisualizer
        position_visualizer = PositionAnalysisVisualizer(self.df, output_dir=self.output_dir)
        position_visualizer.plot_top_positions(top_n=15)
        #position_visualizer.plot_wordcloud_positions()

        # Modelos Preditivos
        #print("Gerando gráficos de modelos preditivos...")
        #from src.report.predictive_models_visualizer import PredictiveModelsVisualizer
        #models_visualizer = PredictiveModelsVisualizer(self.df, output_dir=self.output_dir)
        #models_visualizer.plot_linear_regression_coefficients()
        #models_visualizer.plot_logistic_regression_classification_report()
        #models_visualizer.plot_linear_regression_predictions()

        # Análise Regional
        print("Gerando gráficos de análise regional...")
        from src.report.regional_analysis_visualizer import RegionalAnalysisVisualizer
        regional_visualizer = RegionalAnalysisVisualizer(self.df, output_dir=self.output_dir)
        regional_visualizer.plot_average_salary_top_5_cities()

        # Testes Estatísticos
        #print("Gerando gráficos de testes estatísticos...")
        #from src.report.statistical_tests_visualizer import StatisticalTestsVisualizer
        #stats_visualizer = StatisticalTestsVisualizer(self.df, output_dir=self.output_dir)
        #stats_visualizer.plot_gender_salary_comparison(test="t-test")
        #stats_visualizer.plot_gender_salary_comparison(test="mann-whitney")
        #stats_visualizer.plot_anova_by_region()
        #stats_visualizer.plot_anova_by_sector()

        print("Relatórios completos gerados e salvos em:", self.output_dir)
