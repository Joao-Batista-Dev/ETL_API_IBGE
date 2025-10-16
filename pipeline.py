import requests
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, IbgeData
from dotenv import load_dotenv

load_dotenv()

POSTGRES_DBNAME=os.environ.get('POSTGRES_DBNAME')
POSTGRES_USER=os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD=os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST=os.environ.get('POSTGRES_HOST')
POSTGRES_PORT=os.environ.get('POSTGRES_PORT')

DATABASE_URL = (
	f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
	f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
)

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_table():
    Base.metadata.create_all(engine)


def extract_date_ibge():
    url = 'https://servicodados.ibge.gov.br/api/v3/agregados/6579/periodos/all/variaveis/9324?localidades=N1[1]'
    
    response = requests.get(url)
    data = response.json()
    
    return data


def transform_date_ibge(data):
    country = data[0]['resultados'][0]['series'][0]['localidade']['nome']
    year_data = data[0]['resultados'][0]['series'][0]['serie']

    data_tranform = [
        {
            'country': country,
            'year': int(year),
            'population': int(population),
            'timestamp': datetime.now()
        }
        for year, population in year_data.items()
    ]

    return data_tranform

def save_data_postgresql(data):
    session = Session()
    try:
        for item in data:
            new_register = IbgeData(**item)
            session.add(new_register)
        session.commit()
        print('Registro Inseridos com sucesso!')
    except KeyboardInterrupt:
        session.close()
        print('Banco de dados Encerrado com Sucesso!')


if __name__ == "__main__":
    create_table()
    try:
        data_json = extract_date_ibge()
        if data_json:
            processed_data = transform_date_ibge(data_json) 
            save_data_postgresql(processed_data)
    except KeyboardInterrupt:
        print('Precesso interropido!')






