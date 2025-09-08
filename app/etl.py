import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Definición de Rutas ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "restaurants.db"

# --- Función de Limpieza (sin cambios) ---
def clean_data(df: pd.DataFrame, city_name: str) -> pd.DataFrame:
    df['city'] = city_name
    price_mapping = {'€': 'Bajo', '€€ - €€€': 'Medio', '€€€€': 'Alto'}
    df['price_level'] = df['price_level'].map(price_mapping).fillna('No especificado')
    numeric_cols = ['rating', 'num_reviews', 'subrating_rate_food', 'subrating_rate_service', 'subrating_rate_atmosphere']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    relevant_cols = ['name', 'address', 'cuisine', 'rating', 'price_level', 'num_reviews', 'subrating_rate_food', 'subrating_rate_service', 'subrating_rate_atmosphere', 'url', 'city']
    final_df = pd.DataFrame()
    for col in relevant_cols:
        if col in df.columns:
            final_df[col] = df[col]
        else:
            final_df[col] = 0 if col in numeric_cols else 'No disponible'
    final_df['cuisine'] = final_df['cuisine'].fillna('No especificado')
    return final_df

# --- Función Principal del ETL (MODIFICADA) ---
def run_etl():
    try:
        logging.info("Iniciando el proceso de ETL...")
        
        # --- CAMBIO PRINCIPAL: Detectar todos los archivos CSV automáticamente ---
        csv_files = list(DATA_DIR.glob("*.csv"))
        if not csv_files:
            logging.error(f"No se encontraron archivos .csv en el directorio: {DATA_DIR}")
            return

        all_dataframes = []
        logging.info(f"Archivos CSV encontrados: {[file.name for file in csv_files]}")

        for csv_file in csv_files:
            city_name = csv_file.stem.replace('_', ' ').capitalize() # Convierte "palma_de_mallorca" a "Palma de mallorca"
            logging.info(f"Procesando datos para: {city_name}")
            df = pd.read_csv(csv_file)
            cleaned_df = clean_data(df, city_name)
            all_dataframes.append(cleaned_df)
        # --- FIN DEL CAMBIO ---

        logging.info("Combinando datos de todas las ciudades.")
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        logging.info(f"Creando la base de datos en: {DB_PATH}")
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        logging.info("Cargando datos limpios a la base de datos SQLite...")
        combined_df.to_sql('restaurants', con=engine, if_exists='replace', index=False)
        
        logging.info(f"¡Proceso ETL completado! {len(combined_df)} registros de {len(csv_files)} ciudades cargados.")

    except Exception as e:
        logging.error(f"Ocurrió un error inesperado durante el ETL: {e}")

if __name__ == "__main__":
    run_etl()