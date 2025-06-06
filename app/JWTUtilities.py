from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta

# ✅ Password hashing config
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ JWT settings
SECRET_KEY = "myjwtsecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ✅ Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Decode JWT token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None