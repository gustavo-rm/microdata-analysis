from src.data.data_loader import DataLoader
from src.config import Config

def main():
    # 1. Carregar e preprocessar os dados
    loader = DataLoader(Config.RAW_DATA_PATH + "microdados.csv")
    data = loader.load_data()
    data = loader.preprocess_data(data)

    tipos = data['tipo_salario'].apply(type).value_counts()
    print("\nTipos de dados:")
    print(tipos)

if __name__ == "__main__":
    main()
