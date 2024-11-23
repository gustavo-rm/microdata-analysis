from src.data_loader import DataLoader
from src.data_filter import DataFilter
from src.analysis import Analysis
from src.visualizations import Visualizations
from src.report_generator import ReportGenerator
from src.config import Config

def main():
    # 1. Carregar dados
    loader = DataLoader(Config.RAW_DATA_PATH + 'microdados.csv')
    data = loader.load_data()

    # 2. Preprocessar dados
    data = loader.preprocess_data(data)

    # 3. Filtrar dados
    filter = DataFilter(data)
    data_filtered = filter.filter_by_year(Config.DEFAULT_YEAR)

    # 4. Analisar dados
    analysis = Analysis(data_filtered)
    total_employees = analysis.calculate_total_employees()
    average_salary = analysis.calculate_average_salary()

    # 5. Visualizar dados
    viz = Visualizations(data_filtered)
    viz.plot_employment_by_region()

    # 6. Gerar relatório
    report = ReportGenerator({'total_employees': total_employees, 'average_salary': average_salary},
                             Config.OUTPUT_PATH + 'relatorio.docx')
    report.generate_word_report()

if __name__ == '__main__':
    main()
