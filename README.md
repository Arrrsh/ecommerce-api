# E-Commerce API

This is a RESTful API for managing products in an e-commerce application. It is built using FastAPI and includes features like JWT-based authentication, product management, and SQLite as the database.

## Features

- **Product Management:**
  - `GET /products`: Retrieve a list of all products.
  - `GET /products/{id}`: Retrieve a product by its ID.
  - `POST /products`: Create a new product (authenticated).
  - `PUT /products/{id}`: Update an existing product by its ID (authenticated).
  - `DELETE /products/{id}`: Delete a product by its ID (authenticated).
  
- **Authentication and Authorization:**
  - JWT-based authentication to protect sensitive endpoints.
  - Login with `POST /token` to get an access token.
  
- **Database:**
  - Uses SQLite for data persistence.

## Requirements

- Python 3.11+
- FastAPI
- SQLite

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Setup the database
FastAPI will automatically create the SQLite database and tables when you run the application. Ensure that the database is initialized when first running the app.

### 5. Run the FastAPI server
```bash
uvicorn main:app --reload
```
The server will run at http://127.0.0.1:8000.

### Protected Routes:
```bash
POST /products
PUT /products/{id}
DELETE /products/{id}
```
### Unit Tests
Unit tests for this project can be run using pytest.

### Install pytest:
```bash
pip install pytest
```
### Run tests:
```bash
pytest
```
