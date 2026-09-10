
from database import Base
from sqlalchemy import Boolean, Column, Integer, String, Float

class MateBase(Base):
    __tablename__ = "mates"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    material = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    descripcion = Column(String, nullable=False)
    disponible = Column(Boolean)


class Mate(MateBase):
    pass
