import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import logging

# Configuración del logging para ver el progreso y posibles errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- 1. Definición de Rutas (Paths) ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = BASE_DIR / "restaurants.db"

MADRID_CSV = DATA_DIR / "madrid.csv"
BARCELONA_CSV = DATA_DIR / "barcelona.csv"

# --- 2. Función de Limpieza de Datos ---
def clean_data(df: pd.DataFrame, city_name: str) -> pd.DataFrame:
    """Aplica una serie de limpiezas y transformaciones al DataFrame."""
    
    df['city'] = city_name
    
    price_mapping = {
        '€': 'Bajo',
        '€€ - €€€': 'Medio',
        '€€€€': 'Alto'
    }
    df['price_level'] = df['price_level'].map(price_mapping).fillna('No especificado')

    numeric_cols = [
        'rating', 'num_reviews', 'subrating_rate_food', 
        'subrating_rate_service', 
        'subrating_rate_atmosphere' # <-- CORRECCIÓN AQUÍ
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    relevant_cols = [
        'name', 'address', 'cuisine', 'rating', 'price_level', 'num_reviews',
        'subrating_rate_food', 'subrating_rate_service', 
        'subrating_rate_atmosphere', # <-- CORRECCIÓN AQUÍ
        'url', 'city'
    ]
    
    # Asegurarse de que todas las columnas relevantes existen en el dataframe
    final_df = pd.DataFrame()
    for col in relevant_cols:
        if col in df.columns:
            final_df[col] = df[col]
        else:
            final_df[col] = 0 if col in numeric_cols else 'No disponible'

    # Rellenar nulos en columnas de texto que podrían haber quedado
    final_df['cuisine'] = final_df['cuisine'].fillna('No especificado')
    
    return final_df

# --- 3. Función Principal del Proceso ETL ---
def run_etl():
    """Ejecuta el proceso completo de ETL."""
    try:
        logging.info("Iniciando el proceso de ETL...")
        
        logging.info(f"Cargando datos de {MADRID_CSV} y {BARCELONA_CSV}")
        df_madrid = pd.read_csv(MADRID_CSV)
        df_barcelona = pd.read_csv(BARCELONA_CSV)
        
        logging.info("Limpiando y transformando los datos...")
        cleaned_madrid = clean_data(df_madrid, 'Madrid')
        cleaned_barcelona = clean_data(df_barcelona, 'Barcelona')
        
        logging.info("Combinando datos de Madrid y Barcelona.")
        combined_df = pd.concat([cleaned_madrid, cleaned_barcelona], ignore_index=True)
        
        logging.info(f"Creando la base de datos en: {DB_PATH}")
        engine = create_engine(f"sqlite:///{DB_PATH}")
        
        logging.info("Cargando datos limpios a la base de datos SQLite...")
        combined_df.to_sql('restaurants', con=engine, if_exists='replace', index=False)
        
        logging.info(f"¡Proceso ETL completado! {len(combined_df)} registros cargados en la tabla 'restaurants'.")

    except FileNotFoundError as e:
        logging.error(f"Error: No se encontró el archivo CSV. Asegúrate de que los archivos están en la carpeta 'data'. Detalle: {e}")
    except Exception as e:
        logging.error(f"Ocurrió un error inesperado durante el ETL: {e}")

# --- 4. Ejecución del Script ---
if __name__ == "__main__":
    run_etl()