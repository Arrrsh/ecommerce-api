from pydantic import BaseModel

# Schema to create a product
class ProductCreate(BaseModel):
    title: str
    description: str
    price: float

# Schema to update a n existing product
class ProductUpdate(BaseModel):
    title: str
    description: str
    price: float

# Schema for response including product id

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_model = True

