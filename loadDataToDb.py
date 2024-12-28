import os
import gzip
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Entities.SensorData import SensorData
from utils.Config import Config


def process_and_load_files(root_directory, session_maker):
    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if file.endswith(".csv.gz"):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                with gzip.open(file_path, 'rt') as gz:
                    df = pd.read_csv(gz)

                sensor_data_objects = [
                    SensorData(
                        LocationId=row['location_id'],
                        SensorId=row['sensors_id'],
                        Location=row['location'],
                        Datetime=row['datetime'],
                        Lat=row['lat'],
                        Lon=row['lon'],
                        Parameter=row['parameter'],
                        Units=row['units'],
                        Value=row['value']
                    )
                    for _, row in df.iterrows()
                ]
                with session_maker() as session:
                    session.add_all(sensor_data_objects)
                    session.commit()
                print(f"File {file} loaded successfully.")


config = Config.load_json("appsettings.json")
engine = create_engine(config.Postgres.ConnectionString)
Session = sessionmaker(bind=engine)
dataDirectory = "data-2022"
process_and_load_files(dataDirectory, Session)

print("All files have been processed and loaded.")
