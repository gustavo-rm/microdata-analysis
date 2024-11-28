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

    def generate_basic_statistics_reports(self):
        """
        Gera gráficos relacionados a estatísticas básicas.
        """
        print("Gerando gráficos básicos de estatísticas...")
        from src.report.basic_statistics_visualizer import BasicStatisticsVisualizer
        visualizer = BasicStatisticsVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_metrics_bar_chart()
        visualizer.plot_average_salary_by_year()

    def generate_employment_indexes_reports(self):
        """
        Gera gráficos relacionados aos índices de emprego.
        """
        print("Gerando gráficos de índices de emprego...")
        from src.report.employment_indexes_visualizer import EmploymentIndexesVisualizer
        visualizer = EmploymentIndexesVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_salary_disparity()
        visualizer.plot_education_index()

    def generate_gender_analysis_reports(self):
        """
        Gera gráficos relacionados à análise de gênero.
        """
        print("Gerando gráficos de análise de gênero...")
        from src.report.gender_analysis_visualizer import GenderAnalysisVisualizer
        visualizer = GenderAnalysisVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_gender_salary_gap()
        visualizer.plot_gender_ratio()
        visualizer.plot_combined_analysis()
        visualizer.plot_salary_comparison_top_10_jobs()
        visualizer.plot_top_active_employees_by_year()

    def generate_position_analysis_reports(self):
        """
        Gera gráficos relacionados à análise de cargos.
        """
        print("Gerando gráficos de análise de cargos...")
        from src.report.position_analysis_visualizer import PositionAnalysisVisualizer
        visualizer = PositionAnalysisVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_top_positions(top_n=15)

    def generate_regional_analysis_reports(self):
        """
        Gera gráficos relacionados à análise regional.
        """
        print("Gerando gráficos de análise regional...")
        from src.report.regional_analysis_visualizer import RegionalAnalysisVisualizer
        visualizer = RegionalAnalysisVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_average_salary_top_5_cities()

    def generate_predictive_models_reports(self):
        """
        Gera gráficos relacionados aos modelos preditivos.
        """
        print("Gerando gráficos de modelos preditivos...")
        from src.report.predictive_models_visualizer import PredictiveModelsVisualizer
        visualizer = PredictiveModelsVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_linear_regression_coefficients()
        visualizer.plot_logistic_regression_classification_report()
        visualizer.plot_linear_regression_predictions()

    def generate_statistical_tests_reports(self):
        """
        Gera gráficos relacionados aos testes estatísticos.
        """
        print("Gerando gráficos de testes estatísticos...")
        from src.report.statistical_tests_visualizer import StatisticalTestsVisualizer
        visualizer = StatisticalTestsVisualizer(self.df, output_dir=self.output_dir)
        visualizer.plot_gender_salary_comparison(test="t-test")
        visualizer.plot_gender_salary_comparison(test="mann-whitney")
        visualizer.plot_anova_by_region()
        visualizer.plot_anova_by_sector()

    def generate_all_reports(self):
        """
        Gera todos os gráficos das análises realizadas pelas classes de visualização.
        """
        print("Gerando relatórios...")
        self.generate_basic_statistics_reports()
        self.generate_employment_indexes_reports()
        self.generate_gender_analysis_reports()
        self.generate_position_analysis_reports()
        self.generate_regional_analysis_reports()
        self.generate_predictive_models_reports()
        self.generate_statistical_tests_reports()
        print("Relatórios completos gerados e salvos em:", self.output_dir)
