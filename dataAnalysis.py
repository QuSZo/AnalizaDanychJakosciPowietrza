from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy.orm import sessionmaker
from Entities.SensorData import SensorData
from utils.Config import Config
from sqlalchemy import create_engine, select
import matplotlib.pyplot as plt


def fetch_data(session_maker, parameter, day_range=None):
    stmt = select(SensorData)

    if day_range is not None:
        previous_week = datetime.now() - timedelta(days=day_range)
        stmt = stmt.where(SensorData.Datetime >= previous_week)

    stmt = stmt.where(SensorData.Parameter == parameter).order_by(SensorData.Datetime)

    with session_maker() as session:
        return list(session.scalars(stmt))


def create_plot(data_plot, parameter):
    plt.figure(figsize=(10, 6))
    plt.plot(data_plot['Datetime'], data_plot['Value'], label='pm10', color='blue')
    plt.title(f'{parameter} Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


config = Config.load_json("appsettings.json")
engine = create_engine(config.Postgres.ConnectionString)
Session = sessionmaker(bind=engine)

for parameter in ["co", "no2", "pm10", "pm25"]:
    sensorData = fetch_data(Session, parameter)

    data = pd.DataFrame([{
        "Datetime": obj.Datetime,
        "Value": obj.Value
    } for obj in sensorData])

    create_plot(data, parameter)

