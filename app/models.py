from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
