from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

#Helper Function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hashed(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expire_delta: timedelta = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user:
        logger.warning(f"Authentication failed for user: {username} - user not found")
        return False
    if not verify_password(password, user["hashed_password"]):
        logger.warning(f"Authentication failed for user: {username} - incorrect password")
        return False
    logger.info(f"User {username} successfully authenticated")
    return user

def get_current_user(token: str = Depends(oauth2_schema)):
    credetials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    try:
        payload = decode_access_token(token)
        username = payload.get("sub")
        if username is None:
            raise credetials_exception
    except JWTError:
        raise credetials_exception
    user = fake_user_db.get(username)
    if user is None:
        raise credetials_exception
    return user
    

# For Demo purpose
fake_user_db = {
    "user1": {"username": "user1", "hashed_password": get_password_hashed("password123")}
}