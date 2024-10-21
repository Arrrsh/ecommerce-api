from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .auth import authenticate_user, create_access_token, get_current_user
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# create all tables in SQLite database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Application")

@app.get("/")
def docs_redirect() -> RedirectResponse:
    return RedirectResponse(url='/docs')

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user["username"]})
    logger.info("Login Successful")
    return {"access_token": access_token, "access_type": "bearer"}

# Retrieve all products
@app.get('/products', response_model=list[schemas.ProductResponse])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logger.info("Fetching all products")
    try:
        products = db.query(models.Product).offset(skip).limit(limit).all()
        logger.info(f"{len(products)} products retrieved")
        return products
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving products")

# Retrieve a specific product by its ID
@app.get("/products/{id}", response_model=schemas.ProductResponse)
def get_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Create a new Product
@app.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create product: {product.title}")
    try:
        db_product = models.Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        logger.info(f"Product {db_product.title} created successfully")
        return db_product
    except Exception as e:
        logger.error(f"Error creating product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error creating product")

# Update an existing product base on its ID
@app.put("/products/{id}", response_model=schemas.ProductResponse)
def update_product(id: int, product: schemas.ProductUpdate, db: Session=Depends(get_db)):
    logger.info(f"Attempting to update product with ID: {id}")
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        logger.warning(f"Product with ID {id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        for key, value in product.dict().items():
            setattr(db_product, key, value)

        db.commit()
        logger.info(f"Product {id} updated successfully")
        db.refresh(db_product)
        return db_product
    except Exception as e:
        logger.error(f"Error updating product {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error updating product")

# Delete a product by its ID:
@app.delete("/product/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.info(f"Delete request for product ID: {id}")
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product is None:
        logger.warning(f"Product with ID {id} not found")
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        db.delete(db_product)
        db.commit()
        logger.info(f"Product {id} deleted successfully")
        return
    except Exception as e:
        logger.error(f"Error deleting product {id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error deleting product")
