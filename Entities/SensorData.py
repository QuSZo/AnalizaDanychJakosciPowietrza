from datetime import datetime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column


Base = declarative_base()


class SensorData(Base):
    __tablename__ = "SensorData"

    Id: Mapped[int] = mapped_column(primary_key=True)
    LocationId: Mapped[int]
    SensorId: Mapped[int]
    Location: Mapped[str]
    Datetime: Mapped[datetime]
    Lat: Mapped[float]
    Lon: Mapped[float]
    Parameter: Mapped[str]
    Units: Mapped[str]
    Value: Mapped[float]

    def __repr__(self) -> str:
        return (f"SensorData(id={self.Id!r}, " +
                f"LocationId={self.LocationId}, " +
                f"SensorId={self.SensorId}, " +
                f"Location={self.Location}, " +
                f"Datetime={self.Datetime}, " +
                f"Lat={self.Lat}, " +
                f"Lon={self.Lon}, " +
                f"Parameter={self.Parameter}, " +
                f"Units={self.Units}, " +
                f"Value={self.Value})")
