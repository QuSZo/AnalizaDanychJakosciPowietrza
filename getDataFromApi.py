import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Entities.SensorData import SensorData
from utils.Config import Config

config = Config.load_json("appsettings.json")
url = config.Openaq.Url
apiKey = config.Openaq.ApiKey

engine = create_engine(config.Postgres.ConnectionString)
Session = sessionmaker(bind=engine)

location = next(loc for loc in config["Openaq"]["Locations"] if loc["Name"] == "Rzeszow")
sensors = location["Sensors"]

response = requests.get(f"{url}/v3/locations/{location.LocationId}/latest", headers={"X-API-Key": apiKey})
jsonResponse = response.json()
results = jsonResponse["results"]

for data in results:
    parameter = next(sensor["Name"] for sensor in sensors if sensor["Id"] == data["sensorsId"])
    units = next(sensor["Units"] for sensor in sensors if sensor["Id"] == data["sensorsId"])
    sensorData = SensorData(
        LocationId=data["locationsId"],
        SensorId=data["sensorsId"],
        Location="Rzeszow",
        Datetime=data["datetime"]["local"],
        Lat=data["coordinates"]["latitude"],
        Lon=data["coordinates"]["longitude"],
        Parameter=parameter,
        Units=units,
        Value=data["value"]
    )
    with Session() as session:
        session.add(sensorData)
        session.commit()

