import pandas as pd
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

# configuração database
POSTGRES_DBNAME=os.environ.get('POSTGRES_DBNAME')
POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
POSTGRES_PORT=os.environ.get('POSTGRES_PORT')


def main():
    try:
        conn = psycopg2.connect(
            database=POSTGRES_DBNAME,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
        )
        query = "SELECT * FROM ibge_dados ORDER BY year DESC;"
        df = pd.read_sql(query, conn)
        df.to_excel(f"ibge_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx", index=False)
        conn.close()
        return df
    except Exception as e:
        print(f'Error ao conectar com Banco de dados PostgreSQL: {e}')
        return pd.DataFrame()

-
if __name__ == "__main__":
    main()